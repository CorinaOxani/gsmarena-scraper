# GSMArena Web Scraper

This project implements a Python-based web scraper for collecting and analyzing
mobile phone specifications from the GSMArena platform.

The application extracts structured technical data from individual phone pages
and exports the results in JSON and CSV formats for further analysis.


## Project Structure
- `main.py` – application entry point and execution flow
- `scraper.py` – handles HTTP requests and page retrieval
- `parser.py` – parses HTML content and extracts phone specifications
- `docs/` – project documentation 
- `output/` – generated files (ignored by Git)

## Technologies Used
- Python 3
- requests
- BeautifulSoup4
- lxml


## How to Run the Project

### 1) Check Python installation

```bash
python --version
```
2) (Optional) Create and activate a virtual environment (Windows)
```bash
python -m venv venv
```
```bash
venv\Scripts\activate
```
3) Install dependencies
```bash
pip install requests beautifulsoup4 lxml
```
4) Run the application
```bash
python main.py
```
5) After execution, the generated files can be found in the output directory:

phones_full.json

phones_key_fields.json

phones_key_fields.csv


## Documentation

The full project documentation is available in the `docs` folder:
- `GSMArena_Web_Scraper_Documentation.docx`

---

This project was developed for educational purposes only.  

