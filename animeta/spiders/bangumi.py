import scrapy


class BangumiSpider(scrapy.Spider):
    name = "bangumi"

    def start_requests(self):
        urls = [
            'https://bangumi.tv/anime/browser?sort=rank&page=1',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for each in response.css("div.section").css("div.inner"):
            yield {
                "title": each.css("a::text").get(),
                "score": each.css("p.rateInfo").css("small.fade::text").get(),
            }
            
        if len(response.css("div.section").css("div.inner")):
             next_page = response.urljoin(response.css("div.page_inner").css("a.p::attr(href)")[-2].get())
             yield scrapy.Request(next_page, callback=self.parse)
