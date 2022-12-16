#!/bin/bash

CONFIG="/home/gan/stasi/stasi.conf"
DATADIR="/home/gan/stasi-data/"
OUTDIR="/var/www/html"

if [ -f $CONFIG ]; then
  source $CONFIG
else
  echo "Missing $CONFIG"
  exit 1
fi

html="<html><body>"

i=0
for graph in "${GRAPHS[@]}"; do
  for image_file in `TZ=$GRAPH_TZ python3 /home/gan/stasi/scripts/rrd_graph.py $DATADIR $OUTDIR $i $graph`; do
    echo "Generated $image_file!"
    html+="<img src='$image_file' />"
  done
  let i++
done

html+="</body></html>"

echo $html > $OUTDIR/index.html
