
from bs4 import BeautifulSoup
import requests


def get_pagina_itens(pagina):
    page = requests.get('https://rn.olx.com.br/imoveis?o=' + pagina)
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

def get_imovel_link(link):
  page = requests.get(link)
  soup = BeautifulSoup(page.text, 'html.parser')
  preco = soup.find(class_='OLXad-price')

  if soup == None: return
  list_loc = soup.find(class_='OLXad-location')
  list_det = soup.find(class_='OLXad-details')
  
  if list_det == None: return
  if list_loc == None: return

  imovel = []
  lista_detalhamento = list_det.find(class_='list')
  lista_location = list_loc.find(class_='list')

  if lista_location != None and lista_detalhamento != None:
    bairro = ''
    cep  = ''
    municipio = ''
    tipo = ''
    numero_de_quartos = ''
    numero_de_banheiros = ''
    vagas_de_garagem = ''
    for d in lista_location.find_all('li'):
      if d.span.string[:-1] == 'CEP do imóvel':
        if d.strong != None:
          cep = d.strong.string.strip()
      if d.span.string[:-1] == 'Bairro':
        if d.strong != None:
          bairro = d.strong.string.strip()
        else:
          return
      if d.span.string[:-1] == 'Município':
        if d.strong != None:
          municipio = d.strong.string.strip()
        else:
          return

      for i in lista_detalhamento.find_all('li'):
        if (i.span.string[:-1] == 'Tipo'):
          tipo = i.strong.string.split(' ')[0]

        if (i.span.string[:-1] == 'Número de quartos'):
          numero_de_quartos = i.strong.string

        if (i.span.string[:-1] == 'Número de banheiros'):
          numero_de_banheiros = i.strong.string

        if (i.span.string[:-1] == 'Vagas na garagem'):
          vagas_de_garagem = i.strong.string

          
    if (cep != '' and municipio != '' and bairro != '' and preco != '' and tipo != '' and numero_de_quartos != '' and numero_de_banheiros !='' and vagas_de_garagem !=''):
      if preco == None: return
      imovel.append(cep)
      imovel.append(municipio)
      imovel.append(bairro)
    
      imovel.append(preco.string[3:]) #Ta iterando sobre um objeto vazio, por isso não consegue iterar com uma string
      imovel.append(tipo)
      imovel.append(numero_de_quartos) 
      imovel.append(numero_de_banheiros[0])
      imovel.append(vagas_de_garagem[0])

    return imovel


def exist_erro(pagina):
    page = requests.get('https://rn.olx.com.br/imoveis?o=' + str(pagina))
    soup = BeautifulSoup(page.text, 'html.parser')

    preco = soup.find(id='error_page')
    return preco != None

def write_csv(imoveis):
  arqv = open('imoveis.csv', 'a')
  for imovel in imoveis:
    if imovel:
      print(imovel)
      arqv.write(imovel[0] + ', ' + imovel[1] + ', ' + imovel[2] + ', ' + imovel[3] + ', ' + imovel[4] + ', ' + imovel[5] + ', ' + imovel[6] + ', ' + imovel[7] + '\n')

  arqv.close()
   
if __name__ == '__main__':
  pagina = 97

  while not exist_erro(pagina):

    itens = get_pagina_itens(str(pagina))
    links = get_links(itens)
    imoveis = []
    for link in links:
      imoveis.append(get_imovel_link(link))


      write_csv(imoveis)
 
    pagina = pagina + 1


