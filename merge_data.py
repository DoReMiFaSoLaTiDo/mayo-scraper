# Author: Michael Fashola
# Description: Merge all the extracted data into single datasheet 

import pandas as pd
import json
import glob

# List of json files
json_files = glob.glob('pages/base_*.json')

# initial list
master_list = []

# Loop through all json files
for file in json_files:
  # Load json file data into a pandas dataframe
  df = pd.read_json(file)
  # Append the dataframe to the master list
  master_list.append(df)

# Set 'name' column as index
master_df = pd.concat(master_list, axis=0, ignore_index=True)

# remove 'href' column and drop duplicate disease names from merged data
master_df = master_df.drop('href', axis=1)
master_df = master_df.drop_duplicates()
master_df.set_index('name', inplace=True)

# Add symptoms and treatment columns to pandas dataframe
master_df['symptoms'] = None
master_df['treatment'] = None

symptoms_files = glob.glob('results/disease_data_*.json')  # List of symptoms data files

for symptoms_file in symptoms_files:
  with open(symptoms_file, 'r') as file:
    data = json.load(file)
    for item in data:
      disease_name = item.get('name')
      content = item.get('content')

      # Check if disease name corresponds and content is not null
      if disease_name and content and master_df.loc[disease_name, 'symptoms'] == None:
        master_df.loc[disease_name, 'symptoms'] = content

print(master_df.head(5))
treatment_files = glob.glob('results/treatments_data_*.json')  # List of treatment data files

for treatment_file in treatment_files:
  with open(treatment_file, 'r') as file:
    data = json.load(file)
    for item in data:
      disease_name = item.get('disease_name')
      content = item.get('treatment')

      # Check if disease name corresponds and content is not null
      if disease_name != None and content != None and master_df.loc[disease_name, 'treatment'] == None:
          master_df.loc[disease_name, 'treatment'] = content

master_df.reset_index(inplace=True)
master_df.to_json("results/main.json", orient="records", force_ascii=False)