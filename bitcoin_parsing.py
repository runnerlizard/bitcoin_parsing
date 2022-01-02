import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from multiprocessing import Pool


def get_html(url):
    r = requests.get(url)
    return r.text


def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('table', class_='cmc-table').find_all('div', class_='sc-16r8icm-0 escjiH')
    links = []
    for div in divs:
        a = div.find('a', class_='cmc-link').get('href')
        link = 'https://coinmarketcap.com' + a
        links.append(link)  
    return links


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    name = soup.find('h2', class_='h1').text.strip()
    cost = soup.find('div', class_ = 'priceValue').text.strip()
    data = {'name': name,
            'price': cost}
    return data


def write_csv(data):
    with open('coinmarketcap.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow( (data['name'],
                          data['price']) )
        print(data['name'], 'parsed')


def multiproc(url):
    html = get_html(url)
    data = get_page_data(html)
    write_csv(data)


def main():
    start = datetime.now()
    url = 'https://coinmarketcap.com/'
    html = get_html(url)
    all_links = get_all_links(html)
    with Pool(40) as p:
        p.map(multiproc, all_links)
    end = datetime.now()
    print (end - start)


if __name__ == '__main__':
    main()