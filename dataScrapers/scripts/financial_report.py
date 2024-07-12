from .scraper_type import ScraperType
import pandas as pd


class FinancialReport(ScraperType):
    MAIN_URL = "https://www.biznesradar.pl"
    SUB_URL  = [
            "raporty-finansowe-rachunek-zyskow-i-strat",
            "raporty-finansowe-bilans",
            "raporty-finansowe-przeplywy-pieniezne",
        ]
    DEFAULT_SAVE_PATH = [
        "../database/financial_report/bill",
        "../database/financial_report/balance",
        "../database/financial_report/flow",
    ]

    def __init__(self, company_names: list | str) -> None:
        super().__init__()
        self.set_company_names(company_names)

    def __iter__(self):
        return self
    
    def __next__(self) -> str:
        if self._current_page < self._page_to_read:
            self._current_page += 1
            return '{}/{}/{},Y'.format(FinancialReport.MAIN_URL,
                                       FinancialReport.SUB_URL[(self._current_page-1)%len(FinancialReport.SUB_URL)],
                                       self._company_names[(self._current_page-1)//len(FinancialReport.SUB_URL)])
        raise StopIteration

    def _set_iteration(self) -> None:
        self._current_page = 0
        self._page_to_read = len(self._company_names) * len(FinancialReport.SUB_URL) 

    def _get_content_table(self, raw_page):
        """Find and return html table with financial data"""
        return raw_page.find("table", attrs={"class":"report-table"})

    def _get_years_data(self, raw_table) -> dict:
        """Find and return row with year of publication"""
        year_header = raw_table.find("tr") # Get first row (row with date)
        year_coll = year_header.find_all("th", attrs={"class":"thq h"})
        return {"Rok": ["".join(y.text.split()).split('(')[0] for y in year_coll ]}

    def _get_financial_data(self, raw_table) -> dict:
        """Find and return financial raport data"""
        financial_data = {}

        # Remove premium rows 
        for premium_row in raw_table.find_all("tr", attrs={"class":"premium-row"}): #Remove premium row 
            premium_row.decompose()

        # Find important data
        important_rows = raw_table.find_all("tr", attrs={"class":"bold"})

        # Cast data
        for row in important_rows:
            row_header = row.find("td", attrs={"class":"f"}).find("strong").text

            values = []
            for column in row.find_all("td", attrs={"class":"h"}):
                bold_data_value = column.find("span", attrs={"class":"value"}).find("span", attrs={"class":"pv"})
                values.append("".join(bold_data_value.text.split()))
            
            financial_data[row_header] = values[:-1]

        return financial_data

    def set_company_names(self, company_names: list | str) -> None:
        self._company_names = [company_names] if isinstance(company_names, str) else company_names
        self._set_iteration()

    def get_current_page(self) -> int:
        return self._current_page
    
    def get_page_to_read(self) -> int:
        return self._page_to_read

    def page_parse(self, raw_page) -> pd.DataFrame:
        table = self._get_content_table(raw_page)
        data = {}
        data.update(self._get_years_data(table))
        data.update(self._get_financial_data(table))
        return pd.DataFrame(data).transpose()

    def save_to_csv(self, data: pd.DataFrame):
        str_path = "{}/{}.csv".format(
            FinancialReport.DEFAULT_SAVE_PATH[(self._current_page-1)%len(FinancialReport.DEFAULT_SAVE_PATH)],
            self._company_names[(self._current_page-1)//len(FinancialReport.DEFAULT_SAVE_PATH)])
        data.to_csv(str_path)