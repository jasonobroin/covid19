
# coding: utf-8

# TODO: Read data as JSON directly from https://services5.arcgis.com/ROBnTHSNjoZ2Wm1P/arcgis/rest/services/COVID_19_Statistics/FeatureServer/3/query?where=1%3D1&outFields=dtcreate,Alameda,GlobalID,OBJECTID&outSR=4326&f=json and then transform to csv

# Now we have a CSV format - load it (this can be elided if we load and transform the JSON directly
# 
# TODO: Rename "I" to "Total Cases"

# In[666]:

import os

#LOCAL_DATA_ROOT = "/Users/jason/development/cv19/"
CITY = os.getenv('COVID_CITY', 'alameda')
print('Parsing data from ' + CITY)
LOCAL_DATA_ROOT = "./"
CSV_FILE = "daily_data.csv"
CSV_OUTPUT_FILE = "daily_delta_data.csv"

CASES_PER_DAY_GRAPH_FILE = "daily_cases.png"

CSV_PATH = os.path.join(LOCAL_DATA_ROOT, CITY, CSV_FILE)
CSV_OUTPUT_PATH = os.path.join(LOCAL_DATA_ROOT, CITY, CSV_OUTPUT_FILE)
CASES_PER_DAY_GRAPH_PATH = os.path.join(LOCAL_DATA_ROOT, CITY, CASES_PER_DAY_GRAPH_FILE)

print('Parsing data from file ' + CSV_PATH)

get_ipython().magic(u'matplotlib auto')
import pandas as pd

def load_covid_data(csv_path=CSV_PATH):
    return pd.read_csv(csv_path)


# In[ ]:




# In[667]:

covid = load_covid_data()
covid.head()


# In[668]:

covid.info()


# Clean up the data - replace NaN with 0; replace <10 with 0

# In[669]:

covid["Total"].fillna(0,inplace=True)
covid["Total"].replace("<10", 0,inplace=True)


# Convert I field from an object (as it originally had strings) to an int

# In[670]:

covid["Total"] = covid["Total"].astype(str).astype(int)


# In[ ]:




# In[671]:

covid.info()


# In[ ]:




# In[672]:

covid.head()


# In[ ]:




# In[673]:

pd.set_option('display.max_rows', None)
print(covid)


# In[ ]:




# Work out the case delta between each row to generate a number of new cases per day as the second column

# In[674]:

test = covid["Total"]
print(test)


# In[ ]:




# UNKNOWN: Why is diff on a specific row (or on test) not working?
# The "I" column is an object, not an int - convert?

# In[675]:

test.diff()


# Convert dates into standard pandas data format

# In[676]:

covid['std-date'] = pd.to_datetime(covid["dates"], format='%d/%m/%Y')
print(covid)
covid.info()


# In[ ]:




# Need to sort by incrementing dates

# In[677]:

covid = covid.sort_values(by='std-date',ascending=True) 


# In[678]:

print(covid)


# In[ ]:




# Work out diffs; convert NaN to the original value and convert diff column to int
# TODO: Move diff column to column two

# In[679]:

covid["I"] = covid["Total"].diff().fillna(covid['Total']).astype(int)


# In[680]:

print(covid)


# In[681]:

covid.info()


# Swap cells to be in the correct organization for WHO-PAHO

# In[682]:

cols = list(covid.columns)
a, b = cols.index('Total'), cols.index('I')
cols[b], cols[a] = cols[a], cols[b]
covid = covid[cols]


# In[683]:

print(covid)


# We have a lot of dates with no data (at 0 total value) at the end of the dataset; drop these invalid data. 
# 
# TODO: We currently do it from a known end point, but we should look for where I goes negative (or we transition to 0) and drop all after this point

# In[684]:

#covid = covid.loc[0:276]
#print(covid)


# In[ ]:




# Remove the std-date column from the dataframe we write as CSV as it confused WHO-PAHO

# In[685]:

csv_covid = covid.drop(['std-date'], axis=1)


# In[686]:

csv_covid.to_csv(CSV_OUTPUT_PATH, header=True, index=False) 


# In[ ]:




# Display covid cases over time

# In[691]:

covid.plot(x="std-date", y="Total", title=CITY + " Covid cumulative cases")


# Show log y - change in growth over time

# In[688]:

covid.plot(x="std-date", y="Total",logy=True)


# In[ ]:




# In[689]:

ax = covid.plot(x="std-date", y="I", kind="bar", figsize=(20,10), title=CITY + " Covid cases per day")

n = 10

ticks = ax.xaxis.get_ticklocs()
ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
ax.xaxis.set_ticks(ticks[::n])
ax.xaxis.set_ticklabels(ticklabels[::n])
ax.figure.tight_layout()

ax.figure.show()


# In[690]:

ax.figure.savefig(CASES_PER_DAY_GRAPH_PATH)


# In[ ]:



