import requests
from bs4 import BeautifulSoup
from random import randint


# Імпорт з файлу для автоматизації
__all__ = ('work', "rabota", 'dou', 'djinni')

# Підставна інфа щоб бота прийняли за браузер
headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    ]


def work(url, city=None, language=None):
    """Скрапінг по сайту work.ua"""
    jobs = []
    errors = []
    domain = 'https://www.work.ua'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:  # Перевірка на наявність данних
            soup = BeautifulSoup(resp.content, 'html.parser')
            # Пошук інфи проходить по div
            main_div = soup.find('div', id='pjax-job-list')
            if main_div:
                div_lst = main_div.find_all('div', attrs={'class': 'job-link'})
                for div in div_lst:  # Обробляєм інфу по вакансії
                    title = div.find('h2')  # Назва вакансії
                    href = title.a['href']  # URL вакансії
                    content = div.p.text  # Основний текст вакансії
                    company = 'No name'  # Компанія
                    logo = div.find('img')  # Альтернатива назві компанії
                    if logo:
                        company = logo['alt']
                    # Оброблену інфу по вакансії збиваєм в словарь і запихуєм в список
                    jobs.append({'title': title.text,
                                 'url': domain + href,
                                 'description': content,
                                 'company': company,
                                 'city_id': city,
                                 'language_id': language})
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})
    return jobs, errors


def rabota(url, city=None, language=None):
    """Скрапінг по сайту rabota.ua. Увага, зміна назви таблиці на сайті проходить раз в 2 місяці"""
    jobs = []
    errors = []
    domain = 'https://rabota.ua'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:  # Перевірка на наявність данних
            soup = BeautifulSoup(resp.content, 'html.parser')
            new_jobs = soup.find('div', attrs={'class': 'f-vacancylist-newnotfound'})
            # Div запакований в таблиці тому пошук інфи проходить по таблицям у яких є id
            if not new_jobs:
                table = soup.find('table', id='ctl00_content_vacancyList_gridList')
                if table:
                    tr_lst = table.find_all('tr', attrs={'id': True})
                    for tr in tr_lst:  # Обробляєм інфу по вакансії
                        div = tr.find('div', attrs={'class': 'card-body'})
                        if div:
                            title = div.find('p', attrs={'class': 'card-title'})  # Назва вакансії
                            href = title.a['href']  # URL вакансії
                            content = div.p.text  # Основний текст вакансії
                            company = 'No name'
                            p = div.find('p', attrs={'class': 'company-name'})
                            if p:
                                company = p.a.text  # Компанія
                            # Оброблену інфу по вакансії збиваєм в словарь і запихуєм в список
                            jobs.append({'title': title.text,
                                         'url': domain + href,
                                         'description': content,
                                         'company': company,
                                         'city_id': city,
                                         'language_id': language})
                else:
                    errors.append({'url': url, 'title': "Table does not exists"})
            else:
                errors.append({'url': url, 'title': "Page is empty"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})
    return jobs, errors


def dou(url, city=None, language=None):
    """Скрапінг по сайту dou.ua"""
    jobs = []
    errors = []
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:  # Перевірка на наявність данних
            soup = BeautifulSoup(resp.content, 'html.parser')
            main_div = soup.find('div', id='vacancyListId')
            if main_div:
                li_lst = main_div.find_all('li', attrs={'class': 'l-vacancy'})
                for li in li_lst:
                    title = li.find('div', attrs={'class': 'title'})
                    href = title.a['href']
                    cont = li.find('div', attrs={'class': 'sh-info'})
                    content = cont.text
                    company = 'No name'
                    a = title.find('a', attrs={'class': 'company'})
                    if a:
                        company = a.text
                    jobs.append({'title': title.text,
                                 'url': href,  # На сайті ссилка абсолютна
                                 'description': content,
                                 'company': company,
                                 'city_id': city,
                                 'language_id': language})
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})
    return jobs, errors


def djinni(url, city=None, language=None):
    """Скрапінг по сайту djinni.co"""
    jobs = []
    errors = []
    domain = 'https://djinni.co'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:  # Перевірка на наявність данних
            soup = BeautifulSoup(resp.content, 'html.parser')
            # Div відсутній, шукаєм по классам
            main_ul = soup.find('ul',  attrs={'class': 'list-jobs'})
            if main_ul:
                li_lst = main_ul.find_all('li', attrs={'class': 'list-jobs__item'})
                for li in li_lst:
                    title = li.find('div', attrs={'class': 'list-jobs__title'})
                    href = title.a['href']
                    cont = li.find('div', attrs={'class': 'list-jobs__description'})
                    content = cont.text
                    company = 'No name'
                    comp = li.find('div', attrs={'class': 'list-jobs__details__info'})
                    if comp:
                        company = comp.text
                    jobs.append({'title': title.text,
                                 'url': domain + href,
                                 'description': content,
                                 'company': company,
                                 'city_id': city,
                                 'language_id': language})
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})
    return jobs, errors
