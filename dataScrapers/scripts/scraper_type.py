from abc import ABC, abstractmethod


class ScraperType(ABC):
    @abstractmethod
    def scrape_data(self):
        pass