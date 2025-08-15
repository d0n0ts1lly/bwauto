import requests
from bs4 import BeautifulSoup
import time


def get_car_data(page_num=1):
    base_url = 'https://www.auctionexport.com/uk/cars/page/'
    url = f'{base_url}{page_num+2}'
    
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    cards = soup.find_all('div', class_='card mt-2')

    car_list = []

    for card in cards:
        car = {}

        name = card.find('a', class_='ae-fs-18 ae-fw-500 ae-text-dark text-decoration-none')
        car['name'] = name.text.strip() if name else 'Не вказано'

        status = card.find('div', class_='col text-muted ml-2')
        if not status:
            status_div = card.find('div', class_='row align-items-center no-gutters pt-1 pt-lg-2 px-2 px-md-3')
            if status_div:
                status = status_div.find('span')
        car['status'] = status.text.strip() if status else 'Не вказано'
        price = card.find('div', class_='col-auto ae-fs-24 ae-fw-700 ae-text-dark-blue')
        car['status'] = status.text.strip() if status else 'Попередні торги закрито'
        car['price'] = price.text.strip() if price else ''

        haract = card.find_all('div', class_='col-6 col-lg-7 ae-text-dark-blue text-truncate')
        car['lot'] = haract[0].text.strip() if len(haract) > 0 else 'Не вказано'
        car['mileage'] = haract[1].text.strip() if len(haract) > 1 else 'Не вказано'
        car['document'] = haract[2].text.strip() if len(haract) > 2 else 'Не вказано'
        car['time_left'] = haract[3].text.strip() if len(haract) > 3 else 'Не вказано'
        car['sale_date'] = haract[4].text.strip() if len(haract) > 4 else 'Не вказано'
        car['location'] = haract[5].text.strip() if len(haract) > 5 else 'Не вказано'

        sost = card.find('div', class_='ae-badge ae-badge-success') or \
               card.find('div', class_='ae-badge ae-badge-default') or \
               card.find('div', class_='ae-badge ae-badge-primary') or \
               card.find('div', class_='ae-badge ae-badge-danger')

        car['condition'] = sost.text.strip() if sost else 'Не вказано'

        image = card.find('img')
        if image and image.get('src'):
            car['image'] = f"https://www.auctionexport.com{image['src']}"
        else:
            car['image'] = 'No Image'
        
        link = card.find('a', class_='ae-fs-18 ae-fw-500 ae-text-dark text-decoration-none')
        car['link'] = f"https://www.auctionexport.com{link['href']}" if link else '#'

        car_list.append(car)

    time.sleep(0)  # Задержка между запросами
    return car_list