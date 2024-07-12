from abc import ABC, abstractmethod


class ScraperType(ABC):
    @abstractmethod
    def page_parse(self, raw_page):
        pass

    @abstractmethod
    def save_to_csv(self, data):
        pass