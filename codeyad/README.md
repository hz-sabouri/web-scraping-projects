# Codeyad scrapers

Two small practice scrapers that read the public JSON API behind the course listing of [codeyad.com](https://codeyad.com/), without parsing any HTML.

| Script | What it does | Output |
|---|---|---|
| `codeyad_info.py` | Walks through the first 3 pages of the course API (12 courses per page) and saves each course's title, duration, price and category | `codeyad_info.csv` (UTF-8) |
| `codeyad_image.py` | Walks through 14 pages of the same API, builds the full image URL of every course and downloads the images | `image_1.jpg`, `image_2.jpg`, ... in a local folder |

## Techniques

- Calling a paginated JSON API with query parameters (`pageId`, `take`)
- Parsing nested JSON responses
- Building absolute URLs with `urljoin`
- Writing CSV with `csv.DictWriter` (UTF-8, Persian text)
- Downloading binary files with status-code checks

## Run

```bash
pip install -r requirements.txt

python codeyad_info.py
python codeyad_image.py
```

Before running `codeyad_image.py`, change `folder_path` at the top of the file to a folder on your machine (it currently points to a Windows `D:` path). `codeyad_info.py` appends to its CSV file, so delete `codeyad_info.csv` before running it again.
