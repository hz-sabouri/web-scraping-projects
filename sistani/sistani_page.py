import requests
from bs4 import BeautifulSoup
import re
import csv
from urllib.parse import urljoin

first_url =['https://www.sistani.org/persian/book/26578/',
            'https://www.sistani.org/persian/book/26577/',
            'https://www.sistani.org/persian/book/26576/',
            'https://www.sistani.org/persian/book/26575/',
            'https://www.sistani.org/persian/book/25936/',
            'https://www.sistani.org/persian/book/51/',
            'https://www.sistani.org/persian/book/52/']
urls = []
for url in first_url:
    r = requests.get(url)
    soup = BeautifulSoup(r.text,features='html.parser')
    heders = soup.find_all('a',href =re.compile(r'^(/persian)/(book)/\d*/\d*/'))

    for h in heders:
        urls.append(urljoin(url,h['href']))
        
with open('sistani_urls.csv', 'w', encoding='utf8', newline='') as sistani:
    writer = csv.writer(sistani)
    for i in urls:
        writer.writerow([i])