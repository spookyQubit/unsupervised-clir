#!/bin/bash

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
