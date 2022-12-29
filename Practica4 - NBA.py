import requests

import json

url = "https://stats.nba.com/stats/playercareerstats"

params = {
"LeagueID": "00",
"PerMode": "PerGame",
"PlayerID": 977
}

headers = {
"Accept": "application/json, text/plain, */*",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "en-US,en;q=0.5",
"Connection": "keep-alive",
"DNT": "1",
"Host": "stats.nba.com",
"Origin": "https://www.nba.com",
"Referer": "https://www.nba.com/",
"TE": "Trailers",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

response = requests.get(url, headers=headers, params=params)
print(response.status_code)
print(response.json())


with open('kobe.json', 'w', encoding='utf-8') as f:
    json.dump(response.json(), f, ensure_ascii=False, indent=4)