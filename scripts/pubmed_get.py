import requests
import time
import re
import os
import shutil


def pmid_get(d):
	print "\n### Getting pubmed ids ###"
	start = time.time()

	url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
	payload = {'db': 'pubmed',
               'term': '"1900/01/01"[PDAT] : "2100/12/31"[PDAT] AND (hasabstract[text] AND medline[sb])',
               'retmax': '1000000000'}

	# get the data
	r = requests.get(url, params=payload)

	out = open(d + 'pmids_raw.txt', 'w')
	out.write(r.text)
	end = time.time()
	print "\tTime taken:", round((end - start) / 60, 3), "minutes"


def parse_pmids(d):
	print "\n### Parsing ids ###"
	counter = 0
	start = time.time()
	f = open(d + 'pmids_raw.txt', 'r')
	out = open(d + 'pmids_trimmed.txt', 'w')
	for line in f:
		counter += 1
		l = re.search(r'.*?<Id>(.*?)</Id>', line)
		if l:
			out.write(l.group(1) + "\n")
	end = time.time()
	print "\tTime taken:", round((end - start) / 60, 3), "minutes"
	return counter


def split_pmids(counter, split_num, d):
	print "\n### Splitting ids into separate files ###"
	start = time.time()

	n = counter / split_num
    # max value for retmax is 10000
	if (n > 10000):
		print "\tMore files needed - max number of ids per search is 10,000!"
		n = 10000
		split_num = round(counter / n)
	print "\tSplitting " + str(counter) + " ids into " + str(split_num) + " new files..."
	com = 'split -a 10 -l ' + str(n) + ' ' + d + 'pmids_trimmed.txt ' + d + 'pmid_split.'
	# print com
	os.system(com)
	# need to replace new lines with commas
	end = time.time()
	print "\tEach file has around " + str(n) + " pubmed ids."
	print "\tTime taken:", round((end - start) / 60, 3), "minutes"
	return (n)


def medline_get(f):
	print "\n### Getting medline files for file - ", f + " ###"
	start = time.time()
	ids = open(f).read().replace('\n', ',')
	# print ids

	# ids='26037045,25913273,25913194,25899830,25899612,25899321,25858171,25854326,25854185,25846844,25833681,25833380,25833299,25828538,25825272,25820539,25820482,25820447,25820375,2582024'
	url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?'
	payload = {'db': 'pubmed', 'id': ids, 'retmax': '10000', 'retmode': 'text', 'rettype': 'medline'}

	# POST with data
	r = requests.post(url, data=payload)

	out = open(f + '.medline', 'w')
	out.write(r.text)

	end = time.time()
	print "\tTime taken:", round((end - start) / 60, 3), "minutes"


def run_pubmed_get(keep_tmp):
	start = time.time()
	# set tmp directory
	d = 'tmp_pubmed/'
	num_files = 4

	if not os.path.exists(d):
		os.makedirs(d)

	pmid_get(d)
	c = parse_pmids(d)
	split_pmids(c, num_files, d)
	for file in os.listdir(d):
		if file.startswith("pmid_split"):
			if not file.endswith(".medline"):
				file = d + file
				medline_get(file)
	cat_com = "cat " + d + "/*.medline > pubmed_medline.txt"
	os.system(cat_com)

	# clean up
	if (keep_tmp == False):
		shutil.rmtree(d)
	end = time.time()
	print "\nTotal time taken:", round((end - start) / 60, 3), "minutes"


pmid_get('tmp_pubmed/')
# run_pubmed_get(keep_tmp=True)
