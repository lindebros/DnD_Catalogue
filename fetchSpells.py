from bs4 import BeautifulSoup
import requests
import os, os.path, csv

results = []

url = "https://www.dnd-spells.com/spells"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

#name, level, school, classes, casting time, ritual, concentration, source

for rows in soup.find_all("tr"):
    if len(rows.find_all("td")) > 0:
        name = rows.find_all("td")[1].get_text().split("\n")[0].split(" (")[0]
        level = rows.find_all("td")[2].get_text()
        school = rows.find_all("td")[3].get_text()
        classes = ", ".join(rows.find_all("td")[7].get_text().replace(" ", "").split("\r\n")[:-1])
        castingtime = rows.find_all("td")[4].get_text()
        ritual = rows.find_all("td")[5].get_text()
        concentration = rows.find_all("td")[6].get_text()
        source = rows.find_all("td")[8].get_text()
        results.append([name, level, school, classes, castingtime, ritual, concentration, source])

with open("spells.csv", 'w', encoding='utf-8', newline='') as toWrite:
    writer = csv.writer(toWrite)
    writer.writerows(results)

print(str(len(results)) + " DND spells fetched")