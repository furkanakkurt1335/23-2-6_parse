import scrapy


class MarasSpider(scrapy.Spider):
    name = "maras"
    allowed_domains = ["kahramanmaras.bel.tr"]
    start_urls = ["https://kahramanmaras.bel.tr/hizmetler/mahalle-ve-muhtarlar"]

    def parse(self, response):
        for i, entry in enumerate(response.css("table > tbody > tr")):
            data = entry.css("td::text").getall()

            district = data[0].strip()
            village = data[1].strip()

            try:
                mukhtar = data[2].strip()
                tel = data[3].strip()
            except:
                mukhtar = ""
                tel = ""

            yield {
                "Il": "Kahramanmaraş",
                "Ilce": district,
                "Muhtarlik": village,
                "Muhtar": mukhtar,
                "Tel": tel,
                "Kaynak": self.start_urls[0],
            }
