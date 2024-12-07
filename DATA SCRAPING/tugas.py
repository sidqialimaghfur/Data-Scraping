from bs4 import BeautifulSoup
from selenium import webdriver
import time

URL = 'https://www.tokopedia.com/search'

params = {
    'q': 'klemben banyuwangi'
}

driver = webdriver.Chrome()
fullURL = f"{URL}?q={params['q']}"  
driver.get(fullURL)

time.sleep(10)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

data = soup.find_all('div', {'class': 'css-5wh65g'})

for i in range(len(data)):
    nama_produk = data[i].find('span', {'class': '_0T8-iGxMpV6NEsYEhwkqEg=='})
    harga = data[i].find('div', {'class': '_67d6E1xDKIzw+i2D2L0tjw=='})
    penjual = data[i].find('span', {'class': 'T0rpy-LEwYNQifsgB-3SQw== pC8DMVkBZGW7-egObcWMFQ== flip'})
    if nama_produk and harga and penjual :
        print("nama produk: "+nama_produk.text)
        print("harga: "+harga.text)
        print("penjual: "+penjual.text)

print(data)
driver.quit()