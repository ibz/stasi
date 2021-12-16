#!/bin/bash

if [ -f /stasi/stasi.conf ]; then
  source /stasi/stasi.conf
else
  echo "Missing /stasi/stasi.conf"
  exit 1
fi

for data_source in "${DATA_SOURCES[@]}"; do
  /usr/bin/rsync -e "ssh -o 'StrictHostKeyChecking no'" -avz $data_source /stasi/data/
done

