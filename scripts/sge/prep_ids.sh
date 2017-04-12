#!/bin/bash
# request resources:
#PBS -l nodes=1:ppn=1
#PBS -l walltime=02:00:00

# on compute node, change directory to 'submission directory':
cd $PBS_O_WORKDIR

STARTTIME=$(date +%s)

echo "Preparing pubmed IDs..."

cat $tmpDir/pmids/*.pmids > $tmpDir/all_pmid_data.txt 
cat $tmpDir/all_pmid_data.txt  | perl -n -e'/<Id>(\d+)<\/Id>/ && print "$1\n"' | sort | uniq > $tmpDir/all_pmids.txt

split -a 5 -d -l 10000 $tmpDir/all_pmids.txt 

if [ ! -d $tmpDir/splits ];  then
	mkdir $tmpDir/splits
fi

mv x* $tmpDir/splits

#echo $(printf %05d $a)

ENDTIME=$(date +%s)
echo "Time taken: $(($ENDTIME - $STARTTIME))"