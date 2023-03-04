from bs4 import BeautifulSoup
import requests
import os, os.path, csv

# name, source, size, type, cr

results = []
url = "https://dungeonsdragons.fandom.com/wiki/List_of_Dungeons_%26_Dragons_5th_edition_monsters"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

table = soup.find_all('table')[0]



for rows in table.find_all("tr"):
    if (len(rows.find_all("td")) == 0):
        continue
    name = rows.find_all("td")[0].get_text()
    source = rows.find_all("td")[1].get_text()
    size = rows.find_all("td")[2].get_text()
    type = rows.find_all("td")[3].get_text()
    cr = rows.find_all("td")[4].get_text().replace("\n", "")
    results.append([name,source,size,type,cr])
    


with open("monsters.csv", 'w', encoding='utf-8', newline='') as toWrite:
    writer = csv.writer(toWrite)
    writer.writerows(results)

print(str(len(results)) + " DND monsters fetched")