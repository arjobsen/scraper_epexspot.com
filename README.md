# Scraper voor energieprijzen
Van https://www.epexspot.com/en/market-data

## Setup
1. Download en installeer [Python](https://www.python.org/downloads/) en git ([Git for Windows](https://gitforwindows.org/)) als dat nog niet is gebeurd.
1. Clone deze repo `git clone https://github.com/arjobsen/energieprijzen`
1. Navigeer naar de zojuist geclonede folder `cd energieprijzen`
1. Maak een Python [virtual environment](https://docs.python.org/3/library/venv.html) aan `python -m venv venv`
1. Activeer de venv. Met Git Bash op Windows gebruik `source venv/Scripts/activate`
1. Installeer de benodigde packages `pip install -r requirements.txt`

Voor opslag op Dropbox is een API key nodig. Die gaat natuurlijk niet openbaar op het internet.
1. Maak een tekstbestand genaamd cred.yaml aan in de folder energieprijzen en plaats daar de volgende lijn code in
`db_key: "APIKEY"`
Vervang `APIKEY` met de sleutel die je van Arjen hebt gekregen. Die "haakjes" moeten wel blijven staan.

Gefeliciteerd de setup is compleet en nu kun je de scraper uitvoeren met `python scraper.py`

