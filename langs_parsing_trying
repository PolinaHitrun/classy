import csv
import requests
from bs4 import BeautifulSoup


with open('id_languages.csv', newline='', encoding='utf-8') as csvfile:
    idreader = csv.reader(csvfile, delimiter=',')
    hrefs_list = []
    for row in idreader:
        hrefs_list.append('https://glottolog.org/resource/languoid/id/' + row[0])
    hrefs_list = hrefs_list[1:]
for href in hrefs_list:
    page = requests.get(href)
    soup = BeautifulSoup(page.text, 'html.parser')
    script = soup.find_all('script', 'GLOTTOLOG3.Tree.init')
    print(script)
