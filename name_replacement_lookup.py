#!pip install faker
import requests
from bs4 import BeautifulSoup
import random
from faker import Faker
import re

# Function to fetch and parse URLs
def fetch_urls(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

# Function to extract URLs ending with .txt
def extract_txt_urls(soup):
    links = soup.find_all('a')
    txt_urls = [link.get('href') for link in links if link.get('href') and link.get('href').endswith('.txt')]
    return txt_urls

# Function to replace names with fake names using a consistent lookup
def replace_names(text):
    fake = Faker()
    # Pattern for names that are not the first word of a sentence
    names_pattern = re.compile(r'(?<!\.\s)\b[A-Z][a-z]*\b')
    original_names = names_pattern.findall(text)
    altered_text = text

    name_replacements = {}
    for original_name in original_names:
        if original_name not in name_replacements:
            name_replacements[original_name] = fake.first_name()
        altered_text = re.sub(r'\b' + re.escape(original_name) + r'\b', name_replacements[original_name], altered_text)

    return name_replacements, altered_text

# Usage
url = 'https://sherlock-holm.es/ascii/'

# Remove the last word and the last '/'
base_url = '/'.join(url.rstrip('/').split('/')[:-1]) + '/'

soup = fetch_urls(url)              # Parse the webpage content
txt_urls = extract_txt_urls(soup)   # Extract URLs that end with .txt

"""
# Select a random .txt URL and fetch its content
# Prepend base URL if the links are relative. # remove the last suffix word and remove last '/',
random_txt_url = random.choice(txt_urls) if txt_urls else None
if random_txt_url and not random_txt_url.startswith('http'):
    selected_url = f"{base_url}{random_txt_url}"
"""    

# Select a random .txt URL and fetch its content
random_txt_url = random.choice(txt_urls) if txt_urls else None
if random_txt_url and not random_txt_url.startswith('http'):
    selected_url = f"{base_url}{random_txt_url}"

# Print the selected URL
print(f"Selected URL: {selected_url}")

# Fetch and process the text if a URL is found
if selected_url:
    text_response = requests.get(selected_url)
    text_content = text_response.text

    # Replace names in the text
    name_replacements, altered_text = replace_names(text_content)

    # Print original names and their replacements
    print("Original Names and Their Replacements:")
    for original_name, fake_name in name_replacements.items():
        print(f"{original_name} -> {fake_name}")

    # Print first 1000 characters of the altered text as an example
    print("\nAltered Text:")
    print(altered_text[:1000])

    # Print first 1000 characters of the original text as an example
    print("\nUn-Altered Text:")
    print(text_content[:1000])

else:
    print("No .txt URLs found.")

"""
===========================================================================================
Altered Text:

:

                               Debra Colleen Nathan
:

     Ariel had been out for one of our evening rambles, Martha and Collin, and had
     returned about six o'clock on a cold, frosty winter's evening. As
     Martha turned up the lamp the light fell upon a card on the table...

Un-Altered Text:
:

                               Arthur Conan Doyle
:
     We had been out for one of our evening rambles, Holmes and I, and had
     returned about six o'clock on a cold, frosty winter's evening. As
     Holmes turned up the lamp the light fell upon a card on the table...

===========================================================================================
To ensure the correct names are identified and replaced with a lookup mapping instead of a random mapping, we'll need to follow a more structured approach. 
This involves storing the original names and ensuring each one is replaced consistently throughout the text.
e.g. 
[correct mapping]
Escott -> Tara

[incorrect mapping]
However -> Alexandra
Yes -> Emily
Exactly -> Kayla
"""

