#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 14:51:16 2021

@author: ab

Webscraper energieprijzen
URLs:
* https://www.epexspot.com/en/market-data
* https://www.energyzero.nl/energiecontract/stroom-en-gas/flextarieven
"""
# %%
import pandas as pd
import requests
import webbrowser
from pathlib import Path
from datetime import date, timedelta, datetime
import re
import lxml.html as html
import dropbox

# %%
# We willen de prijzen van morgen
today = date.today()
tomorrow = today + timedelta(1)

# Browse naar website
url = "https://www.epexspot.com/en/market-data"
params = {
    "market_area": "NL",
    "trading_date": today,
    "delivery_date": tomorrow,
    "modality": "Auction",
    "sub_modality": "DayAhead",
    "product": 60,
    "data_mode": "table",
    
}
print("GET", params)
page = requests.get(url, params=params)
assert page.status_code == 200

# %%
# Optioneel: bekijk html in browser
# path = Path().resolve()
# filename = "tmp.html"
# with open(path / filename, "w") as f:
#     f.write(str(page.content))

# webbrowser.open_new_tab(f"file:///{path / filename}")


# %%
# Get html content
content = html.fromstring(page.content)

# Let op: Bij een toekomstige datum waar de data nog niet van bekend is, springt de URL terug naar die van vandaag
# Dus check de datum in <h2>
h2 = content.cssselect("h2")
assert len(h2) == 1
h2 = h2[0].text

# Alle aansluitende whitespace reduceren naar 1 spatie en strip uiteinden
h2 = re.sub(r"\s+", " ", h2).strip()
print("<h2>", h2)

# Pak laatste element na >
m = re.match(r".* > (.*)", h2)
d = datetime.strptime(m.group(1), "%d %B %Y").date()
assert d == tomorrow

# Print ook het laatste moment van updaten
last_update = re.sub(r"\s+", " ", content.cssselect("span.last-update")[0].text)
print(last_update)

# Selecteer de <table>
tbody = content.cssselect("tbody")
assert len(tbody) == 1
tbody = tbody[0]
tr_s = tbody.cssselect("tr")
assert len(tr_s) == 24

# Scrape de tabel
d = {
    "day": tomorrow,
    "hours": sorted(range(24)),
    "buy_volume": [],
    "sell_volume": [],
    "volume": [],
    "price": [],
}
column_headers = ["buy_volume", "sell_volume", "volume", "price"]
for tr in tr_s:
    for column_header, td in zip(column_headers, tr.cssselect("td")):
        d[column_header].append(td.text)

df = pd.DataFrame(d)
df

# %%
# Connect to Dropbox
import yaml
with open('cred.yaml', 'r') as file:
    cred = yaml.safe_load(file)

access_token = cred["db_key"]
dbx = dropbox.Dropbox(access_token)
assert dbx.users_get_current_account().name.abbreviated_name == "AB"

# Upload csv
binary_csv = df.to_csv(index=False).encode('utf-8')
filename = f"/epexspot_{tomorrow}.csv"
dbx.files_upload(binary_csv, filename, mode=dropbox.files.WriteMode("overwrite"))

# Print files in folder
result = dbx.files_list_folder('')
for entry in result.entries:
    print(entry.path_display)
    
print("Done")
