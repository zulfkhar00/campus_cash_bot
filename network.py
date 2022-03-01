import requests
from bs4 import BeautifulSoup, NavigableString
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder


url = 'https://services.jsatech.com/login.php?cid=156'

def getSkey():
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    skey = soup.find('input', {'name': 'skey'}).get('value')
    return skey

def getTransactions(table, isFlex):
    transactions = []
    trs = table.find_all('tr', {'role': 'row'})[2:]
    for tr in trs:
        date = tr.find('th').getText()
        place = tr.find('td', {'class': 'jsa_desc'}).getText()
        row = tr.find('td', {'class': 'jsa_amount'})
        chargedPrice = [element.strip() for element in row if isinstance(element, NavigableString)][0]
        if isFlex:
            chargedPrice = str(float(chargedPrice)/100)
        transactions.append({
            'date': date,
            'place': place,
            'chargedPrice': chargedPrice
        })
    return transactions
    

def getMoney(money):
    mp_encoder = MultipartEncoder(
        fields={
            'loginphrase': 'olxzulfar@gmail.com',
            'password': '11HQLQD55T'
        }
    )
    skey = getSkey()
    response = requests.post(
        url+'&skey='+skey+'&fullscreen=1&wason=',
        data=mp_encoder,
        headers={'Content-Type': mp_encoder.content_type}
    )

    url2 = 'https://services.jsatech.com/index.php?skey='+skey+'&cid=156&'
    r2 = requests.get(url2)
    soup = BeautifulSoup(r2.text, 'html.parser')
    tables = soup.find_all('table')
    moneyId = 0
    if money == 'campus':
        moneyId = 1
    elif money == 'falcon':
        moneyId = 2
    elif money == 'swipe':
        moneyId = 3
    elif money == 'flex':
        moneyId = 4

    if money == 'campus' or money == 'falcon' or money == 'swipe':
        row = tables[moneyId].find_all('tr')[1].find('td', {'class': 'jsa_amount'})
        balance = [element.strip() for element in row if isinstance(element, NavigableString)][0]
    elif money == 'flex':
        row = tables[moneyId].find_all('tr')[2].find('p')
        balance = [element.strip() for element in row if isinstance(element, NavigableString)][0]
        balance = str(float(balance)/100) + ' AED'
    
    transactions = getTransactions(tables[moneyId], True if moneyId == 4 else False)
    return {'balance': balance, 'transactions': transactions}