import scrapy


class OsmaniyeSpider(scrapy.Spider):
    name = "osmaniye"
    allowed_domains = ["osmaniye-bld.gov.tr"]
    start_urls = ["https://osmaniye-bld.gov.tr/kurumsal/mahalle-muhtarlari"]

    def parse(self, response):
        for i, entry in enumerate(response.css("table tr")):
            if i <= 1:
                continue

            data = entry.css("td::text").getall()
            mukhtar = data[0].strip()
            village = data[1][: -len("Mahalle Muhtarı")].strip()
            tel = data[2].strip()

            yield {
                "Il": "Osmaniye",
                # "Ilce": district,
                "Muhtarlik": village,
                "Muhtar": mukhtar,
                "Tel": tel,
                "Kaynak": self.start_urls[0],
            }
