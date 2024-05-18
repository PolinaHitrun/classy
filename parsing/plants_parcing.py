from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import csv


# функция, позволяющая извлекать со страницы ссылки на растения + последняя ссылка в списке на следующую страницу
# возвращается список из ссылок на растения со страницы с адресом-аргументом
def linkinator(anotherurl):
    anotherlinkslist = []
    soup = BeautifulSoup(requests.get(anotherurl).text, "lxml")
    languages = list(soup.findAll('a', class_=None, id_=None))
    j = 0
    m = 0
    for link in languages:
        if j == 1:
            m += 1
            anotherlinkslist.append(link.get('href'))
            if m == 202:
                break
        if link.get('title') == 'Категория:Растения по алфавиту':
            j += 1
    return anotherlinkslist

# функция, которая выделяет название конкретного уровня и возвращает это название
def determinder(line, word):
    line_check = list(line.split(word)[1])
    j = 1
    answer = line_check[0]
    if 64 < ord(answer) < 91:
        while 123 > ord(line_check[j]) > 96:
            answer += line_check[j]
            j += 1
    else:
        while ord(line_check[j]) >= 1072:
            answer += line_check[j]
            j += 1
    return answer


# функция, которая "достает" классификацию со страницы растения
# возвращает список из 6 "уровней" классификации, если в википедии какой-то уровень пропущен, на его месте 0
def classificator(link):
    print(link)
    name = pd.read_html(link, flavor='lxml')[0].columns.values[0]
    if type(name) == np.int64:
        # print(pd.read_html(link, flavor='lxml', header=1))
        if 'Unnamed: 0' in pd.read_html(link, flavor='lxml', header=1)[name]:
            data = pd.read_html(link, flavor='lxml', header=1)[name]['Unnamed: 0'][1]
        else:
            return [0, 0, 0, 0, 0, 0]
    else:
        data_0 = pd.read_html(link, flavor='lxml')[0][name]
        j = 0
        while j < len(data_0):
            if type(data_0[j]) != float:
                if 'Домен:ЭукариотыЦарство:Растения' in data_0[j]:
                    break
            j += 1
        if j >= len(data_0):
            return [0, 0, 0, 0, 0, 0]
        data = data_0[j]
    if type(data) == float:
        return [link, 0, 0, 0, 0, 0]
    elif 'Вид:' not in data or '†' in data:
        return [0, 0, 0, 0, 0, 0]
    species = data.split('Вид:')[1]

    if 'Род:' in data:
        genus = determinder(data, 'Род:')
    else:
        genus = 0
    if 'Семейство:' in data:
        family = determinder(data, 'Семейство:')
    else:
        family = 0
    if 'Порядок:' in data:
        order = determinder(data, 'Отряд:')
    else:
        order = 0
    return [species, genus, family, order, class_y, phylum]

url = 'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A0%D0%B0%D1%81%D1%82%D0%B5%D0%BD%D0%B8%D1%8F_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83'
url = 'https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A0%D0%B0%D1%81%D1%82%D0%B5%D0%BD%D0%B8%D1%8F_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&from=%D0%90'
flag = True


f = open('plants.csv', 'w', encoding='utf-8')

while flag:
    linkslist = linkinator(url)
    for i in range(len(linkslist) - 1):
        csv.writer(f).writerow(classificator('https://ru.wikipedia.org' + linkslist[i]))
        if 'https://ru.wikipedia.org/wiki/%D0%AF%D1%87%D0%BC%D0%B5%D0%BD%D1%8C_%D0%BE%D0%B1%D1%8B%D0%BA%D0%BD%D0%BE' \
           '%D0%B2%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9' == 'https://ru.wikipedia.org' + \
                linkslist[i]:
            flag = False
            break
    url = 'https://ru.wikipedia.org' + linkslist[-1]

f.close()

