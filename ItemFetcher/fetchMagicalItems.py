from bs4 import BeautifulSoup
import requests
import os, os.path, csv
import logging
import time


# name, level, type, attuned, source
def fetch():
    results = []
    url = "http://dnd5e.wikidot.com/wondrous-items"
    sourceDict = {}

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    itemBaseUrl = "http://dnd5e.wikidot.com"

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
        print("Fetching " + lvl + " magical items!")
        i = 0
        for item in tabs[ti].find_all("tr")[1:]:
            i += 1
            if i % 25 == 0:
                print(str(i) + " " + levels[ti]  + " magical items parsed!")
            name = item.find_all("td")[0].get_text()
            type = item.find_all("td")[1].get_text()
            attuned = item.find_all("td")[2].get_text() != '-'
            source = ", ".join([sourceDict[s] if s != 'WGE' else sourceDict["XGE"] for s in item.find_all("td")[3].get_text().split(", ") ])

            itemUrl = itemBaseUrl + item.find_all("td")[0].find("a")['href']
            itemResponse = requests.get(itemUrl)
            isoup = BeautifulSoup(itemResponse.text, "html.parser")
            desc = " ".join([p.get_text() for p in isoup.find_all("div", id="page-content")[0].find_all("p")[2:]])

            results.append([name, lvl, type, attuned, desc, source])


    with open("items.csv", 'w', encoding='utf-8', newline='') as toWrite:
        writer = csv.writer(toWrite)
        writer.writerows(results)

    print(str(len(results)) + " DND items fetched")

def main():
    logging.basicConfig()
    while True:
        try:
            fetch()
        except Exception:
            logging.exception("Failed processing")
        time.sleep(300)

if __name__ =="__main__":
    main()