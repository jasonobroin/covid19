jupyter notebook

Convert Notebook to a Python script that can be run from the command line
-------------------------------------------------------------------------

jupyter nbconvert --to script 'covid_notebook.ipynb' 
(convert_to_script.sh)

Basic script approach
---------------------

* Run script to grab latest CV19 numbers from web and convert to CSV
* Run Python script to parse CSV and generate graphs
	use ipython <file.py>
* Do something with the graphs

Basic usage
-----------

* Run scripts to pull latest data from web and process via Jupyter notebook, generate graphs etc.
  ./update.sh
# Generate website and upload to webserver
  ./hugo_build_and_upload.sh

Useful web pages
----------------

* https://www.dataquest.io/blog/jupyter-notebook-tutorial/

Data source
-----------

* https://data.acgov.org/search?q=covid
  (specifically https://data.acgov.org/datasets/5d6bf4760af64db48b6d053e7569a47b_3/geoservice)