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
		with open(dataDir+'/json/'+json_file) as data_file:
			json_data = json.load(data_file)
		if 'publication-base_uk:dois' in json_data['publication-template:GetPublicationResponse']['core:result']['core:content']:
			print json_data['publication-template:GetPublicationResponse']['core:result']['core:content']['publication-base_uk:dois']
		else:
			print json_file+ ".json has no DOI"

def main():
	xml_to_json()
	parse_json()

if __name__ == '__main__':
	main()