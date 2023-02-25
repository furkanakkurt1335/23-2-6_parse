import scrapy


class HataySpider(scrapy.Spider):
    name = "hatay"
    allowed_domains = ["www.hatay.gov.tr"]
    start_urls = ["http://www.hatay.gov.tr/mahalle-muhtarlari-iletisim-bilgileri"]

    def parse(self, response):
        def_district = None

        for i, entry in enumerate(response.css("table > tbody > tr")):
            if i <= 1:  # skip headers
                continue

            data = entry.css("td::text").getall()

            if data[1] == '"':
                data[1] = def_district
            else:
                def_district = data[1].strip()

            district = data[1].strip()
            village = data[2].strip()
            mukhtar = data[3].strip()
            tel = data[4].strip()

            yield {
                "Il": "Hatay",
                "Ilce": district,
                "Muhtarlik": village,
                "Muhtar": mukhtar,
                "Tel": tel,
                "Kaynak": self.start_urls[0],
            }
