import os, json
import xmltodict
from csv import reader

dataDir = '/Users/be15516/projects/elastic-medline/'

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
		print '#### Parsing '+json_file+' ####'
		with open(dataDir+'/json/'+json_file) as data_file:
			json_data = json.load(data_file)
		mData = []
		#for each publication
		for p in json_data['PubmedArticleSet']['PubmedArticle']:
			counter+=1
			#create empty dictionary
			#d={'pmid':'','date_created':''}
			d = {}
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
					d['DateCreated']=medLineData['DateCreated']
				else:
					print json_file+' : '+str(counter)+ " has no DateRevised"
				#date revised
				if 'DateRevised' in medLineData:
					d['DateRevised']=medLineData['DateRevised']
				else:
					print json_file+' : '+str(counter)+ " has no DateRevised"
				#article
				if 'Article' in medLineData:
					d['Article']=medLineData['Article']
				else:
					print json_file+' : '+str(counter)+ " has no Article"
			else:
				print str(counter)+" has no MedlineCitation"
		mData.append(d)
	print json.dumps(mData)

def main():
	xml_to_json()
	parse_json()

if __name__ == '__main__':
	main()