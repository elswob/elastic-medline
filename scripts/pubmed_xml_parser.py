import os, json, gzip, marshal
import xmltodict
from xml_to_json import parse_xml
from csv import reader

dataDir = '/Users/be15516/projects/elastic-medline/data/'

mData = []
counter=0

def parse_stream(_, xml_data):
	#print xml_data
	global mData,counter
	for p in xml_data:
		#print p
		if p == 'MedlineCitation':
			#print counter
			if counter % 10000 == 0:
				print counter
			counter+=1
			#for each publication
			d = {}
			medLineData = xml_data[p]
			pmid = ''
			if 'PMID' in medLineData:
				print medLineData['PMID']['#text']
				d['pmid']=medLineData['PMID']['#text']
				pmid = d['pmid']=medLineData['PMID']['#text']
			else:
				print str(counter)+ " has no pmid"  # date created
			if 'DateCreated' in medLineData:
				d['DateCreated'] = medLineData['DateCreated']['Year'] + '-' + medLineData['DateCreated']['Month'] + '-' + medLineData['DateCreated']['Day']
			else:
				print pmid+" : "+str(counter) + " has no DateRevised"
			# date revised
			if 'DateRevised' in medLineData:
				d['DateRevised'] = medLineData['DateRevised']['Year'] + '-' + medLineData['DateRevised']['Month'] + '-' + medLineData['DateRevised']['Day']
			else:
				print pmid+" : "+str(counter) + " has no DateRevised"

			# article
			if 'Article' in medLineData:
				d['ArticleTitle'] = medLineData['Article']['ArticleTitle']
				if 'Journal' in medLineData['Article']:
					if 'ISSN' in medLineData['Article']['Journal']:
						d['issn'] = medLineData['Article']['Journal']['ISSN']['#text']
					else:
						print str(counter) + " has no ISSN"
						d['issn'] = 'n/a'
					if 'Title' in medLineData['Article']['Journal']:
						d['JournalTitle'] = medLineData['Article']['Journal']['Title']
					else:
						d['JournalTitle'] = 'n/a'
					if 'ISOAbbreviation' in medLineData['Article']['Journal']:
						d['ISOAbbreviation'] = medLineData['Article']['Journal']['ISOAbbreviation']
					else:
						d['ISOAbbreviation'] = 'n/a'

				#abstract
				if 'Abstract' in medLineData['Article']:
					if 'AbstractText' in medLineData['Article']['Abstract']:
							if medLineData['Article']['Abstract'] == 'AbstractText':
								d['Abstract'] = medLineData['Article']['Abstract']['AbstractText']
							else:
								d['Abstract']=''
								for a in medLineData['Article']['Abstract']:
									print a
									if a == 'AbstractText':
										if type(medLineData['Article']['Abstract'][a]) is list:
											for text in medLineData['Article']['Abstract'][a]:
												if '#text' in text:
													d['Abstract'] += text['#text']
										else:
											d['Abstract'] = medLineData['Article']['Abstract'][a]
				elif 'OtherAbstract' in medLineData:
					d['Abstract'] = medLineData['OtherAbstract']['AbstractText']
				else:
					print pmid+" : "+str(counter) + " has no Abstract"
			else:
				print pmid+" : "+str(counter) + " has no Article"

			# mesh
			if 'MeshHeadingList' in medLineData:
				meshList = []
				meshData = medLineData['MeshHeadingList']['MeshHeading']
				if type(meshData) is list:
					for mesh in meshData:
						descriptor = mesh['DescriptorName']['#text']
						if mesh['DescriptorName']['@MajorTopicYN'] == 'Y':
							#print mesh
							meshList.append(mesh['DescriptorName']['#text'])
						if 'QualifierName' in mesh:
							if type(mesh['QualifierName']) is list:
								for q in mesh['QualifierName']:
									if q['@MajorTopicYN'] == 'Y':
										# print mesh
										#print descriptor + '/' + q['#text']
										meshList.append(descriptor + '/' + q['#text'])
							elif type(mesh['QualifierName']) is dict:
								if mesh['QualifierName']['@MajorTopicYN'] == 'Y':
									# print mesh
									print descriptor + '/' + mesh['QualifierName']['#text']
									meshList.append(descriptor + '/' + mesh['QualifierName']['#text'])

				elif type(meshData) is dict:
					descriptor = meshData['DescriptorName']['#text']
					if meshData['DescriptorName']['@MajorTopicYN'] == 'Y':
						#print mesh
						meshList.append(meshData['DescriptorName']['#text'])
					if 'QualifierName' in mesh:
						if type(mesh['QualifierName']) is list:
							for q in mesh['QualifierName']:
								if q['@MajorTopicYN'] == 'Y':
									# print mesh
									#print descriptor + '/' + q['#text']
									meshList.append(descriptor + '/' + q['#text'])
						elif type(mesh['QualifierName']) is dict:
							if mesh['QualifierName']['@MajorTopicYN'] == 'Y':
								# print mesh
								#print descriptor + '/' + mesh['QualifierName']['#text']
								meshList.append(descriptor + '/' + mesh['QualifierName']['#text'])
				d['Mesh'] = meshList
			mData.append(d)
		if p == 'PubmedData':
			pubMedData = xml_data[p]
			if 'History' in pubMedData:
				for pDate in pubMedData['History']['PubMedPubDate']:
					if pDate['@PubStatus']=='pubmed':
						d['PubMedPubDate'] = pDate['Year'] + '-' + pDate['Month'] + '-' + pDate['Day']
				#print pubMedData['History']['PubMedPubDate'][0]['@PubStatus']

	return True

def xml_stream():
	global mData
	global counter
	for xml_file in os.listdir(dataDir+'xml/'):
		if xml_file.endswith('.xml.gz'):
			json_file = xml_file.replace('.xml.gz','.json.gz')
			if os.path.exists(dataDir+'/elastic-json/'+json_file):
				print xml_file+" already parsed"
			else:
				print "### "+xml_file+" ###"
				#item_depth is key, needs to be 2 for xml dowmloads form pubmed, 3 for output from my entrez-direct script
				with gzip.open(dataDir+'/xml/'+xml_file, "rb") as f:
					xmltodict.parse(f,item_depth=2,item_callback=parse_stream)

				counter=0
				w = gzip.open(dataDir+'/elastic-json/'+json_file,'w')
				for m in mData:
					if len(m)>1:
						counter+=1
						#print m
						w.write('{ "index" : { "_index" : "pubmed-index", "_type" : "type1", "_id" : "'+str(counter)+'" } }\n')
						w.write(json.dumps(m)+'\n')
				mData = []


def xml_to_json():
	for xml_file in os.listdir(dataDir+'xml/'):
		json_file = xml_file.replace('.xml','.json')
		if os.path.exists(dataDir+'/json/'+json_file):
			print 'JSON file '+json_file+' already created'
		else:
			print 'Converting '+xml_file+' to JSON'
			w = open(dataDir+'/json/'+json_file,'w')
			with open(dataDir+'/xml/'+xml_file) as fd:
				doc = xmltodict.parse(fd.read())
				w.write(json.dumps(doc))
				#print json.dumps(doc)


if __name__ == '__main__':
	xml_stream()