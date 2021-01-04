import requests
import datetime
import json
from bs4 import BeautifulSoup
# import pandas as pd
# from matplotlib import pyplot as plt
# import seaborn as sns
import smtplib
import time

URL = 'https://cars.ksl.com/search/make/Mazda/model/CX-9/priceFrom/15000/priceTo/23000/zip/84005/miles/50/newUsed/Used;Certified/titleType/Clean+Title'
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; intel Mac OS 11_1_0) AppleWebKit/537.36 (KHTML, Like Geko) Chrome/87.0.4280.88 Safari/537.36'}
page = requests.get(URL, headers=header)

soup = BeautifulSoup(page.content, 'html.parser')

results = [car['data-listing']
           for car in soup.find_all() if 'data-listing' in car.attrs]


def miles_by_year(mileage, year):
    total_years = datetime.datetime.now().year - year
    return mileage / total_years


def send_mail(e_body):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('b2randon@gmail.com', 'ghtbrqoqimccgdof')
    subject = 'Car Search'
    body = e_body

    msg = f'Subject: {subject}\n\n{body}'
    server.sendmail(
        'b2randon@gmail.com',
        'b2randon@gmail.com',
        msg
    )
    print('email sent')
    server.quit()


# set up while loop to run the program 2 times a day
#time.sleep(60 * 60 * 12)
email_msg = ''
for car in results:
    car_obj = json.loads(car)
    make = f'Make: \t\t {car_obj["make"]}'
    model = f'Model: \t\t {car_obj["model"]}'
    price = f'Price: \t\t ${car_obj["price"]:,.2f}'
    year = f'Year: \t\t {car_obj["makeYear"]}'
    mileage = f'Mileage: \t {car_obj["mileage"]:,.0f}'
    mileage_by_year = f'Mileage by Year: {miles_by_year(car_obj["mileage"], car_obj["makeYear"]):,.0f}'
    vin = f'Vin: \t\t {car_obj["vin"]}'
    link = f'cars.ksl.com/listing/{car_obj["id"]}'
    print(make)
    print(model)
    print(price)
    print(year)
    print(mileage)
    print(mileage_by_year)
    print(vin)
    print('\n')

    email_msg += (make + '\n' + model + '\n' + price + '\n' + year + '\n' + mileage + '\n' + mileage_by_year + '\n' + vin + '\n' + link + '\n\n')

send_mail(email_msg)
# df = pd.read_csv('./Pokemon1.csv', index_col=0)

# sns.lmplot(x='Attack', y='Defense', data=df, fit_reg=False, hue='Stage')
