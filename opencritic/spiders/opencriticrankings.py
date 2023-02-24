from scrapy import Request, Spider


class OpenCriticRankingsSpider(Spider):
    name = "opencriticrankings"

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.pages = int(kwargs.get("pages", 10))

    def start_requests(self):
        for i in range(1, self.pages + 1):
            yield Request(f"https://opencritic.com/browse/all?page={i}")

    def parse(self, response):
        for row in response.xpath(".//div[contains(@class, 'py-2 game-row')]"):
            yield self.parse_game(row)

    def parse_game(self, game):
        result = {}
        result["title"] = game.css("div > a::text").get()
        result["opencritic_score"] = game.xpath(".//app-tier-display/img/@alt").get()
        result["platforms"] = game.xpath(".//div[contains(@class, 'platforms')]/text()").get("").strip().split(",")
        result["release_date"] = game.css("div > div > span::text").get("").strip()
        result["score"] = game.xpath(".//div[contains(@class, 'score')]/text()").get()
        result["url"] = "https://opencritic.com" + game.css("div > a::attr(href)").get()
        return result
