#!/bin/sh
#
# 1. Pull the latest data as JSON and convert to CSV
# TODO 1a. Check if data has changed and whether format is good (no lines without cases at end of file)
# 2. Run the Juypter notebook (as ipython) on CSV to generate graphs
# TODO 3. Report some summary info

echo Download Oakland COVID data as JSON
./processDaily.sh oakland > oakland/daily_data.csv
echo Download Alameda COVID data as JSON
./processDaily.sh alameda > alameda/daily_data.csv
echo Convert to CSV format
COVID_CITY=oakland ipython covid_notebook.py
COVID_CITY=alameda ipython covid_notebook.py
