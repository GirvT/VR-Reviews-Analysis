import pandas as pd
from bs4 import BeautifulSoup
import re

dfs = pd.read_html('./vrdata.html', encoding='utf-8')[0]
dfs.to_csv('headsets.csv', index=False)

with open("./vrdata.html", encoding="utf8") as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    


table = soup.find("table", {'class':'headsetsTable'})
headsets = table.find_all("tr")
all_responce = list()
for entry in headsets:
    for path in entry.find_all("path"):
        if path.get('d') == 'M242.72 256l100.07-100.07c12.28-12.28 12.28-32.19 0-44.48l-22.24-22.24c-12.28-12.28-32.19-12.28-44.48 0L176 189.28 75.93 89.21c-12.28-12.28-32.19-12.28-44.48 0L9.21 111.45c-12.28 12.28-12.28 32.19 0 44.48L109.28 256 9.21 356.07c-12.28 12.28-12.28 32.19 0 44.48l22.24 22.24c12.28 12.28 32.2 12.28 44.48 0L176 322.72l100.07 100.07c12.28 12.28 32.2 12.28 44.48 0l22.24-22.24c12.28-12.28 12.28-32.19 0-44.48L242.72 256z':
            all_responce.append(False)
        elif path.get('d') == 'M173.898 439.404l-166.4-166.4c-9.997-9.997-9.997-26.206 0-36.204l36.203-36.204c9.997-9.998 26.207-9.998 36.204 0L192 312.69 432.095 72.596c9.997-9.997 26.207-9.997 36.204 0l36.203 36.204c9.997 9.997 9.997 26.206 0 36.204l-294.4 294.401c-9.998 9.997-26.207 9.997-36.204-.001z':
            all_responce.append(True)

add_col = pd.DataFrame({'standalone':all_responce[::2], 'base_station':all_responce[1::2]})
add_col.to_csv('addinfo.csv', index=False)