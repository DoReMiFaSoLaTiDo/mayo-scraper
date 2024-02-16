# Author: Michael Fashola
# About: This code is similar to main.py but works with an existing file to fetch
#         the necessary data from Mayo Clinic with less clean-up required afterwards.

import string
import requests
import pandas  as pd
from bs4 import BeautifulSoup
from time import sleep
from random import randint

# All letters
letters = list(string.ascii_uppercase)

# Scrape disease content pages
for letter in letters:
    content_list = []
    df = pd.read_json("pages/base_{}.json".format(letter))
    for ix, row in df.iterrows():
        if row["name"].startswith(letter):
            print("Fetching content for {}".format(row["name"]))
            response = requests.get(row["href"])
            soup = BeautifulSoup(response.text, 'html.parser')
            nodeList = soup.find_all("div", "row")
            if (len(nodeList) >= 3):
                content_list.append(nodeList[3].get_text())
            else:
                content_list.append(None)
            sleep(randint(1,5))
        else:
            content_list.append(None)

    # Output final file for letter
    df["content"] = content_list
    df.to_json("results/disease_data_{}.json".format(letter), orient="records", force_ascii=False)
