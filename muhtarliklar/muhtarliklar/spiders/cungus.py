import scrapy


class CungusSpider(scrapy.Spider):
    name = "cungus"
    allowed_domains = ["www.cungus.bel.tr"]
    start_urls = ["http://www.cungus.bel.tr/kurum/muhtarlar/"]

    def parse(self, response):
        for i, entry in enumerate(response.css("table > tbody > tr")):
            data = entry.css("td::text").getall()

            village = data[0].strip()
            mukhtar = data[1].strip()
            tel = data[2].strip()

            yield {
                "Il": "Diyarbakir",
                "Ilce": "Çüngüş",
                "Muhtarlik": village,
                "Muhtar": mukhtar,
                "Tel": tel,
                "Kaynak": self.start_urls[0],
            }
