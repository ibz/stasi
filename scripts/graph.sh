#!/bin/bash

if [ -f /home/gan/stasi/stasi.conf ]; then
  source /home/gan/stasi/stasi.conf
else
  echo "Missing /home/gan/stasi/stasi.conf"
  exit 1
fi

html="<html><body>"

i=0
for graph in "${GRAPHS[@]}"; do
  for image_file in `TZ=$GRAPH_TZ python3 /home/gan/stasi/scripts/rrd_graph.py /home/gan/stasi/data /var/www/html $i $graph`; do
    html+="<img src='$image_file' />"
  done
  let i++
done

html+="</body></html>"

echo $html > /var/www/html/index.html
