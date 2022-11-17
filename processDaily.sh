#!/bin/sh
#
# processDaily.sh <city>

# TODO: fix filter to used city name passed

if [ $# -eq 0 ]; then
  echo "No arguments supplied"
  exit 0
fi

CITY=$1

if [ $CITY == "alameda" ]; then
  curl "https://services5.arcgis.com/ROBnTHSNjoZ2Wm1P/arcgis/rest/services/COVID_19_Statistics/FeatureServer/6/query?where=1%3D1&outFields=$CITY,dtcreate&outSR=4326&f=json" | jq --arg city "$CITY" -r -f filter.jq
fi

if [ $CITY == "emeryville" ]; then
  curl "https://services5.arcgis.com/ROBnTHSNjoZ2Wm1P/arcgis/rest/services/COVID_19_Statistics/FeatureServer/6/query?where=1%3D1&outFields=$CITY,dtcreate&outSR=4326&f=json" | jq --arg city "$CITY" -r -f filterEm.jq
fi

if [ $CITY == "oakland" ]; then
  curl "https://services5.arcgis.com/ROBnTHSNjoZ2Wm1P/arcgis/rest/services/COVID_19_Statistics/FeatureServer/6/query?where=1%3D1&outFields=$CITY,dtcreate&outSR=4326&f=json" | jq --arg city "$CITY" -r -f filterOak.jq
fi
