import json
import csv
import os

from scraper import GsmArenaScraper
from parser import parse_phone_page, pick_key_fields

# List of phone pages that will be scraped
PHONE_URLS = [
    "https://www.gsmarena.com/samsung_galaxy_s23_ultra-12024.php",
    "https://www.gsmarena.com/xiaomi_13t_pro-12388.php",
    "https://www.gsmarena.com/google_pixel_8_pro-12545.php",
]

# Output paths
OUT_DIR = "output"
OUT_JSON_FULL = os.path.join(OUT_DIR, "phones_full.json")
OUT_JSON_KEYS = os.path.join(OUT_DIR, "phones_key_fields.json")
OUT_CSV_KEYS = os.path.join(OUT_DIR, "phones_key_fields.csv")

def ensure_out_dir():
    """Creates the output directory if it does not exist."""
    os.makedirs(OUT_DIR, exist_ok=True)

def save_json(path: str, data):
    """Saves data to a JSON file with readable formatting."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_csv(path: str, rows: list[dict]):
    """Saves a list of dictionaries to a CSV file."""
    if not rows:
        return

    fieldnames = list(rows[0].keys())
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def main():
    ensure_out_dir()

    scraper = GsmArenaScraper(delay_seconds=1.0)

    full_phones = []
    key_rows = []

    # Iterate through all phone URLs
    for url in PHONE_URLS:
        print(f"[+] Fetching: {url}")
        html, final_url = scraper.fetch(url)

        # Inform the user if a redirect happened
        if final_url != url:
            print(f"    [i] Redirected to: {final_url}")

        # Parse the phone page
        phone = parse_phone_page(html, final_url)

        # Basic sanity check to detect unexpected parsing issues
        requested_brand = final_url.split("/")[-1].split("_")[0].lower()
        parsed_model = (phone.get("model") or "").lower()

        if requested_brand and parsed_model and requested_brand not in parsed_model:
            print(f"    [WARN] Parsed model may not match URL: {phone.get('model')}")

        full_phones.append(phone)

        # Extract only the required fields
        key = pick_key_fields(phone)
        key_rows.append(key)

        # Print some info for debugging purposes
        print(f"    -> model: {key.get('model')}")
        print(f"    -> chipset: {key.get('chipset')}")
        print(f"    -> battery: {key.get('battery')}")
        print("")

    # Save results to disk
    save_json(OUT_JSON_FULL, full_phones)
    save_json(OUT_JSON_KEYS, key_rows)
    save_csv(OUT_CSV_KEYS, key_rows)

    print("[OK] Export completed:")
    print(f" - {OUT_JSON_FULL}")
    print(f" - {OUT_JSON_KEYS}")
    print(f" - {OUT_CSV_KEYS}")

if __name__ == "__main__":
    main()
