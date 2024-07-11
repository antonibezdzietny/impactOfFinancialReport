from .scraper_type import ScraperType


class Scraper:
    def __init__(self, scraper_type: ScraperType) -> None:
        self._scraper_type = scraper_type

    def scrape(self) -> None:
        self._scraper_type.scrape_data()