jupyter notebook

Convert Notebook to a Python script that can be run from the command line
-------------------------------------------------------------------------

jupyter nbconvert --to script 'alameda_covid.ipynb' 

Basic script approach
---------------------

* Run script to grab latest CV19 numbers from web and convert to CSV
* Run Python script to parse CSV and generate graphs
* Do something with the graphs
