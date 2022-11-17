
# coding: utf-8

# TODO: Read data as JSON directly from https://services5.arcgis.com/ROBnTHSNjoZ2Wm1P/arcgis/rest/services/COVID_19_Statistics/FeatureServer/3/query?where=1%3D1&outFields=dtcreate,Alameda,GlobalID,OBJECTID&outSR=4326&f=json and then transform to csv

# Now we have a CSV format - load it (this can be elided if we load and transform the JSON directly
# 
# TODO: Rename "I" to "Total Cases"

# In[116]:

import os

#LOCAL_DATA_ROOT = "/Users/jason/development/cv19/"
CITY = os.getenv('COVID_CITY', 'alameda')
print('Parsing data from ' + CITY)
LOCAL_DATA_ROOT = "./"
CSV_FILE = "daily_data.csv"
CSV_OUTPUT_FILE = "daily_delta_data.csv"
CSV_OUTPUT_WEEKLY_FILE = "weekly_delta_data.csv"
JSON_OUTPUT_FILE = "data.json"

CASES_PER_DAY_GRAPH_FILE = "daily_cases.png"
CASES_CUMULATIVE_FILE = "cumulative_cases.png"
CASES_CUMULATIVE_LOG_FILE = "cumulative_cases_log.png"

CSV_PATH = os.path.join(LOCAL_DATA_ROOT, CITY, CSV_FILE)
CSV_OUTPUT_PATH = os.path.join(LOCAL_DATA_ROOT, CITY, CSV_OUTPUT_FILE)
CSV_WEEKLY_PATH = os.path.join(LOCAL_DATA_ROOT, CITY, CSV_OUTPUT_WEEKLY_FILE)
CASES_PER_DAY_GRAPH_PATH = os.path.join(LOCAL_DATA_ROOT, CITY, CASES_PER_DAY_GRAPH_FILE)
CUMULATIVE_GRAPH_PATH = os.path.join(LOCAL_DATA_ROOT, CITY, CASES_CUMULATIVE_FILE)
CUMULATIVE_LOG_GRAPH_PATH = os.path.join(LOCAL_DATA_ROOT, CITY, CASES_CUMULATIVE_LOG_FILE)

JSON_OUTPUT_PATH = os.path.join(LOCAL_DATA_ROOT, CITY, JSON_OUTPUT_FILE)

print('Parsing data from file ' + CSV_PATH)

get_ipython().magic(u'matplotlib auto')
import pandas as pd

def load_covid_data(csv_path=CSV_PATH):
    return pd.read_csv(csv_path)


# In[ ]:




# In[117]:

covid = load_covid_data()
covid.head()


# In[118]:

covid.info()


# Clean up the data - replace NaN with 0; replace <10 with 0

# In[119]:

covid["Total"].fillna(0,inplace=True)
covid["Total"].replace("<10", 0,inplace=True)


# Convert I field from an object (as it originally had strings) to an int

# In[120]:

covid["Total"] = covid["Total"].astype(str).astype(int)


# In[ ]:




# In[121]:

covid.info()


# In[ ]:




# In[122]:

covid.head()


# In[ ]:




# In[123]:

pd.set_option('display.max_rows', None)
print(covid)


# In[ ]:




# Work out the case delta between each row to generate a number of new cases per day as the second column

# In[124]:

test = covid["Total"]
print(test)


# In[ ]:




# UNKNOWN: Why is diff on a specific row (or on test) not working?
# The "I" column is an object, not an int - convert?

# In[125]:

test.diff()


# Convert dates into standard pandas data format

# In[126]:

covid['std-date'] = pd.to_datetime(covid["dates"], format='%d/%m/%Y')
print(covid)
covid.info()


# In[ ]:




# Need to sort by incrementing dates

# In[127]:

covid = covid.sort_values(by='std-date',ascending=True) 


# In[128]:

print(covid)


# In[129]:

#idx = np.where(df['y'].eq(0), df.index, 0).max()+1

# Temporary - drop the last day as it might be 0. Better to check if 0 and remove, but don't know how to do that!!
#covid = covid[:-1]


# Work out diffs; convert NaN to the original value and convert diff column to int
# TODO: Move diff column to column two

# In[130]:

covid["I"] = covid["Total"].diff().fillna(covid['Total']).astype(int)


# In[131]:

print(covid)


# In[132]:

covid.info()


# Swap cells to be in the correct organization for WHO-PAHO

# In[133]:

cols = list(covid.columns)
a, b = cols.index('Total'), cols.index('I')
cols[b], cols[a] = cols[a], cols[b]
covid = covid[cols]


# In[134]:

print(covid)


# We have a lot of dates with no data (at 0 total value) at the end of the dataset; drop these invalid data. 
# 
# TODO: We currently do it from a known end point, but we should look for where I goes negative (or we transition to 0) and drop all after this point

# In[135]:

#covid = covid.loc[0:276]
#print(covid)


# In[ ]:




# Remove the std-date column from the dataframe we write as CSV as it confused WHO-PAHO

# In[136]:

csv_covid = covid.drop(['std-date'], axis=1)


# In[137]:

csv_weekly_covid = csv_covid.tail(7)
csv_weekly_covid.to_csv(CSV_WEEKLY_PATH, header=False, index=False)


# In[ ]:




# In[138]:

csv_covid.to_csv(CSV_OUTPUT_PATH, header=True, index=False) 


# In[ ]:




# In[ ]:




# In[ ]:




# Display covid cases over time

# In[139]:

cases = covid.plot(x="std-date", y="Total", title=CITY + " Covid cumulative cases")
cases.figure.show()
cases.figure.savefig(CUMULATIVE_GRAPH_PATH)


# Show log y - change in growth over time

# In[140]:

lcases = covid.plot(x="std-date", y="Total",logy=True, title=CITY + " Covid (log) cumulative cases")
lcases.figure.show()
lcases.figure.savefig(CUMULATIVE_LOG_GRAPH_PATH)


# In[ ]:




# In[141]:

ax = covid.plot(x="std-date", y="I", kind="bar", figsize=(20,10), title=CITY + " Covid cases per day")

n = 10

ticks = ax.xaxis.get_ticklocs()
ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
ax.xaxis.set_ticks(ticks[::n])
ax.xaxis.set_ticklabels(ticklabels[::n])
ax.figure.tight_layout()

ax.figure.show()


# In[142]:

ax.figure.savefig(CASES_PER_DAY_GRAPH_PATH)


# Output some data as a JSON file

# In[147]:

import json

json_data = {}
val = int(csv_covid.tail(1)['Total'])
json_data['total_cases'] = val

# Parse JSON
with open(JSON_OUTPUT_PATH, 'w') as outfile:
    json.dump(json_data, outfile)

