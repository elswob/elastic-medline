#!/bin/bash

STARTTIME=$(date +%s)

if [ -z $1 ]; then
	echo "Need year 1" && exit
fi

if [ -z $2 ]; then
	echo "Need year 2" && exit
fi

if [ -z $3 ]; then
	echo "Need tmp directory" && exit 
fi

if [ -z $4 ]; then
	echo "Need number of CPUs" && exit
fi

y1=$1
y2=$2
tmpDir=$3

if [ ! -d $tmpDir ];  then
	mkdir $tmpDir
fi

#./load_data/pubmed_get_sge.sh 1970 1973 tmp_pub 10

SCRIPT=$( readlink -m $( type -p $0 ))      # Full path to script
#echo $SCRIPT
BASE_DIR=`dirname ${SCRIPT}` 

s=$(( $RANDOM % 100000 ));

#if [ ! -s $tmpDir/all_pmids.txt ]; then
	echo "Downloading pubmed IDs..."
	#j1=$(qsub -q veryshort -N get_pmids.${s} -t $y1-$(($y2-1)) -v tmpDir=$tmpDir $BASE_DIR/get_ids.sh)
	#echo $j1
#fi	

if [ ! -s $tmpDir/all_pmids.txt ]; then
	echo "Parsing downloaded pubmed IDs..."
	#j2=$(qsub -N parse_pmids.${s} -W depend=afterok:${j1%%.*} -v tmpDir=$tmpDir $BASE_DIR/prep_ids.sh)
	j2=$(qsub -N prep_pmids.${s} -v tmpDir=$tmpDir $BASE_DIR/prep_ids.sh)
fi

qsub -N get_medline.${s} -t 1-3 -v tmpDir=$tmpDir $BASE_DIR/get_meds.sh 

#qsub -N merge_meds.${s} -hold_jid get_medline.${s} -V "merge_meds.sh $tmpDir"

