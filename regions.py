"""
Checks each regional file for desired expocodes.

Maren Kjos Karlsen 2020.07.06
"""
import os
import pandas as pd
import csv
import re
import SOCAT_functions as SOCATf
SOCAT_synthesis_folder='/Users/rocio/Downloads/SOCATv2022_synthesis_files/'
YEAR = '2021'
#
# # To minimize memory-issues only the expocode and datetime information is fetched from the file
EXP_DATETIME_COLUMNS = [0,4,5,6,7,8,9] #[Expocode,yr,mon,day,hh,mm,ss]
FILE = SOCAT_synthesis_folder+'SOCATv2022.tsv'
_, df, _, _, _ = SOCATf.read_SOCAT(FILE,'str')

df=df['Expocode']

expocodes = df.values

all_files = os.listdir(SOCAT_synthesis_folder)
all_files=[SOCAT_synthesis_folder+f for f in all_files]
regional_files = list(filter(lambda file: SOCAT_synthesis_folder+'SOCATv2022_' in file, all_files))

regions={}
for reg_file in regional_files:
  region_camelcase = reg_file.split('_')[-1].split('.')[0]
  if region_camelcase =='FlagE': continue
  splitted = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', region_camelcase)).split()
  region = ' '.join(splitted)

  print(region)

  with open(reg_file) as file:
    content = file.read()
    for exp in expocodes:
      if(exp in content):
        if exp in regions.keys():
          regions[exp]+= '; ' + region
        else:
          regions[exp]=region

      # if(exp[0] in content):
      #   if exp[0] in regions.keys():
      #     regions[exp[0]]+= '; ' + region
      #   else:
      #     regions[exp[0]]=region

print(regions)

with open('regions.csv','w') as csv_file:
  writer = csv.writer(csv_file)
  for key, val in regions.items():
    print(key)
    writer.writerow([key, val])