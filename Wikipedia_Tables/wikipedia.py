import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

class WikipediaTables:
    def __init__(self, url):
        self.url = url

    def extract_tables(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, features="html.parser")
        tables = soup.find_all("table", {"class": "wikitable"})        
        if not tables:
            print("No tables found")
            return False        
        for i, table in enumerate(tables, start=1):
            caption = table.caption.text.strip() if table.caption else f'NoCaption_{i}'
            heading = f"{i}_{caption}"
            df = self.read_table(table)
            self.write_csv(filename=heading + ".csv", data=df)
            return True

    def read_table(self, table):
        thead = table.find('thead')
        if thead:
            skip_rows = len(thead.find_all('tr'))
        else:
            skip_rows = 0
        return pd.read_html(str(table), skiprows=skip_rows)[0]

    def write_csv(self, filename, data):
        current_path = os.path.dirname(os.path.realpath(__file__))
        table_directory = os.path.join(current_path, f"Wikipedia_Tables_CSV/{self.url.split('/')[-1]}")
        os.makedirs(table_directory, exist_ok=True)
        filepath = os.path.join(table_directory, filename)        
        data.to_csv(filepath, index=False, encoding="utf-8")

if __name__ == "__main__":
    url = input("Enter Wikipedia URL: ")
    wto = WikipediaTables(url=url)
    wto.extract_tables()
