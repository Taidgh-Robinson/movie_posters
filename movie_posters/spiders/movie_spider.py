import scrapy
import re

class movie_spider(scrapy.Spider):
    name = 'movie' 
    
    start_urls = ['https://www.imdb.com/search/title?groups=top_1000&sort=user_rating&view=simple']

    def parse(self, response):
        
        #Follow the movie link, downloaded with the parse_page method
        for movie in response.css('.col-title span a::attr(href)'):
            print(movie)
            yield response.follow(movie, self.parse_page)

        #Yield the next page, used [-1] because the first link leads back on all pages except the first. 
        yield response.follow(response.css('.desc a::attr(href)').extract()[-1], self.parse)

    def parse_page(self, response):

        #The link on each page was to the lower resolution version, but it was a simple pattern solved with regex
        low_res = response.css('.poster img::attr(src)').extract_first()
        filt = re.compile('^.*?(?=V1_)')
        high_res = filt.findall(low_res)[0] + 'V1_.jpg'
        title = response.css('.title_wrapper h1::text').extract_first()[:-1]

        yield { 'title' : title, 'image_urls': [high_res] } 
