#!/bin/bash
# request resources:
#PBS -l nodes=1:ppn=1
#PBS -l walltime=02:00:00

# on compute node, change directory to 'submission directory':
cd $PBS_O_WORKDIR
STARTTIME=$(date +%s)

echo "### Getting pubmed ids ###"

echo "The Array ID is: ${PBS_ARRAYID}" 

if [ ! -d $tmpDir/pmids ];  then
	mkdir $tmpDir/pmids
fi

y2=$((PBS_ARRAYID+1))

C="curl http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi? \
-d'db=pubmed&term=\"${PBS_ARRAYID}/01/01\"[PDAT] : \"${y2}/12/31\"[PDAT] AND (hasabstract[text] AND medline[sb])&retmax=1000000000' > $tmpDir/pmids/${PBS_ARRAYID}.pmids"

echo $C
eval $C

ENDTIME=$(date +%s)
echo "Time taken: $(($ENDTIME - $STARTTIME))"