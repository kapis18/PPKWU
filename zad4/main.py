import requests
from bs4 import BeautifulSoup
import vobject


def scrape_data(query):
    url = f'https://panoramafirm.pl/szukaj?k={query}&l='
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")

    addresses = soup.findAll('div', {"class": "address"})
    phone_numbers = soup.findAll('a', {"class": "icon-telephone"})
    emails_and_names = soup.findAll('a', {"class": "ajax-modal-link"})

    company_data = [{'name': name.get('data-company-name'),
                     'email': name.get('data-company-email'),
                     'phone': phone.get('title'),
                     'address': address.text.strip()} for name, phone, address in
                    zip(emails_and_names, phone_numbers, addresses)]
    return company_data


def generate_vcard(company_list):
    for company in company_list:
        vc = vobject.vCard()
        vc.add('fn').value = company['name']
        vc.add('email').value = company['email']
        vc.add('tel').value = company['phone']
        vc.add('adr').value = vobject.vcard.Address(company['address'])
        print(vc.serialize())


generate_vcard(scrape_data("hydraulik"))
