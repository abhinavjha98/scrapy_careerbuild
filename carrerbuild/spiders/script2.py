import scrapy
import urllib
import requests

class DmozItem(scrapy.Item):
	CoIndustry = scrapy.Field()
	CoWebsite = scrapy.Field()
	Merges = scrapy.Field()

class DmozSpider(scrapy.Spider):
	name = "dmoz_website"
	page_numbers = 2
	start_urls = [
    'https://www.careerbuilder.com/jobs?utf8=%E2%9C%93&keywords=&location=Pagosa+Springs%2C+CO'
    ]
	BASE_URL = 'https://www.careerbuilder.com'

	def parse(self, response):
		links = response.css('a.data-results-content').xpath("@href").extract()
		for link in links:
			absolute_url = self.BASE_URL + link
			yield scrapy.Request(absolute_url, callback=self.parse_attr)
		next_page = "https://www.careerbuilder.com/jobs?keywords=&location=Pagosa+Springs%2C+CO&page_number="+str(DmozSpider.page_numbers)

		if DmozSpider.page_numbers<=91:
			DmozSpider.page_numbers +=1
			yield response.follow(next_page,callback=self.parse)
	def parse_attr(self, response):
		item = DmozItem()
		cs =response.css('a.tab').xpath("@href").extract()
		ab_url = self.BASE_URL + cs[1]
		yield scrapy.Request(ab_url, callback=self.parse_att)

		return item
	def parse_att(self, response):
		item = DmozItem()
		llink = response.css('a.link-cta').xpath("@href").extract()
		co_indu = response.css('div.data-details span::text').extract()
		item['Merges'] = response.url
		item['CoIndustry'] = co_indu[1]
		item['CoWebsite'] = llink[1]
		return item
