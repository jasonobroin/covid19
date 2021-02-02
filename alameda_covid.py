
# coding: utf-8

# TODO: Read data as JSON directly from https://services5.arcgis.com/ROBnTHSNjoZ2Wm1P/arcgis/rest/services/COVID_19_Statistics/FeatureServer/3/query?where=1%3D1&outFields=dtcreate,Alameda,GlobalID,OBJECTID&outSR=4326&f=json and then transform to csv

# Now we have a CSV format - load it (this can be elided if we load and transform the JSON directly
# 
# TODO: Rename "I" to "Total Cases"

# In[487]:

import os

#LOCAL_DATA_ROOT = "/Users/jason/development/cv19/"
LOCAL_DATA_ROOT = "./"
CSV_FILE = "alameda_data.csv"
CSV_OUTPUT_FILE = "alameda_delta_data.csv"

CASES_PER_DAY_GRAPH_FILE = "alameda_daily_cases.png"

CSV_PATH = os.path.join(LOCAL_DATA_ROOT, CSV_FILE)
CSV_OUTPUT_PATH = os.path.join(LOCAL_DATA_ROOT, CSV_OUTPUT_FILE)
CASES_PER_DAY_GRAPH_PATH = os.path.join(LOCAL_DATA_ROOT, CASES_PER_DAY_GRAPH_FILE)

get_ipython().magic(u'matplotlib auto')
import pandas as pd

def load_covid_data(csv_path=CSV_PATH):
    return pd.read_csv(csv_path)


# In[ ]:




# In[488]:

covid = load_covid_data()
covid.head()


# In[489]:

covid.info()


# Clean up the data - replace NaN with 0; replace <10 with 0

# In[490]:

covid["Total"].fillna(0,inplace=True)
covid["Total"].replace("<10", 0,inplace=True)


# Convert I field from an object (as it originally had strings) to an int

# In[491]:

covid["Total"] = covid["Total"].astype(str).astype(int)


# In[ ]:




# In[492]:

covid.info()


# In[ ]:




# In[493]:

covid.head()


# In[ ]:




# In[494]:

pd.set_option('display.max_rows', None)
print(covid)


# In[ ]:




# Work out the case delta between each row to generate a number of new cases per day as the second column

# In[495]:

test = covid["Total"]
print(test)


# In[ ]:




# UNKNOWN: Why is diff on a specific row (or on test) not working?
# The "I" column is an object, not an int - convert?

# In[496]:

test.diff()


# Convert dates into standard pandas data format

# In[497]:

covid['std-date'] = pd.to_datetime(covid["dates"], format='%d/%m/%Y')
print(covid)
covid.info()


# In[ ]:




# Need to sort by incrementing dates

# In[498]:

covid = covid.sort_values(by='std-date',ascending=True) 


# In[499]:

print(covid)


# In[ ]:




# Work out diffs; convert NaN to the original value and convert diff column to int
# TODO: Move diff column to column two

# In[500]:

covid["I"] = covid["Total"].diff().fillna(covid['Total']).astype(int)


# In[501]:

print(covid)


# In[502]:

covid.info()


# Swap cells to be in the correct organization for WHO-PAHO

# In[503]:

cols = list(covid.columns)
a, b = cols.index('Total'), cols.index('I')
cols[b], cols[a] = cols[a], cols[b]
covid = covid[cols]


# In[504]:

print(covid)


# We have a lot of dates with no data (at 0 total value) at the end of the dataset; drop these invalid data. 
# 
# TODO: We currently do it from a known end point, but we should look for where I goes negative (or we transition to 0) and drop all after this point

# In[505]:

#covid = covid.loc[0:276]
#print(covid)


# In[ ]:




# Remove the std-date column from the dataframe we write as CSV as it confused WHO-PAHO

# In[506]:

csv_covid = covid.drop(['std-date'], axis=1)


# In[507]:

csv_covid.to_csv(CSV_OUTPUT_PATH, header=True, index=False) 


# In[ ]:




# Display Alameda covid cases over time

# In[508]:

covid.plot(x="std-date", y="Total", title="Alameda Covid cumulative cases")


# Show log y - change in growth over time

# In[ ]:

covid.plot(x="std-date", y="Total",logy=True)


# In[ ]:




# In[ ]:

ax = covid.plot(x="std-date", y="I", kind="bar", figsize=(20,10), title="Alameda Covid cases per day")

n = 10

ticks = ax.xaxis.get_ticklocs()
ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
ax.xaxis.set_ticks(ticks[::n])
ax.xaxis.set_ticklabels(ticklabels[::n])
ax.figure.tight_layout()

ax.figure.show()


# In[ ]:

ax.figure.savefig(CASES_PER_DAY_GRAPH_PATH)


# In[ ]:



