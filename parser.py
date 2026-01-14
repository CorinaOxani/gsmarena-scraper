from bs4 import BeautifulSoup
from urllib.parse import urlparse

def _clean(text: str) -> str:
    """
    Helper function used to normalize text.
    It removes extra spaces and trims the string,
    because GSMArena content often contains messy formatting.
    """
    return " ".join(text.split()).strip()

def parse_phone_page(html: str, url: str) -> dict:
    """
    Parses a GSMArena phone page and extracts:
    - basic info (brand, model name, image)
    - all specifications grouped by section
    """
    # Create BeautifulSoup object to parse the HTML document
    soup = BeautifulSoup(html, "lxml")

    # Extract the phone model name from the page title
    name_tag = soup.select_one("h1.specs-phone-name-title")
    model_name = _clean(name_tag.get_text()) if name_tag else None

    # Try to determine the brand of the phone
    # Usually the first word of the model name is the brand
    brand = None
    if model_name:
        brand = model_name.split()[0]
    else:
        # Fallback option: extract brand from the URL
        path = urlparse(url).path.rsplit("/", 1)[-1]
        brand = path.split("_", 1)[0] if "_" in path else None

    # Get the main image URL of the phone
    img_tag = soup.select_one("div.specs-photo-main img")
    image_url = img_tag.get("src") if img_tag else None

    # Dictionary that will store all specs grouped by section
    specs = {}

    # Root element that contains all specifications tables
    specs_root = soup.select_one("#specs-list")

    if specs_root:
        # Each table corresponds to a section like Display, Battery, Platform, etc.
        for table in specs_root.select("table"):
            th = table.select_one("th")
            section = _clean(th.get_text()) if th else "Other"

            # Create the section if it does not already exist
            specs.setdefault(section, {})

            # Go through each row in the table
            for row in table.select("tr"):
                key_cell = row.select_one("td.ttl")  # spec name
                val_cell = row.select_one("td.nfo")  # spec value

                if not key_cell or not val_cell:
                    continue

                key = _clean(key_cell.get_text())
                val = _clean(val_cell.get_text(" ", strip=True))

                if key and val:
                    specs[section][key] = val

    # Return all extracted data in a structured dictionary
    return {
        "url": url,
        "brand": brand,
        "model": model_name,
        "image_url": image_url,
        "specs": specs,
    }

def pick_key_fields(phone: dict) -> dict:
    """
    Extracts only the fields required by the project
    (display, chipset, cameras, battery, price, etc.).
    The function is written to be robust against layout changes.
    """
    specs = phone.get("specs", {})

    def find_value(possible_keys, preferred_sections=None):
        """
        Searches for a value using multiple possible key names.
        First checks preferred sections, then falls back to all sections.
        """
        possible_keys = {k.lower() for k in possible_keys}

        if preferred_sections:
            for sec in preferred_sections:
                kv = specs.get(sec)
                if not kv:
                    continue
                for k, v in kv.items():
                    if k.lower() in possible_keys:
                        return v

        # Fallback: search in all sections
        for _, kv in specs.items():
            for k, v in kv.items():
                if k.lower() in possible_keys:
                    return v

        return None

    # Display type (taken strictly from Display section)
    display = specs.get("Display", {}).get("Type")

    # Platform information
    os_ = find_value({"os"}, preferred_sections=["Platform"])
    chipset = find_value({"chipset"}, preferred_sections=["Platform"])

    # Internal memory
    memory = find_value({"internal"}, preferred_sections=["Memory"])

    # Main camera information
    main_camera = None
    if "Main Camera" in specs:
        for k in ["Single", "Dual", "Triple", "Quad", "Modules"]:
            if k in specs["Main Camera"]:
                main_camera = specs["Main Camera"][k]
                break

    # Selfie camera information
    selfie_camera = None
    if "Selfie camera" in specs:
        for k in ["Single", "Dual", "Triple", "Modules"]:
            if k in specs["Selfie camera"]:
                selfie_camera = specs["Selfie camera"][k]
                break

    # Battery information
    battery = specs.get("Battery", {}).get("Type")
    charging = specs.get("Battery", {}).get("Charging")

    # Price is usually found in the Misc section
    price = specs.get("Misc", {}).get("Price")

    return {
        "brand": phone.get("brand"),
        "model": phone.get("model"),
        "url": phone.get("url"),
        "display": display,
        "chipset": chipset,
        "memory": memory,
        "main_camera": main_camera,
        "selfie_camera": selfie_camera,
        "battery": battery,
        "charging": charging,
        "os": os_,
        "price": price,
    }
