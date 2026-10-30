
import requests
from bs4 import BeautifulSoup
import json
import re

BAD_UNICODE_CHARS = [
    '\u200f', '\u200e',
    '\u202a', '\u202b', '\u202c',
    '\u2066', '\u2067', '\u2068', '\u2069',
]

BAD_STRING_PATTERNS = [
    r'\\u200f',        
    r'\[U\+200F\]',   
]

def clean_text(text: str) -> str:
    if not text:
        return ''

    for ch in BAD_UNICODE_CHARS:
        text = text.replace(ch, ' ')

    for pattern in BAD_STRING_PATTERNS:
        text = re.sub(pattern, ' ', text, flags=re.IGNORECASE)


    text = ' '.join(text.split())
    return text

urls = []
with open('sistani_urls.csv', 'r', encoding='utf8') as f:
    for line in f:
        line = line.strip()
        if line:
            urls.append(line)

final_data = []
for url in urls:
    r = requests.get(url, timeout=15)
    soup = BeautifulSoup(r.text, features='html.parser')

    heder_tag = soup.find('h1', class_='c')
    heder_text = clean_text(heder_tag.get_text(strip=True)) if heder_tag else ''

    text_tag = soup.select('div.baz.book-text')
    text = clean_text(
        text_tag[0].get_text(separator=' ', strip=True)
    ) if text_tag else ''

    footnote_tag = soup.select('div.baz.book-footnote')
    footnote = clean_text(
        footnote_tag[0].get_text(separator=' ', strip=True)
    ) if footnote_tag else ''

    combined_text = text
    if footnote:
        combined_text += "\n" + footnote

    final_data.append({
        "text": combined_text,
        "questions": [
            {
                "text": heder_text
            }
        ]
    })

    print(f"OK: {url}")
    print("-" * 80)

with open('sistani_data.json', 'w', encoding='utf8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=4)
print("✔ تمام URLها پردازش و در فایل sistani_data.json ذخیره شدند.")


"""#خروجی تکست
import requests
from bs4 import BeautifulSoup
import re

BAD_UNICODE_CHARS = [
    '\u200f', '\u200e',
    '\u202a', '\u202b', '\u202c',
    '\u2066', '\u2067', '\u2068', '\u2069',
]

BAD_STRING_PATTERNS = [
    r'\\u200f',
    r'\[U\+200F\]',
]

urls = []
with open('sistani_urls.csv', 'r', encoding='utf8') as f:
    for line in f:
        urls.append(line.strip())

with open('sistani_data.txt', 'w', encoding='utf8') as out:

    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, features='html.parser')

        heder_tag = soup.find('h1', class_='c')
        heder_text = heder_tag.get_text(strip=True) if heder_tag else ''

        text_tag = soup.select('div.baz.book-text')
        text = text_tag[0].get_text(separator=' ', strip=True) if text_tag else ''

        footnote_tag = soup.select('div.baz.book-footnote')
        footnote = footnote_tag[0].get_text(separator=' ', strip=True) if footnote_tag else ''

        for bad_char in BAD_UNICODE_CHARS:
            heder_text = heder_text.replace(bad_char, ' ')
            text = text.replace(bad_char, ' ')
            footnote = footnote.replace(bad_char, ' ')

        for pattern in BAD_STRING_PATTERNS:
            heder_text = re.sub(pattern, ' ', heder_text)
            text = re.sub(pattern, ' ', text)
            footnote = re.sub(pattern, ' ', footnote)

        
        out.write(f"question:\n{heder_text}\n\n")
        out.write(f"answer:\n{text}\n\n")
        if footnote:
            out.write(f"FOOTNOTE:\n{footnote}\n\n")
        out.write("\n\n")

        print(url)
        print("_" * 100)

print("تمام URL ها در فایل متنی ذخیره شدند!")
"""

"""import requests
from bs4 import BeautifulSoup
import json

urls = []
with open('sistani_urls.csv', 'r', encoding='utf8') as f:
    for line in f:
        urls.append(line.strip())

data = []

for url in urls:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features='html.parser')

    # استخراج هدر
    heder_tag = soup.find('h1', class_='c')
    heder_text = heder_tag.get_text(strip=True) if heder_tag else ''

    # استخراج متن
    text_tag = soup.select('div.baz.book-text')
    text = text_tag[0].get_text(separator=' ', strip=True) if text_tag else ''

    # استخراج پاورقی
    footnote_tag = soup.select('div.baz.book-footnote')
    footnote = footnote_tag[0].get_text(separator=' ', strip=True) if footnote_tag else ''

    # اضافه کردن به لیست داده‌ها
    data.append({
        'Header': heder_text,
        'Text': text,
        'Footnote': footnote
    })
    print(url)
    print("_"*100)

# ذخیره به صورت JSON
with open('sistani_data.json', 'w', encoding='utf8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("تمام URL ها در JSON ذخیره شدند!")
"""



"""import csv
import requests
from bs4 import BeautifulSoup

urls = []
with open('sistani_urls.csv', 'r', encoding='utf8') as f:
    reader = csv.reader(f)
    for row in reader:
        urls.append(row[0])

with open('sistani_data.csv', 'w', encoding='utf8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['Header', 'Text', 'Footnote'])
    writer.writeheader()

for url in urls:
    r = requests.get(url)
    soup = BeautifulSoup(r.text,features='html.parser')
    heder = soup.find('h1',class_='c')
    heders = [h.get_text(strip=True) for h in heder]
    heders =heders[0]

    text = soup.select('div.baz.book-text')
    text = text[0].text
    text = text.replace('\n', ' ').replace('\r', ' ').strip() if text else ''
    footnote = soup.select('div.baz.book-footnote')
    footnote = footnote[0].text
    footnote = footnote.replace('\n', ' ').replace('\r', ' ').strip() if footnote else ''
    with open('sistani_data.csv', 'a', encoding='utf8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Header', 'Text', 'Footnote'],quoting=csv.QUOTE_ALL)
        writer.writerow({
            'Header': heders,
            'Text': text,
            'Footnote': footnote
        })

print("تمام URL ها در CSV ذخیره شدند!")


print("CSV ساخته شد!")
"""