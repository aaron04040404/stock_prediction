import requests
from bs4 import BeautifulSoup

def get_twse_stock_ids():
    url = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'#本國上市證券國際證券辨識號碼一覽表
    response = requests.get(url)
    response.encoding = 'big5'
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'h4'})
    rows = table.find_all('tr')[1:]
    stock_ids = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 0:
            stock_id = cols[0].text.split()[0]
            flag = stock_id
            if stock_id.isdigit():
                stock_ids.append(stock_id + '.TW')
                if flag == '9958':
                    break
    with open('stock_ids.txt', 'w') as file:
        for stock_id in stock_ids:
            file.write(stock_id + '\n')
    return True

get_twse_stock_ids()