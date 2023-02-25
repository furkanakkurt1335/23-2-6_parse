import scrapy


class KilisSpider(scrapy.Spider):
    name = "kilis"
    allowed_domains = ["www.kilis.bel.tr"]
    start_urls = ["https://www.kilis.bel.tr/index.php/2019/05/03/1438/"]

    def parse(self, response):
        district = None
        skip = True
        for entry in response.css("tbody tr"):
            data = entry.css("td strong::text").get()
            if data is not None and len(data) > 0:
                # district = data[len("KİLİS İLİ"):-len("KÖY MUHTARLARINA AİT TELEFONLAR")].strip()
                skip = True
                continue

            data = entry.css("td::text").getall()
            if data is not None and len(data) > 0:
                if skip:
                    skip = False
                    continue

                if data[0] == "\xa0\n":
                    continue

                yield {
                    "Il": "Kilis",
                    "Ilce": data[1].strip(),
                    "Muhtarlik": data[2].strip(),
                    "Muhtar": data[3].strip(),
                    "Tel": data[4].strip(),
                    "Kaynak": self.start_urls[0],
                }
