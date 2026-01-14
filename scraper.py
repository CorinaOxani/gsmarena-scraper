import time
import requests

# Default headers used to simulate a real browser request
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

class GsmArenaScraper:
    def __init__(self, delay_seconds: float = 1.0, timeout: int = 20):
        """
        Initializes the scraper.
        delay_seconds is used to avoid sending too many requests too fast.
        """
        self.delay_seconds = delay_seconds
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)

    def fetch(self, url: str) -> tuple[str, str]:
        """
        Downloads a GSMArena page and returns:
        - the HTML content
        - the final URL (after redirects, if any)
        """
        resp = self.session.get(url, timeout=self.timeout, allow_redirects=True)
        resp.raise_for_status()

        # Small delay to behave politely towards the website
        time.sleep(self.delay_seconds)

        return resp.text, resp.url
