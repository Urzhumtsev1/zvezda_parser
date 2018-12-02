# -*- coding: utf-8 -*-

import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup


class Downloader:

    def __init__(self):
        html = urlopen("https://tvzvezda.ru/export/test-task-1.xml")
        self.bsObj = BeautifulSoup(html.read(), "lxml-xml")


class Parser:

    def __init__(self):
        self.urls_lst = []
        for news in Downloader().bsObj.findAll("url"):
            self.urls_lst.append(news)
            
    def news_list(self):
        """
        Формирует список новостей
        """
        counter = 1
        for news in range(25):
            print(str(counter) + ' ' + self.urls_lst[news].contents[3].contents[5].next)
            counter += 1

    # Альтернатиный способ формирования списка. В таком случае сложность алгоритма
    # порядка O(n**2)
    #def news_list(self):
    #    i = 1
    #    for news in enumerate(Downloader().bsObj.find_all("title"), start=i):
    #        i += 1
    #        print(str(news[0]) + '. ' + news[1].next)
    
    def get_full_news_by_number(self, num):
        """
        Используйте этот метод чтобы получить развернутое сообщение о новости.
        """
        num = int(num)
        num -= 1
        news_maker = self.urls_lst[num].contents[3].contents[1].contents[1].next
        date = self.urls_lst[num].contents[3].contents[3].contents[0]
        title = self.urls_lst[num].contents[3].contents[5].next
        url = self.urls_lst[num].contents[1].next
        html = requests.get(url)
        soup = BeautifulSoup(html.text, "html.parser")
        news = soup.find_all("div", {"class": "glav_text"})
        text = news_maker + '\n' + date + '\n' +  title + '\n' + news[0].text
        print(text)

    def get_by_tag(self, tag):
        """
        Используйте этот метод чтобы получить список новостей по тегу
        """
        tag = tag[1:-1]
        for i in range(25):
            if tag in self.urls_lst[i].contents[3].contents[7].next:
                news_maker = self.urls_lst[i].contents[3].contents[1].contents[1].next
                date = self.urls_lst[i].contents[3].contents[3].contents[0]
                title = self.urls_lst[i].contents[3].contents[5].next
                keywords = self.urls_lst[i].contents[3].contents[7].next
                url = self.urls_lst[i].contents[1].next
                text = news_maker + '\n' + date + '\n' + title + '\n' + keywords + '\n' + 'Подробнее: ' + url
                print('\n' + text + '\n')


def start():
    arg = input('Введите ALL для получения списка новостей\n' 
                'Введите номер новости по списку, '
                'чтобы получить новость.\n'
                'Ведите тег для поиска новостей по тегу\n'
                'Пример: <видео>\n')
    if arg.lower() == 'all':
        Parser().news_list()
        start()
    if arg in str([i for i in range(1,26)]):
        Parser().get_full_news_by_number(arg)
        start()
    if '<' in arg:
        Parser().get_by_tag(arg)
        start()
    else:
        print("Ошибка")
        return start()

if __name__ == '__main__':
    print("Парсер XML\n")
    start()
