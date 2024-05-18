import random
import csv


anim_base = open('animals.csv', 'r', newline='', encoding='utf-8')
lang_base = open('probe.csv', 'r', newline='', encoding='utf-8')
plant_base = open('probe.csv', 'r', newline='', encoding='utf-8')


# загадывает правильный ответ
def asking(mode):
    if mode == 'anim':
        base = anim_base
    if mode == 'plant':
        base = plant_base
    if mode == 'lang':
        base = lang_base
    ask = list(map(lambda x: x.strip(), random.choice(base.readlines()).split(';')))
    # print(ask)
    return ask


# достаем характеристику вида/языка из таблицы
def guess(userguess, mode):
    if mode == 'anim':
        base = anim_base
    if mode == 'plant':
        base = plant_base
    if mode == 'lang':
        base = lang_base
        res = 0
    for row in csv.reader(base):
        r = row[0].split(';')
        if userguess == r[0]:
            res = r
    return res


def proxi(a: list, g:str, mode):
    # функция проверяет, насколько близко пользователь угадал
    proximity = 0
    anim_base = open('animals.csv', 'r', newline='', encoding='utf-8')
    reader = csv.reader(anim_base, delimiter=';')
    for row in reader:
        if row[0] == g:
            guess_gen = row
    if len(a) == len(guess_gen):
        guessed_level = ''
        for level in reversed(range(len(a))):
            if a[level] == guess_gen[level]:
                guessed_level = a[level]
                proximity += 1
    return proximity, guessed_level
