import string
import requests
import pandas
from bs4 import BeautifulSoup
from time import sleep
from random import randint

# All letters
letters = list(string.ascii_uppercase)
# letters = ["Z"]

base_url = 'https://www.mayoclinic.org/diseases-conditions/index?letter={}'

diseases = []
# Get the links for the diseases, and the disease names
for letter in letters:
    print("Processing {}".format(letter))
    response = requests.get(base_url.format(letter))
    response.raise_for_status()
    content = response.text
    soup = BeautifulSoup(content)
    possible_links = soup.find_all("div", {"class": "cmp-link"})
    for ix, link in enumerate(possible_links):
        print("Processing link {} or {}".format(ix+1, len(possible_links)))
        disease_url = link.find("a")["href"]
        if "/diseases-conditions/" in disease_url and "index?letter=" not in disease_url and not disease_url.endswith("/index"):
            diseases.append({"disease_url": disease_url, "disease_name": link.text})

# Clean up the link list
df = pandas.DataFrame.from_records(diseases)
df = df.drop_duplicates()

# Scrape disease content pages
content_list = []
for ix, row in df.iterrows():
    print("Fetching content for {}".format(row["disease_name"]))
    response = requests.get(row["disease_url"])
    soup = BeautifulSoup(response.text)
    content = soup.get_text()
    content_list.append(content)
    sleep(randint(1,5))

# Output final file
df["content"] = content_list
df.to_csv("disease_data.tsv", sep="\t")
