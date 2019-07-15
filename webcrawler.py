import scrapy
import cfscrape
from scrapy import Request

class ZoneSpider(scrapy.Spider):
	name = "links"
	start_url =	'example.url'
    

	def start_requests(self):
	    cf_requests = []
	    for url in self.start_urls:
	      token, agent = cfscrape.get_tokens(url, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
	      cf_requests.append(Request(url=url,
	                      cookies=token,
	                      headers={'User-Agent': agent}))
	    return cf_requests

	def parse(self, response):
		allSubpages = []
		for target in response.css('a.cvplbd'):
			if target.css('a::attr("href")').extract_first():
					allSubpages.append(target.css('a::attr("href")').extract_first());
		temp = set(allSubpages)
		subpages = list(temp)

		for page in subpages:
			token, agent = cfscrape.get_tokens(page, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
			yield scrapy.Request(
				url = page,
				cookies = token,
				headers={'User-Agent': agent},
				callback = self.subParse,
				dont_filter = True
			)

		#for page in subpages:
		#	if page is not None:
		#		response.follow(page, self.subParse)

		yield{ "spacing" : 'spacing'}

		next_page = response.css('ul.pt-cv-pagination li.active + li a::attr("href")').extract_first()
		if next_page is not None:
			token, agent = cfscrape.get_tokens(page, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
			yield scrapy.Request(
				url = start_url + next_page,
				cookies = token,
				headers={'User-Agent': agent},
				callback = self.parse,
				dont_filter = True
			)

	def subParse(self, response):
		for res in response.css('div.post-content a::attr("href")'):
			yield { 'link': res.extract()}