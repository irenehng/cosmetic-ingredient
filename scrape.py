import requests
from bs4 import BeautifulSoup
import csv

# url = "https://ec.europa.eu/growth/tools-databases/cosing/reference/functions"
# response = requests.get(url)

with open('table.html', 'r') as f:
    contents = f.read()
    soup = BeautifulSoup(contents, "html.parser")

table = soup.find("table").tbody
table_data = []

for row in table.find_all("tr"):
    columns = row.find_all("td")
    inci = columns[1]
    i_name = inci.text.strip()
    table_data.append([i_name, "Depilatory"])

with open("ingredient-function.csv", "a", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(table_data)
