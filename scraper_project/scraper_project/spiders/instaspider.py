import scrapy
from scrapy.linkextractors import LinkExtractor
import re

class InstaSpider(scrapy.Spider):
    name = 'instaspider'
    
    start_urls = [line.strip() for line in open('urls.txt').readlines()]

    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'DOWNLOAD_TIMEOUT': 30,
        'CONCURRENT_REQUESTS': 5,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 2,
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        }
    }

    #def start_requests(self):
    #    for url in self.start_urls:
    #        yield scrapy.Request(url, callback=self.parse, meta={
    #            'proxy': 'http://32ef0ea76be983130f00e07286630352:ce8dd80b0923103068b04b5b207974e1@199.189.86.111:9500'
    #        })
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={
            })

    def parse(self, response):
        le = LinkExtractor(allow=(r'instagram\.com', r'linkedin\.com', r'whatsapp\.com', r'twitter\.com', r'youtube\.com', r'mailto:', r'tel:'))
        links = {
            'URL': response.url,
            'Instagram': [],
            'LinkedIn': [],
            'WhatsApp': [],
            'Twitter': [],
            'YouTube': [],
            'Email': [],
            'Phone': []
        }

        for link in le.extract_links(response):
            if 'instagram.com' in link.url:
                links['Instagram'].append(link.url)
            elif 'linkedin.com' in link.url:
                links['LinkedIn'].append(link.url)
            elif 'whatsapp.com' in link.url:
                links['WhatsApp'].append(link.url)
            elif 'twitter.com' in link.url:
                links['Twitter'].append(link.url)
            elif 'youtube.com' in link.url:
                links['YouTube'].append(link.url)
            try:
                phone_links = response.css('a[href^="tel:"]::attr(href)').getall()
                links['Phone'] += [phone.split("tel:")[1] for phone in phone_links]
            except Exception as e:
                self.logger.error(f"Error extracting phone numbers from {response.url}. Error: {e}")

            try:
                email_links = response.css('a[href^="mailto:"]::attr(href)').getall()
                links['Email'] += [email.split("mailto:")[1] for email in email_links]
            except Exception as e:
                self.logger.error(f"Error extracting emails from {response.url}. Error: {e}")



        # Convert lists to strings for CSV
        for key, value in links.items():
            if isinstance(value, list):
                links[key] = ', '.join(value)

        
        yield links
