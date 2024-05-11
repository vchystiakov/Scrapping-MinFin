# import libraries
import requests
from bs4 import BeautifulSoup
import csv
import sys
import html.parser

# configurating system encoder
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')


# variable with file where data will be saving
CSV = 'cards.csv'

# host and url that will be parsed
HOST = "https://minfin.com.ua/"
URL = 'https://minfin.com.ua/cards/'

# dictionary with headers and accept
HEADERS = {
    "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}


# function that saves data from url in html format
def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


# function that scraps content from html and put's it into cards list
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='sc-182gfyr-0 jmBHNg')
    # list with all cards
    cards = []
    # for every card item append it's info to cards list
    for item in items:
        cards.append({
            'title': item.find('a', class_='cpshbz-0 eRamNS').get_text(strip=True),
            'link_product': HOST + item.find('a', class_='cpshbz-0 eRamNS').get('href'),
            'brand': item.find('span', class_='be80pr-21 dksWIi').get_text(strip=True),
            'card_img': HOST + item.find('img', class_='be80pr-10 jIGseK').get('srcset')
        })
    return cards


# function that writes scrapped data(cards info list) into csv file:
def save_doc(items, path):
    # opens file for writing
    with open(path, 'w', newline='', encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=';')
        # writing row title
        writer.writerow(
            ['Name of product', 'Product link', 'Bank', 'Card image'])
        # writing cards info values into rows
        for item in items:
            writer.writerow([item['title'], item['link_product'],
                            item['brand'], item['card_img']])


# main function parser that calls other funtions
def parser():
    # asking in user for setting numbers of pages for parsing
    PAGINATION = int(input('Insert quantity of pages for parsing:').strip())
    html = get_html(URL)
    # checking if request was succesful
    if html.status_code == 200:
        cards = []
        # scrapping for every page depending on value of PAGINATION
        for page in range(1, PAGINATION):
            # info for user
            print(f'Scrapping of page:{page}')
            # calling function that gets html of current page
            html = get_html(URL, params={'page': page})
            # scrapping current page and extending cards list with new values
            cards.extend(get_content(html.text))
            # writing scrapped cards list into csv file
            save_doc(cards, CSV)
        pass
    else:
        print('Error')


# calling main function
parser()
