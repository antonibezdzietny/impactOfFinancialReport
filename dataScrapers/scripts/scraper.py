from .scraper_type import ScraperType
from bs4 import BeautifulSoup
import requests


class Scraper:
    def __init__(self, scraper_type: ScraperType) -> None:
        self._scraper_type = scraper_type

    def _request_page(self, addr: str):
        request = requests.get(addr)
        page = BeautifulSoup(request.content, 'html.parser')
        return page

    def scrape(self) -> None:
        for addr in self._scraper_type:
            data = self._scraper_type.page_parse(self._request_page(addr))
            self._scraper_type.save_to_csv(data)
