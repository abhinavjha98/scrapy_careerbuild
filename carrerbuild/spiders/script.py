import scrapy
import urllib
import requests

class DmozItem(scrapy.Item):
	Skill = scrapy.Field()
	Company = scrapy.Field()
	Location = scrapy.Field()
	Jobtype = scrapy.Field()
	Title = scrapy.Field()
	Description = scrapy.Field()
	Logo = scrapy.Field()
	# Merges = scrapy.Field()
	ApplyLink = scrapy.Field()
class DmozSpider(scrapy.Spider):
	name = "dmoz_carrer"
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
		logo = response.css('img.w100').xpath("@src").extract()
		cs =response.css('a.tab').xpath("@href").extract()

		# ab_url = self.BASE_URL + cs[1]
		# yield scrapy.Request(ab_url, callback=self.parse_att)
		title = response.css('h2.h3::text').extract()
		location = response.css('div.data-display-header_content div.data-details span::text').extract()
		sk=""
		item = DmozItem()
		skill = response.css('div.check-bubble::text').extract()
		location[1] = location[1].replace('Work From Home,','')
		for i in range(len(skill)):
			sk += "#"+skill[i]
		item['Company'] = location[0]
		item['Location'] = location[1]
		item['Jobtype'] = location[2]
		item['Title'] = title
		item["Logo"] = logo
		item['Skill'] = sk
		# item['Merges'] = "https://www.careerbuilder.com" + cs[1]
		item['ApplyLink'] = response.url
		aa = response.xpath("//div[@class='col-2']/descendant::text()").extract()
		# words = ["Apply to this job.\n","Think you're the perfect candidate?Apply Now\n",""]
		aa[0] = ""
		aa[1] = ""
		aa[2] = ""
		aa[3] = ""
		aa[4] = ""
		aa[5] = ""
		aa[6] = ""
		aa[7] = ""
		aa[8] = ""

		# if aa[0]:
		# 	aa = response.css('div.col-2 div.col-mobile-full p::text').extract()	
		# 	aa +=  response.css('div.seperate-bottom div.col ul strong::text').extract()
		# else:
		# 	aa = response.css('div.col-2 div.col-mobile-full::text').extract() 
		# 	aa +=  response.css('div.seperate-bottom div.col ul strong::text').extract()
		text_list=""
		for text in aa:
			text = text.rstrip("\n")
			text_list=text_list+text
		text_list = text_list.replace("    googletag.cmd.push(function() {",'')
		text_list = text_list.replace("googletag.display('div-gpt-ad-1600936971805-0'); });\n",'')
		text_list = text_list.replace("Apply to this job.\nThink you\'re the perfect candidate?Apply Now\n",'')
		text_list = text_list.replace("     $('.external-apply-email-saved').on('click', function",'')
		text_list = text_list.replace("'(event) {\n",'')
		text_list = text_list.replace("    window.ExternalApply = window.open('/interstitial'",'')
		text_list = text_list.replace("'ExternalApply-j3w31m6mxnzywkwcz8d');\n",'')
		text_list = text_list.replace("  "," ")
		item["Description"] = text_list
		return item
	# def parse_att(self, response):
	# 	item = DmozItem()
	# 	llink = response.css('a.link-cta').xpath("@href").extract()
	# 	item['ApplyLink'] = llink[0]
	# 	return item
