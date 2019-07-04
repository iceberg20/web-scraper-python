
from bs4 import BeautifulSoup
import requests


def get_pagina_itens():
    page = requests.get('https://rn.olx.com.br/imoveis')
    soup = BeautifulSoup(page.text, 'html.parser')
    list_itens = soup.find(class_='section_OLXad-list')
    itens = list_itens.find_all(class_='item')

    return itens


def get_links(itens):
    links = []
    for x in itens:
      link = x.find(class_='OLXad-list-link')
      if link != None:
        links.append(link['href'])
    
    return links

def get_dados_link(link):
  page = requests.get(link)
  soup = BeautifulSoup(page.text, 'html.parser')
  list_loc = soup.find(class_='OLXad-location')
  for loc in list_loc.find_all(class_='description'):
    print(loc)
  
if __name__ == '__main__':
    itens = get_pagina_itens()
    links = get_links(itens)
    for link in links:
      get_dados_link(link)
