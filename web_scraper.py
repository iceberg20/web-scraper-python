
from bs4 import BeautifulSoup
import requests


page = requests.get('https://rn.olx.com.br/imoveis')

soup = BeautifulSoup(page.text, 'html.parser')

pag2 = 'https://rn.olx.com.br/imoveis?o=2'
pag3 = 'https://rn.olx.com.br/imoveis?o=3'

list_itens = soup.find(class_= 'section_OLXad-list')

itens = list_itens.find_all(class_='item')
prices = itens.find(class_='OLXad-list-price')

for x in itens:
  print(x.prettify())



