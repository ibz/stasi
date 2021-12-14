#!/bin/bash
/usr/bin/rsync -e "ssh -o 'StrictHostKeyChecking no'" -avz sensor@$1:/home/sensor/data/ /data/

