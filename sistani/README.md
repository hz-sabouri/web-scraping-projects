# Sistani scraper

A multi-step scraper that collects the Persian-language **books** and **Q&A** sections of [sistani.org](https://www.sistani.org/persian/) and converts them into one JSON dataset of question/answer records.

## Pipeline

Each step writes a file that the next step reads.

| Step | Script | Reads | Writes |
|---|---|---|---|
| 1 | `sistani_page.py` | a list of book index pages (hard-coded) | `sistani_urls.csv` (chapter URLs) |
| 2 | `sistani_data.py` | `sistani_urls.csv` | `sistani_data.json` |
| 3 | `sistani_qa_urls.py` | the Q&A index page | `sistani_qa_urls.csv` (category URLs) |
| 4 | `sistani_qa_data.py` | `sistani_qa_urls.csv` | `sistani_qa_data.json` |
| 5 | `sistani_merged.py` | both JSON files | `sistani_all.json` |

## Output format

```json
[
  {
    "text": "the answer or book passage (plus footnotes, when present)",
    "questions": [
      { "text": "the question or section title" }
    ]
  }
]
```

For book chapters the page heading is used as the question and the chapter body as the text. For the Q&A section each question/answer pair becomes one record.

## What the scripts handle

- HTML parsing with BeautifulSoup (CSS selectors for chapter text, footnotes and Q&A blocks)
- Cleaning of invisible bidirectional Unicode control characters and whitespace normalisation, which matters for Persian text
- Request timeouts, HTTP error checks and per-URL error handling in the Q&A scraper, so one failing page does not stop the run
- Relative-to-absolute URL resolution with `urljoin`

## Run

```bash
pip install -r requirements.txt

python sistani_page.py
python sistani_data.py
python sistani_qa_urls.py
python sistani_qa_data.py
python sistani_merged.py
```

Run the scripts from inside this folder, because the CSV and JSON files are read and written in the current directory.

## Notes

- There is no rate limiting between requests. Add a short delay if you scale this up, and check the site's terms before scraping.
- Generated files are excluded from the repository (see `.gitignore`).

## Tech

Python, `requests`, `BeautifulSoup4`, `csv`, `json`, `re`
