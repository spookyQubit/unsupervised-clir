#!/bin/bash

# Does the following things:
# 1) Downloads zipped file from a websource=url 
# 2) Unzips it in destination=directory 
# 3) Removes the zipped file 

# Usage 
# ./download_unzip.sh  -s "https://madata.bib.uni-mannheim.de/273/UnsupCLIREmbeddings.tar.gz"
# ./download_unzip.sh  -s "www.cs.jhu.edu/~kevinduh/a/wikiclir2018/sasaki18.tgz" -d Data
 
# Default destination where the file will be unzipped is the current (.) directory.
DESTINATION=.

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -d|--destination)
    DESTINATION="$2"
    shift # past argument
    shift # past value
    ;;
    -s|--websource)
    WEBSOURCE="$2"
    shift # past argument
    shift # past value
    ;; 
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

echo DESTINATION  = "${DESTINATION}"
echo WEBSOURCE     = "${WEBSOURCE}"

if [ ! -d $DESTINATION ]; then
    
    mkdir -p $DESTINATION
fi

echo "Downloading file from $WEBSOURCE"
wget  -O ./temp.tgz $WEBSOURCE

echo "Extracting files"
tar -xvzf temp.tgz -C $DESTINATION

rm temp.tgz

exit 0
