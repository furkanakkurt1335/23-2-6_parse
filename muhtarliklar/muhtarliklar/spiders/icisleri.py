import json
import scrapy


class IcisleriSpider(scrapy.Spider):
    name = "icisleri"
    start_urls = [
        "http://www.adana.gov.tr/ilcelerimiz",
        "http://www.adiyaman.gov.tr/ilcelerimiz",
        "http://www.diyarbakir.gov.tr/ilcelerimiz",
        "http://www.gaziantep.gov.tr/ilcelerimiz",
        "http://www.hatay.gov.tr/ilcelerimiz",
        "http://www.kahramanmaras.gov.tr/ilcelerimiz",
        "http://www.kilis.gov.tr/ilcelerimiz",
        "http://www.malatya.gov.tr/ilcelerimiz",
        "http://www.osmaniye.gov.tr/ilcelerimiz",
        "http://www.sanliurfa.gov.tr/ilcelerimiz",
    ]
    queries = {}

    def parse(self, response):
        # ---- IL DETAY ----
        if "ValilikDetay" in response.url:
            il = response.css(".city-title h1::text").get().strip()

            for entry in response.css(".governorship-contact-cart"):
                ilce = entry.css("h5::text").get().strip()
                link = entry.css("div.item-links ::attr(href)").get()
                yield scrapy.Request(
                    link + "/mahalli-idareler",
                    callback=self.parse,
                    meta={"il": il, "ilce": ilce, **response.meta},
                )

            return

        # ---- ILCE DETAY ----
        if "DetayGetir" in response.url:
            obj = json.loads(response.text)
            for item in obj["Data"]["muhtarliklar"]:
                yield {
                    "Il": response.meta["il"],
                    "Ilce": response.meta["ilce"],
                    "Muhtarlik": item["Ad"],
                    "Muhtar": item["BaskanAdi"],
                    "Boylam": item["KoordinatBoylam"],
                    "Enlem": item["KoordinatEnlem"],
                    "Kaynak": "https://www.icisleri.gov.tr/",
                }
            return

        # ---- IL ----
        if response.url in self.start_urls:
            with open("page.html", "w") as f:
                f.write(response.text)

            start = response.text.find("var cKey") + 12
            end = start
            while not (response.text[end] == "'"):
                end = end + 1
            cKey = int(response.text[start:end])
            base_url = "/".join(response.url.split("/")[:-1])

            yield scrapy.Request(
                f"{base_url}/ISAYWebPart/CountiesList/ValilikDetay?cKey={cKey}",
                method="POST",
                callback=self.parse,
                meta={"ilId": cKey},
            )
            return

        # --- ILCE ---
        start = response.text.find("var cKey") + 12
        end = start
        while not (response.text[end] == "'"):
            end = end + 1
        cKey = int(response.text[start:end])
        base_url = "/".join(response.url.split("/")[:-1])

        yield scrapy.Request(
            f"{base_url}/ISAYWebPart/TownList/DetayGetir?id={cKey}&ilId={response.meta['ilId']}",
            method="POST",
            callback=self.parse,
            meta={"ilceId": cKey, **response.meta},
        )
