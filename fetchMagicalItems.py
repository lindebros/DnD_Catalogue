from bs4 import BeautifulSoup
import requests
import os, os.path, csv

# name, level, type, attuned, source

results = []
url = "http://dnd5e.wikidot.com/wondrous-items"
sourceDict = {}

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# sources
sources = soup.find_all("table")[0].find_all("tr")
for s in sources:
    if (len(s.find_all("td")) == 0):
        continue
    sourceDict[s.find_all("td")[0].get_text()] = s.find_all("td")[1].get_text()

# level
levels = [l.get_text() for l in soup.find("ul", class_ = "yui-nav").find_all("em")]

# items
tabs = soup.find("div", class_ = "yui-content").find_all("table")
for ti in range(len(tabs)):
    lvl = levels[ti]
    for item in tabs[ti].find_all("tr")[1:]:
        name = item.find_all("td")[0].get_text()
        type = item.find_all("td")[1].get_text()
        attuned = item.find_all("td")[2].get_text() != '-'
        source = ", ".join([sourceDict[s] if s != 'WGE' else sourceDict["XGE"] for s in item.find_all("td")[3].get_text().split(", ") ])

        results.append([name, lvl, type, attuned, source])


with open("items.csv", 'w', encoding='utf-8', newline='') as toWrite:
    writer = csv.writer(toWrite)
    writer.writerows(results)

print(str(len(results)) + " DND items fetched")