# Author: Michael Fashola
# Description: This fetches diagnosis and treatment data from Mayo Clinic

import string
import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from random import randint

# All letters
# letters = list(string.ascii_uppercase)
letters = ["Y"]

base_url = 'https://www.mayoclinic.org'

diagnosis_links = []
diseases = []
diseases_count = 0
diagnoses_count = 0

# Get the links for the diseases, and the disease names
for letter in letters:
  print("Processing {}".format(letter))
  content_list = []
  df = pd.read_json("pages/base_{}.json".format(letter))
  this_df = df[df['name'].str.startswith(letter)]
  for ix, row in this_df.iterrows():
    diseases_count += 1
    disease_name = row['name']
    print("Fetching diagnoses link for {}".format(disease_name))
    response = requests.get(row['href'])
    response.raise_for_status()
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    possible_links = soup.find_all("a", {"id": "et_genericNavigation_diagnosis-treatment"})
    for ix, element in enumerate(possible_links):
      link = element["href"]
      print("Processing link {} of {}".format(ix+1, len(possible_links)))
      print("Potential link is: {}", link)
      if "/diseases-conditions/" in link and "/diagnosis-treatment/" in link:
          diagnosis_links.append({"diagnosis_url": base_url + link, "disease_name": disease_name})

    sleep(randint(1,5))

# Clean up the link list
ndf = pd.DataFrame.from_records(diagnosis_links)
ndf = ndf.drop_duplicates()

# Scrape disease content pages
content_list = []
for ix, row in ndf.iterrows():
  diagnoses_count += 1
  print("Fetching diagnoses for {}".format(row["disease_name"]))
  response = requests.get(row["diagnosis_url"])
  soup = BeautifulSoup(response.text, 'html.parser')
  nodeList = soup.find_all("div", "content")
  if (len(nodeList) >= 1):
    content_list.append(nodeList[0].get_text())
  else:
    content_list.append(None)

  sleep(randint(1,5))

# Output final file
ndf["diagnosis_and_treatment"] = content_list
ndf.to_json("diagnosis_data_{}.json".format(letter), orient="records", force_ascii=False)

print("Letter: {}; Diseases: {}; Diagnosis: {}".format(letter, diseases_count, diagnoses_count))