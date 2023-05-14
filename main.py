import random

import requests
from bs4 import BeautifulSoup
import json
import csv
from time import sleep
headers = {
    'Accept' : '*/*',
    'User-Agent' : 'Mozilla/5.0 (Linux; U; Linux x86_64) AppleWebKit/533.39 (KHTML, like Gecko) Chrome/55.0.3476.141 Safari/535'

}

# url = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'
# req = requests.get(url, headers=headers)
# src = req.text

# with open('index.html', 'w', encoding='utf-8') as file: # Сохраняем сайт в файл эйчтиэмэл
#     file.write(src)

# with open('index.html', encoding='utf-8') as file:   #открываем, читаем файл и сохранем код страницы в переменную
#     src = file.read()
#
# soup = BeautifulSoup(src, 'lxml')
#
# all_products_herf = soup.find_all(class_='mzr-tc-group-item-href') # Ищем все классы с названием и ссылками на продукты
#
# all_categories_dict = {} # Словарь с названиями категорий и ссылками на них
#
# for items in all_products_herf: # Просто Что бы посмотреть все то что мы собрали
#     #print(items)
#     item_text = items.text # Переменная с названием категории
#     item_href = 'https://health-diet.ru' + items.get('href') # Переменная с сылкой на категорию
#     all_categories_dict[item_text] = item_href # Добавляем все в словарь, где ключи это имена категорий а ссылки - значения
#
# with open('all_categories_dict.json', 'w', encoding='utf-8') as file: # Сохраняем словарь в файл json
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False) # indent - Отступ в файле, ensure_ascii - помогает при работе с кирилицей


with open('all_categories_dict.json', encoding='utf-8') as file: # Загружаем файл json в переменную all_categories
    all_categories = json.load(file) # в этой переменной находится словарь с названиями и ссылками сделанный ранее




#КОД ВНИЗУ создает цикл на каждой итерации которого мы будем заходить на новую страницу категории, собирать с нее данные о всех товарах
# их химическом составе и записывать вспе это в файл
iteration_count = int(len(all_categories)) - 1
count = 0
print(f'Всего итераций: {iteration_count}')
for category_name, category_href in all_categories.items(): # запятую пробел и слэш, которые встречаются в названии будем менять на _


    rep = [',', ' ', '-']# Список из символов которые хотим заменить
    for item in rep:# В цикле пробегаемся по символам
        if item in category_name:            # Если символ есть в имени
            category_name = category_name.replace(item, '_') # То меняем его на нижний слэш


    # Переходим к запросам на страницк
    req = requests.get(url=category_href, headers=headers)
    src = req.text

    #Сохраняем страницу под именем категории
    with open(f'data/{count}_{category_name}.html', 'w', encoding='utf-8') as file:
        file.write(src)

    # Открываем и сохраняем код страницы в переменную
    with open(f'data/{count}_{category_name}.html', encoding='utf-8') as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')

    # Проверка страницы на наличие таблицы с продуктами

    alert_block = soup.find(class_='uk-alert-danger')
    if alert_block is not None:
        continue

    # Собираем заголвоки таблицы
    table_head = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbo = table_head[4].text


    # Открываем файл на запись
    with open(f'data/{count}_{category_name}.csv', 'w', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';') # Переменная писатель
        writer.writerow(     #Указываем писателю что записывать в файл
            (
                product,
                calories,
                proteins,
                fats,
                carbo
            )
        )


    # Собираем данные продуктов
    products_data = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')

    # В цикле собирем из каждого tr тэга td тэги в которых содержится информация
    for item in products_data:
        product_tds = item.find_all('td')

        title = product_tds[0].find('a').text
        calories = product_tds[1].text
        proteins = product_tds[2].text
        fats = product_tds[3].text
        carbo = product_tds[4].text

        # Открываем файл на запись
        with open(f'data/{count}_{category_name}.csv', 'a', encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=';')  # Переменная писатель
            writer.writerow(  # Указываем писателю что записывать в файл
                (
                    title,
                    calories,
                    proteins,
                    fats,
                    carbo
                )
            )
    count += 1
    print(f'# Итерация {count}. {category_name} записан...')

    iteration_count = iteration_count - 1

    if iteration_count == 0:
        print('Работа закончена')
        break

    print(f'Осталось итераций: {iteration_count}')
    sleep(random.randrange(2, 4))
