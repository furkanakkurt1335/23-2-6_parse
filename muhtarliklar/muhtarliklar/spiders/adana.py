import scrapy


class AdanaSpider(scrapy.Spider):
    name = "adana"
    allowed_domains = ["www.adana.bel.tr"]
    start_urls = ["https://www.adana.bel.tr/tr/muhtar1"]

    def parse(self, response):
        for entry in response.css(".MuhtarlarList"):
            district = entry.css(".icon-card-list-item-sub-title::text").get()
            district = district.strip().split("/")
            district, village = district[0].strip(), district[1].strip()

            mukhtar = entry.css(".icon-card-list-item-title::text").get().strip()
            tel = entry.css("p > a::text").get().strip()

            yield {
                "Il": "Adana",
                "Ilce": district,
                "Muhtarlik": village,
                "Muhtar": mukhtar,
                "Tel": tel,
                "Kaynak": self.start_urls[0],
            }
