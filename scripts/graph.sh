#!/bin/bash

if [ -f /stasi/stasi.conf ]; then
  source /stasi/stasi.conf
else
  echo "Missing /stasi/stasi.conf"
  exit 1
fi

TZ=$GRAPH_TZ python3 /scripts/rrd_graph.py data images
