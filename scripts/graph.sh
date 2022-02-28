#!/bin/bash

if [ -f /stasi/stasi.conf ]; then
  source /stasi/stasi.conf
else
  echo "Missing /stasi/stasi.conf"
  exit 1
fi

html="<html><body>"

i=0
for graph in "${GRAPHS[@]}"; do
  for image_file in `TZ=$GRAPH_TZ python3 /scripts/rrd_graph.py data images $i $graph`; do
    html+="<img src='$image_file' />"
  done
  let i++
done

html+="</body></html>"

echo $html > images/index.html
