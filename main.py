import requests
import re
from pprint import pprint
from bs4 import BeautifulSoup
from heapq import merge

DESIRED_HUBS = ['дизайн', 'selectel', 'фото', 'web', 'python']
NET = 'https://habr.com/ru/all/'
REGX = r'[а-яё]*[a-z]*'

def heapq_merge(list1, list2):
    return list(merge(list1, list2))

def search(list, link, header, where):
    for search_word in DESIRED_HUBS:
        if search_word in list:
            data = article.find('span', class_= 'post__time').text
            return [data, header, link, where]
    return None

def get_list_of_words(text):
    return re.findall(REGX, text.lower())


response = requests.get(NET)
soup = BeautifulSoup(response.text, "html.parser")
result_list = []

for article in soup.find_all('article', class_ = "post"):
    # Получаем список из слов заголовка и ссылку на полный текст
    post_title_link = article.find('a', class_= 'post__title_link')
    header = post_title_link.text
    link = post_title_link.attrs.get('href')
    list_of_words = list(map(lambda x: x.lower(), header.split(' ')))
    result = search(list_of_words, link, header, 'Заголовок')
    if result != None:
        result_list.append(result)
    else:
        full_new = BeautifulSoup(requests.get(link).text, "html.parser")
        full_text = full_new.find('div', id="post-content-body").text
        list_of_words = get_list_of_words(full_text)
        result = search(list_of_words, link, header, 'Полный текст')
        if result != None:
            result_list.append(result)
        else:
            # Получаем список из слов ссылок под заголовком
            inline_list = article.find_all('a', class_ ="inline-list__item-link")
            list_of_words = []
            for elem in inline_list:

                list_of_words = list(map(lambda x: x.lower(), heapq_merge(list_of_words, elem.text.split(' '))))
                result = search(list_of_words, link, header, 'Ссылки')
                if result != None:
                    result_list.append(result)
                else:
                    # Получаем список из слов из текста-превью
                    post_text = article.find('div', class_ = 'post__text').text.lower()
                    list_of_words = get_list_of_words(post_text)
                    result = search(list_of_words, link, header, 'Превью')
                    if result != None:
                        result_list.append(result)
pprint(result_list)
