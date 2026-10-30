import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

base_url = 'https://www.sistani.org'
url = 'https://www.sistani.org/persian/qa/'

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

urls = []

qa_trees = soup.find_all('div', class_='qa-tree')

for tree in qa_trees:
    links = tree.find_all('a')
    for a in links:
        href = a.get('href')
        if href:
            full_url = urljoin(base_url, href)
            urls.append(full_url)

with open('sistani_qa_urls.csv', 'w', encoding='utf8') as f:
    for u in urls:
        f.write(u + '\n')
