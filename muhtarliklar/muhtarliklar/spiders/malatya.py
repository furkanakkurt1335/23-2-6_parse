import scrapy


class MalatyaSpider(scrapy.Spider):
    name = "malatya"
    allowed_domains = ["www.malatya.gov.tr"]
    start_urls = ["http://www.malatya.gov.tr/muhtarliklarimiz"]

    def parse(self, response):
        with open("page.html", "w") as f:
            f.write(response.text)

        districts = response.css(
            "div.accordion span.card div.card-header h5::text"
        ).getall()
        districts = [
            district[: -len("İlçesi Mahalle Muhtarlıkları")].strip()
            for district in districts
        ]

        for idx, entry in enumerate(response.css("div.accordion table table")):
            for i, entry_row in enumerate(entry.css("tr")):
                if i == 0:  # skip headers
                    continue

                data = entry_row.css("td > p span::text").getall()

                if len(data) < 5:  # missing information
                    continue

                mukhtar = data[1].strip() + " " + data[2].strip()
                village = data[3].strip()
                tel = "\t".join([data[i].strip() for i in range(4, len(data))])

                yield {
                    "Il": "Malatya",
                    "Ilce": districts[idx],
                    "Muhtarlik": village,
                    "Muhtar": mukhtar,
                    "Tel": tel,
                    "Kaynak": self.start_urls[0],
                }
