#!/bin/bash

if [ -f /home/gan/stasi/stasi.conf ]; then
  source /home/gan/stasi/stasi.conf
else
  echo "Missing /home/gan/stasi/stasi.conf"
  exit 1
fi

for data_source in "${DATA_SOURCES[@]}"; do
  /usr/bin/rsync -e "ssh -o 'StrictHostKeyChecking no'" -avz $data_source /home/gan/stasi/data/
done



