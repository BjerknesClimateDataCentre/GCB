"""
Checks each regional file for desired expocodes.

Maren Kjos Karlsen 2020.07.06
"""
import os
import pandas as pd
import csv
import re

FILE ='SOCATv2020.tsv'
END_OF_METADATA=4
END_OF_HEADER=6301
START_OF_DATA=6363

df = pd.read_csv(FILE, sep='\t',skiprows=END_OF_METADATA, nrows=END_OF_HEADER,dtype=str,usecols=['Expocode'])
expocodes = df.values

all_files = os.listdir('.')
regional_files = list(filter(lambda file: 'SOCATv2020_' in file, all_files))

regions={}
for reg_file in regional_files:
  region_camelcase = reg_file.split('_')[-1].split('.')[0]
  splitted = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', region_camelcase)).split()
  region = ' '.join(splitted)


  print(region)

  with open(reg_file) as file:
    content = file.read()
    for exp in expocodes:
      if(exp[0] in content):
        if exp[0] in regions.keys():
          regions[exp[0]]+= '; ' + region
        else:
          regions[exp[0]]=region

print(regions)

with open('regions.csv','w') as csv_file:
  writer = csv.writer(csv_file)
  for key, val in regions.items():
    print(key)
    writer.writerow([key, val])