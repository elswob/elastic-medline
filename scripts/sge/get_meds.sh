#!/bin/bash
# request resources:
#PBS -l nodes=1:ppn=1
#PBS -l walltime=02:00:00

# on compute node, change directory to 'submission directory':
cd $PBS_O_WORKDIR

STARTTIME=$(date +%s)

echo "Getting medline data..."

#need to convert integer format to match split output
fName=$(printf %05d ${PBS_ARRAYID})
echo "fName = $fName"
pList=$(cat $tmpDir/splits/x$fName | tr "\n" "," | head -c -1)

if [ ! -d $tmpDir/meds ];  then
	mkdir $tmpDir/meds
fi

C="curl http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi? \
-d'db=pubmed&id=$pList&retmax=10000$retmode=text&rettype=medline' > $tmpDir/meds/${PBS_ARRAYID}.med"

#url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?'
#payload = {'db': 'pubmed', 'id': ids, 'retmax': '10000', 'retmode': 'text', 'rettype': 'medline'}


echo $C
eval $C

ENDTIME=$(date +%s)
echo "Time taken: $(($ENDTIME - $STARTTIME))"