import requests
from bs4 import BeautifulSoup
import json
import re

urls = []
with open('sistani_qa_urls.csv', 'r', encoding='utf8') as f:
    for line in f:
        line = line.strip()
        if line:
            urls.append(line)

BAD_UNICODE_CHARS = [
    '\u200f', '\u200e',
    '\u202a', '\u202b', '\u202c',
    '\u2066', '\u2067', '\u2068', '\u2069',
]

def clean_text(text: str) -> str:
    if not text:
        return ''
    for ch in BAD_UNICODE_CHARS:
        text = text.replace(ch, ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip(' ":\n')

all_data = []

for idx, url in enumerate(urls, start=1):
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')

        qa_blocks = soup.select('div.one-qa')
        url_count = 0

        for block in qa_blocks:
            q_label = block.find('span', class_='nvy b')
            question_text = ''
            if q_label:
                raw_q = q_label.find_next_sibling(string=True)
                question_text = clean_text(raw_q)

            answer_div = block.find('div', class_='b')
            answer_text = ''
            if answer_div:
                answer_text = clean_text(
                    answer_div.get_text(separator=' ', strip=True)
                )

            if question_text and answer_text:
                all_data.append({
                    "text": answer_text,
                    "questions": [
                        {
                            "text": question_text
                        }
                    ]
                })
                url_count += 1

        print(f"✅ URL {idx}/{len(urls)} OK → {url_count} پرسش و پاسخ | {url}")

    except Exception as e:
        print(f"❌ URL {idx}/{len(urls)} FAIL → {url}")
        print(f"   ⤷ Error: {e}")

with open('sistani_qa_data.json', 'w', encoding='utf8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)

print(f"\n📦 مجموع کل پرسش و پاسخ‌ها: {len(all_data)}")
print("✔ فایل sistani_qa_data.json با موفقیت ساخته شد.")
