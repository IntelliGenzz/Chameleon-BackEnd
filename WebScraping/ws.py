import scrapy

class LinksSpider(scrapy.Spider):
    name = "links_with_info"

    start_urls = [
        'https://www.bcb.gov.br/estabilidadefinanceira/buscanormas?tipoDocumento=Todos'
    ]

    def parse(self, response):
        # Extrai todos os links da página inicial
        links = response.css('.resultado-item a').getall()

        for link in links:
            # Segue cada link e chama a função parse_link para extrair informações da página interna
            yield response.follow(link, self.parse_link)

    def parse_link(self, response):
        # Aqui você extrai as informações desejadas de dentro das páginas linkadas
        yield {
            'url': response.url,
            'title': response.css('title::text').get(),
            'paragraph': response.css('p::text').get(),  # Exemplo para extrair o primeiro parágrafo <p>
        }
