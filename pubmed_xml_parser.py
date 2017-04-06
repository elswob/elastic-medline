import os, json
import xmltodict
from csv import reader

dataDir = '/Users/be15516/projects/elastic-medline/'

def parse_stream(_, xml_data):
	#print xml_data
	for p in xml_data['PubmedArticle']:
		print p
	return True

def xml_stream():
	for xml_file in os.listdir(dataDir+'xml/'):
		print "### "+xml_file+" ###"
		with open(dataDir+'/xml/'+xml_file, "rb") as f:
			xmltodict.parse(f,item_depth=1,item_callback=parse_stream)

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

def parse_json():
	for json_file in os.listdir(dataDir+'json/'):
		counter=0
		if os.path.exists(dataDir+'/elastic-json/'+json_file):
			print 'Elastic JSON file '+json_file+' already created'
		else:
			print '#### Parsing '+json_file+' ####'
			with open(dataDir+'/json/'+json_file) as data_file:
				json_data = json.load(data_file)
			mData = []
			#for each publication
			d = {}
			for p in json_data['PubmedArticleSet']['PubmedArticle']:
				counter+=1
				#parse medline data
				if 'MedlineCitation' in p:
					#check for single article files
					if p == 'MedlineCitation':
						medLineData = json_data['PubmedArticleSet']['PubmedArticle']['MedlineCitation']
					else:
						medLineData = p['MedlineCitation']
					#pubmed ID
					if 'PMID' in medLineData:
						print medLineData['PMID']['#text']
						d['pmid']=medLineData['PMID']['#text']
					else:
						print json_file+' : '+str(counter)+ " has no pmid"
					#date created
					if 'DateCreated' in medLineData:
						d['DateCreated']=medLineData['DateCreated']['Year']+'-'+medLineData['DateCreated']['Month']+'-'+medLineData['DateCreated']['Day']
					else:
						print json_file+' : '+str(counter)+ " has no DateRevised"
					#date revised
					if 'DateRevised' in medLineData:
						d['DateRevised']=medLineData['DateRevised']['Year']+'-'+medLineData['DateRevised']['Month']+'-'+medLineData['DateRevised']['Day']
					else:
						print json_file+' : '+str(counter)+ " has no DateRevised"
					#article
					if 'Article' in medLineData:
						d['ArticleTitle']=medLineData['Article']['ArticleTitle']
					else:
						print json_file+' : '+str(counter)+ " has no Article"
					#mesh
					if 'MeshHeadingList' in medLineData:
						meshList = []
						meshData = medLineData['MeshHeadingList']['MeshHeading']
						if type(meshData) is list:
							for mesh in meshData:
								descriptor = mesh['DescriptorName']['#text']
								if mesh['DescriptorName']['@MajorTopicYN'] == 'Y':
									print mesh
									meshList.append(mesh['DescriptorName']['#text'])
								if 'QualifierName' in mesh:
									if type(mesh['QualifierName']) is list:
										for q in mesh['QualifierName']:
											if q['@MajorTopicYN'] == 'Y':
												#print mesh
												print descriptor+'/'+q['#text']
												meshList.append(descriptor+'/'+q['#text'])
									elif type(mesh['QualifierName']) is dict:
										if mesh['QualifierName']['@MajorTopicYN'] == 'Y':
											#print mesh
											print descriptor+'/'+mesh['QualifierName']['#text']
											meshList.append(descriptor+'/'+mesh['QualifierName']['#text'])

						elif type(meshData) is dict:
							descriptor = meshData['DescriptorName']['#text']
							if meshData['DescriptorName']['@MajorTopicYN'] == 'Y':
								print mesh
								meshList.append(meshData['DescriptorName']['#text'])
							if 'QualifierName' in mesh:
								if type(mesh['QualifierName']) is list:
									for q in mesh['QualifierName']:
										if q['@MajorTopicYN'] == 'Y':
											#print mesh
											print descriptor+'/'+q['#text']
											meshList.append(descriptor+'/'+q['#text'])
								elif type(mesh['QualifierName']) is dict:
									if mesh['QualifierName']['@MajorTopicYN'] == 'Y':
										#print mesh
										print descriptor+'/'+mesh['QualifierName']['#text']
										meshList.append(descriptor+'/'+mesh['QualifierName']['#text'])
						d['Mesh'] = meshList
					#	d['mesh'] = medLineData['MeshHeadingList']['MeshHeading']
				else:
					print str(counter)+" has no MedlineCitation"
				#create new data set for new pubmed article
				if len(p)==2:
					mData.append(d)
					d = {}
			mData.append(d)
			w = open(dataDir+'/elastic-json/'+json_file,'w')
			#
			counter=0
			for m in mData:
				if len(m)>1:
					counter+=1
					print m
					w.write('{ "index" : { "_index" : "pubmed-json", "_type" : "type1", "_id" : "'+str(counter)+'" } }\n')
					w.write(json.dumps(m)+'\n')
		#print json.dumps(mData)

def main():
	#xml_to_json()
	#parse_json()
	xml_stream()

if __name__ == '__main__':
	main()