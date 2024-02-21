# Author: Michael Fashola
# Description: Step 1 of a 2-step series scrape diagnosis and treatment data from Mayo Clinic

import string
import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from random import randint

# All letters
letters = list(string.ascii_uppercase)
# letters = ["V"]

base_url = 'https://www.mayoclinic.org'


diseases = []
diseases_count = 0
diagnoses_count = 0

# Get the links for the diseases, and the disease names
for letter in letters:
  print("Processing {}".format(letter))
  diagnosis_links = []
  content_list = []
  df = pd.read_json("pages/base_{}.json".format(letter))
  this_df = df[df['name'].str.startswith(letter)]
  for ix, row in this_df.iterrows():
    disease_name = row['name']
    print("Fetching diagnoses link for {}".format(disease_name))
    response = requests.get(row['href'])
    # response.raise_for_status()
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    possible_link = soup.find("a", {"id": "et_genericNavigation_diagnosis-treatment"})
    if possible_link != None:
      link = possible_link["href"]
      print("Potential link is: {}".format(link))
      if "/diseases-conditions/" in link and "/diagnosis-treatment/" in link:
        diagnosis_links.append({"diagnosis_url": base_url + link, "disease_name": disease_name})
      # print("diagnosis links found for {} is {}".format(disease_name, len(diagnosis_links)))
      sleep(randint(1,5))

  # Clean up the link list
  ndf = pd.DataFrame.from_records(diagnosis_links)
  ndf.to_csv("results/diagnosis_link_{}.tsv".format(letter), sep="\t")