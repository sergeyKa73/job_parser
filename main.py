from bs4 import BeautifulSoup as bs
import requests
import csv
import fake_useragent

user = fake_useragent.UserAgent().random
header = {'user-agent': user}
CSV = 'data/job.csv'

def get_html(url):
    r = requests.get(url, headers=header)
    if r.ok:  # 200  ## 403 404
        return r.text
    print(r.status_code)

def write_csv(data, path):
    with open(path, 'a') as file:
        writer = csv.writer(file)
        writer.writerow((data['title'],
                         data['company'],
                         data['location'],
                         data['url']))

def get_page_content(html):
    soup = bs(html, 'lxml')
    vacancys = soup.find_all('div', class_='vacancy-serp-item')
    for vacancy in vacancys:
        try:
            title = vacancy.find('div', class_='vacancy-serp-item__info').text
        except:
            title = ''
        try:
            company = vacancy.find('div', class_='vacancy-serp-item__meta-info-company').text

        except:
            company = ''
        try:
            location = vacancy.find('div',attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text.split()[0].replace(',','') # вынести в отдельную функцию
        except:
            location = ''
        try:
            url = vacancy.find('a', class_='bloko-link').get('href')
        except:
            url = ''


        data = {'title': title,
                'company': company,
                'location': location,
                'url': url,
                }

        write_csv(data, CSV)


def get_next_page(html):
    soup = bs(html, 'lxml')
    paginators = soup.find_all('span', class_='pager-item-not-in-short-range')
    pages = []
    for page in paginators:
        pages.append(page.text)
    n = int(pages[-1])
    print(n)
    return n

def main():
    url = 'https://rabota.by/search/vacancy?area=16&text=Python'
    PAGENATION = get_next_page(get_html(url))
    pattern = 'https://rabota.by/search/vacancy?area=16&text=Python&page='
    for page in range(0, PAGENATION):
        url = pattern.format(str(page))
        print(f'Парсинг страницы {page}')
        get_page_content(get_html(url))



if __name__ == '__main__':
    main()
