import requests
from bs4 import BeautifulSoup

url = 'https://www.bcb.gov.br/estabilidadefinanceira/buscanormas?tipoDocumento=Todos'
headers = {
    'User Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

def proximapagina(soup): 
    # procura botao que avança pagina
    paginas = soup.find('a', {'class': 'page-link ng-star-inserted'})
    # ir ate a ultima pagina onde o botao desativa
    if not soup.find('li', {'class': 'page-item disabled'}):
        url = 'https://www.bcb.gov.br/'
        prox = soup.find('a', 'page-link ng-star-inserted', href=True)
        url_final = (url + str(prox['href']))
        return url_final
    else:
        return
    
site = requests.get(url, headers= headers)
soup = BeautifulSoup(site.content, 'html.parser')
url = proximapagina(soup)

print(url)