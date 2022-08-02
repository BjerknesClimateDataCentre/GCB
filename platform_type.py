"""
Fetches unique platforms and associated platform type from GCB 2018 and writes them to platform_type.csv

Maren Kjos Karlsen 2020.07.06
"""
# Better to use the CMEMS summary file or the platform one. It's more complete

import pandas as pd

df = pd.read_csv('/Users/rocio/Downloads/GCB2019_Datasets.csv',usecols=['Platform','Platform type','Expocode'])

df['Prefix'] = df['Expocode'].str[0:4]

platforms = df.groupby('Platform').min()
platforms = platforms.drop('Expocode',axis=1)
platforms['Name'] = platforms.index

platforms = platforms[['Prefix','Name','Platform type']]
platforms.to_csv('platform_type.csv',index=False)
