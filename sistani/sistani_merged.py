import json

with open('sistani_data.json', 'r', encoding='utf-8') as f:
    data1 = json.load(f)

with open('sistani_qa_data.json', 'r', encoding='utf-8') as f:
    data2 = json.load(f)

merged = data1 + data2 

with open('sistani_all.json', 'w', encoding='utf-8') as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)
