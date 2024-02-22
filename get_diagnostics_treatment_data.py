import requests
import string
import pandas as pd
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from random import randint

# All letters
letters = list(string.ascii_uppercase)
# letters = ["Z"]

for letter in letters:
  print('Printing Letter {}'.format(letter))
  # Read the TSV file
  data = pd.read_csv("results/diagnosis_link_{}.tsv".format(letter), sep='\t')
  df = pd.DataFrame(data, columns=['diagnosis_url', 'disease_name'])

  # Initialize an empty list to hold the content
  content_list = []

  # Loop through each url in the data
  for ix, row in df.iterrows():
    diseaseName = row['disease_name']
    # Send a request to the url
    response = requests.get(row['diagnosis_url'])

    # Parse the response text with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the 'content' class and get the inner text
    found = soup.find(class_='content')
    if found:
      content = found.get_text()
      if (len(content) > 1 ):
        print('Got content for {}'.format(diseaseName))
        # Append the content to the list
        content_list.append(content)
      else:
        print('Ba shishi for {}'.format(diseaseName))
        content_list.append(None)
    else:
      print('Endpoint likely forbidden for {}'.format(diseaseName))
      content_list.append(None)

    sleep(randint(1,5))

  # Create a DataFrame from the list
  df["treatment"] = content_list

  # Save the DataFrame to a JSON file
  df.to_json("results/treatments_data_{}.json".format(letter), orient='records')