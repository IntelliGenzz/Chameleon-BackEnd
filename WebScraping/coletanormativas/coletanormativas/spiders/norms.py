import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from scrapy.http import HtmlResponse
import time

class NormsSpider(scrapy.Spider):
    name = "norms_selenium"

    start_urls = [
        'https://www.bcb.gov.br/estabilidadefinanceira/buscanormas?tipoDocumento=Todos',
    ]

    def __init__(self, *args, **kwargs):
        super(NormsSpider, self).__init__(*args, **kwargs)
        
        # Configuração do Selenium para usar o Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Executa o navegador em modo headless (sem interface gráfica)
        service = Service('C:\Program Files\Google\Chrome\Application\ChromeDriver')  # Substitua pelo caminho para o seu ChromeDriver
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def parse(self, response):
        # Usa Selenium para carregar a página e esperar o carregamento completo
        self.driver.get(response.url)
        time.sleep(3)  # Espera 3 segundos para garantir que a página foi carregada completamente
        
        # Extrai o conteúdo da página carregada
        selenium_response = HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding='utf-8')

        # Seleciona todos os links que contêm a string '/estabilidadefinanceira/exibenormativo?tipo=' no href
        links = selenium_response.css('a[href^="/estabilidadefinanceira/exibenormativo?tipo="]::attr(href)').getall()

        if not links:
            self.logger.warning('Nenhum link encontrado. Verifique os seletores CSS.')

        self.logger.info(f'Links encontrados: {links}')

        for link in links:
            # Gera a URL absoluta para seguir o link
            yield response.follow(link, self.parse_link)

    def parse_link(self, response):
        # Extrai as informações desejadas de dentro das páginas linkadas
        yield {
            'url': response.url,  # URL da página atual
            'title': response.css('title::text').get(),  # Título da página
            'heading': response.css('h1::text').get(),  # Primeiro cabeçalho <h1>
            'paragraph': response.css('p::text').get(),  # Primeiro parágrafo <p>
        }

    def closed(self, reason):
        # Fecha o navegador ao final do processo
        self.driver.quit()


