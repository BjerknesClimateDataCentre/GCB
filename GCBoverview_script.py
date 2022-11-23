"""
Builds the Global Carbon Budget SOCAT overview.
A tsv file containing:
<Platform    Start Datetime  End Datetime    Region  No. of samples (in XXXX)    Principal Investigator  DOI (if available)  QC flag Platform type   Days    Expocode>

The majority of information is fetched from the complete collection. Region is fetched from regional files, platform type is fetched from a separate file assembled from previous years and added to as needed.

Data is fetched from https://www.socat.info/index.php/data-access/
Last accessed 2020.07.06

Requires:
Global and regional synthesis SOCAT files
A previous version of the GCB for platform-type retrieval

Order of operations:
- Regions.py and platform_type.py must be run prior to this script.
 * Regions.py takes a long time to run. An hour+. Plan accordingly.

- When regions.csv and platform_type.csv is created this script can be run.

- The platform type is set to 'None' for all new/unknown platforms. Go through GCB.csv and identify all new platforms (where platform-type is missing), add them to the platform_type.csv with prefix, name and type, and run this main script again.

- Check the final GCB.csv and identify if any work needs to be done with regards to the DOIs. Remove 'None'-entries if that is preferred. 


Maren Kjos Karlsen 2020-07-08
"""


import pandas as pd
import datetime as dt
import SOCAT_functions as SOCATf

# # Global variables, end of header and start of data will change from year to year
# FILE ='SOCATv2020.tsv'
#END_OF_METADATA=4
#END_OF_HEADER=6301
# START_OF_DATA=6363
YEAR = '2021'
#
# # To minimize memory-issues only the expocode and datetime information is fetched from the file
EXP_DATETIME_COLUMNS = [0,4,5,6,7,8,9] #[Expocode,yr,mon,day,hh,mm,ss]
FILE = '/Users/rocio/Downloads/SOCATv2022_synthesis_files/SOCATv2022.tsv'

### Extracting data content

# Maren set up the data types to be all read as string (the default is 0,2 str, rest float)
# Change in the future?
dd, df, _, _, _ = SOCATf.read_SOCAT(FILE, 'str')

dd=dd.iloc[:,EXP_DATETIME_COLUMNS]
print(dd.columns)

## Reduce dataframe to entries from YEAR (Use only 2019 data)   
dd = dd.loc[(dd['yr'] == YEAR)]

## Collect datetime columns to single column
dd['DT'] = dd['yr'] + ' ' + dd['mon']+ ' ' + dd['day']+ ' ' + dd['hh']+ ' ' + dd['mm']+ ' ' + dd['ss']
dd['DT'] = pd.to_datetime(dd['DT'],format='%Y %m %d %H %M %S.')
dd = dd.drop(['yr','mon','day','hh','mm','ss'],axis=1)


# Groupby is a pandas function that collapses the dataframe. For all entries with *expocode* show the minimum value, number of values, etc. 

# First and last datetime per expocode/cruise 
start_date = dd.groupby("Expocode").min()
end_date = dd.groupby("Expocode").max()

#Number of measurements per cruise
num_per_cruise = dd.groupby("Expocode").count()

#Number of days per cruise
num_per_days = dd.groupby(['Expocode',dd['DT'].dt.date]).count() # number of measurements per days, counting the number of these counts gives number of days.
days_per_cruise = num_per_days.groupby(['Expocode']).count()



### Extracting list of datasets
#df = pd.read_csv(FILE, sep='\t', dtype=str, skiprows=END_OF_METADATA, nrows=END_OF_HEADER)
#print(df.columns)

# The Start/End time below is the leave/arrive at port date. These do not contain any time-information. 
# These dates are used to extract cruises starting and/or ending in 2019. They will not be part of the final list. 
# The min/max date from the data-extraction is the date and time of the first/last measurement, and is what is used for the GCB list

df['Start Time']=pd.to_datetime(df['Start Time'])
df['End Time']=pd.to_datetime(df['End Time'])
df['Start year']=df['Start Time'].dt.year
df['End year']=df['End Time'].dt.year
print(df.columns)

# Reducing dataframe to 2019-data only
df = df.loc[(df['Start year'] == int(YEAR)) | (df['End year'] == int(YEAR))]
df = df.drop(['Start year','Start Time','End year','End Time','Dataset Name','version'],axis=1) 


# The index of the groupby dataframes are set to the expocode. Setting the index of the main dataframe to the Expocode prior to concatenating.
df = df.set_index('Expocode')

# Add day-count, measurement-count and start/end-date to list of dataset
df = pd.concat([df,days_per_cruise],join='inner',axis=1)
print(df.head)
df = df.rename(columns={'DT':'Number of days per cruise'}) # The concat function names the new column 'DT', probably an easier fix, but renaming for now.

df = pd.concat([df,num_per_cruise],join='inner',axis=1)
df = df.rename(columns={'DT':'Number of measurements per cruise'})

df = pd.concat([df,start_date],join='inner',axis=1)
df = df.rename(columns={'DT':'Start Datetime'})

df = pd.concat([df,end_date],join='inner',axis=1)
df = df.rename(columns={'DT':'End Datetime'})


#### 
# Add columns
df['Expocode'] = df.index  # Setting the expocode as the index removes the ability to do column operations on the expocode. Therefore a new column is added

# split expocode, add prefix as separate column. Platformtype is using the prefix only to apply to all entries of a particular ship. data is merged on prefix
df['Prefix'] = df['Expocode'].str[0:4]
 
platform_type = pd.read_csv('platform_type.csv',usecols=['Prefix','Platform type']) 
df = df.merge(platform_type,on='Prefix',how='left')

region = pd.read_csv('regions.csv',names=['Expocode','Region'])
df = df.merge(region,on='Expocode',how='left')

#Reorder columns to preferred output
df = df[['Platform Name','Start Datetime','End Datetime','Region','Number of measurements per cruise','PI(s)','Data Source Reference','QC Flag','Platform type','Number of days per cruise','Expocode']]

# write to csv, do not include index, set missing information as None to easily identify missing information.
df.to_csv('GCB.csv',index=False,na_rep='None')
