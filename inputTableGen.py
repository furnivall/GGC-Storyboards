'''
This file generates template table input text files for each sector, which can be edited. They will inform the
storyboard targets table.
'''

import os
import pandas as pd
from shutil import copyfile

# read staff download to populate list of sectors
df = pd.read_excel('W:/Staff Downloads/2020-04 - Staff Download.xlsx')

# get list of sectors
sectors = df['Sector/Directorate/HSCP'].unique()

# get current month
current_month = pd.Timestamp.now().strftime("%B-%Y")

# build dir if it doesn't exist
working_dir = 'C:/storyboards/'+current_month
if not os.path.isdir(working_dir):
    os.mkdir(working_dir)

# copy template file for each sector in list of sectors
template_file = 'C:/storyboards/template.txt'
for i in sectors:
    copyfile(template_file, working_dir+'/'+i+'.txt')

print(str(len(sectors))+" templates generated in "+working_dir)



