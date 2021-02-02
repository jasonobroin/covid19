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

Useful web pages
----------------

* https://www.dataquest.io/blog/jupyter-notebook-tutorial/
