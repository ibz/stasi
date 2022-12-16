#!/bin/bash

CONFIG="/home/gan/stasi/stasi.conf"
DATADIR="/home/gan/stasi-data/"

if [ -f $CONFIG ]; then
  source $CONFIG
else
  echo "Missing $CONFIG"
  exit 1
fi

for data_source in "${DATA_SOURCES[@]}"; do
  /usr/bin/rsync -e "ssh -o 'StrictHostKeyChecking no'" -avz $data_source $DATADIR
done
