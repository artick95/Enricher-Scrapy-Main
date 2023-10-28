import scrapy
from scrapy.linkextractors import LinkExtractor
import re

class InstaSpider(scrapy.Spider):
    name = 'instaspider'
    
    start_urls = [line.strip() for line in open('urlsPart2.txt').readlines()]

    custom_settings = {
        'CONCURRENT_REQUESTS': 30,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 2,
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        }
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={
                'proxy': 'http://artick:mikeislao_country-us_streaming-1@geo.iproyal.com:12321'
            })

    def parse(self, response):
        le = LinkExtractor(allow=(r'instagram\.com', r'linkedin\.com', r'whatsapp\.com', r'twitter\.com', r'youtube\.com', r'mailto:', r'tel:'))
        links = {
            'URL': response.url,
            'Phone': []
        }

        # Extract phone numbers
        try:
            phone_links = response.css('a[href^="tel:"]::attr(href)').getall()
            links['Phone'] += [phone.split("tel:")[1] for phone in phone_links]
        except Exception as e:
            self.logger.error(f"Error extracting phone numbers from {response.url}. Error: {e}")

        # Extract and clean emails
        emails = set()
        email_links = response.css('a[href^="mailto:"]::attr(href)').getall()
        for email in email_links:
            emails.add(email.split("mailto:")[1])

        email_re = r'[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*'
        email_links_regex = re.findall(email_re, response.text)
        for email in email_links_regex:
            if not email.startswith("wght@") and "@" in email:
                emails.add(email)

        # Assign the best email and up to 6 additional emails
        emails = list(emails)
        links['best_email'] = emails[0] if emails else ""
        for i, email in enumerate(emails[1:7], start=1):
            links[f'email{i}'] = email

        # Convert lists to strings for CSV
        for key, value in links.items():
            if isinstance(value, list):
                links[key] = ', '.join(value)

        yield links
