#!/bin/sh
#
# 1. Pull the latest data as JSON and convert to CSV
# TODO 1a. Check if data has changed and whether format is good (no lines without cases at end of file)
# 2. Run the Juypter notebook (as ipython) on CSV to generate graphs
# TODO 3. Report some summary info

echo Download Alameda COVID data as JSON
./alamedaDaily.sh > alameda_data.csv
echo Convert to CSV format
ipython alameda_covid.py