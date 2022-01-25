# Import libraries
from urllib.request import urljoin
from bs4 import BeautifulSoup
import requests
import json
from urllib.request import urlparse
from helpers.message_wrapper import send_message
from helpers.queue_wrapper import get_queue
from consts import SQS_NAME
from models.url_scrape import UrlScrapeModel



# Set for storing urls with same domain
links_intern = set()
input_url = "https://www.google.com/"
depth = 2

# Set for storing urls with different domain
links_extern = set()


# Method for crawling a url at next level
def level_crawler(input_url: str, depth: int):
	temp_urls = set()
	current_url_domain = urlparse(input_url).netloc

	# Creates beautiful soup object to extract html tags
	try:
		beautiful_soup_object = BeautifulSoup(
			requests.get(input_url).content, "html.parser")
	except:
		print('soup error')


	queue = get_queue(SQS_NAME)
	# Access all anchor tags from input
	# url page and divide them into internal
	# and external categories
	for anchor in beautiful_soup_object.findAll("a"):
		href = anchor.attrs.get("href")
		if(href != "" or href != None):
			href = urljoin(input_url, href)
			href_parsed = urlparse(href)
			href = href_parsed.scheme
			href += "://"
			href += href_parsed.netloc
			href += href_parsed.path
			final_parsed_href = urlparse(href)
			is_valid = bool(final_parsed_href.scheme) and bool(final_parsed_href.netloc)
			if is_valid:
				url_scrape = UrlScrapeModel(href, input_url, depth)
				send_message(queue, json.dumps(url_scrape.json()))
				if current_url_domain not in href and href not in links_extern:
					print("Extern - {} - depth {}".format(href, depth))
					links_extern.add(href)
				if current_url_domain in href and href not in links_intern:
					print("Intern - {} - depth {}".format(href, depth))
					links_intern.add(href)
					temp_urls.add(href)
	return temp_urls


if(depth == 0):
	print("Intern - {}".format(input_url))

elif(depth == 1):
	level_crawler(input_url, 1)

else:
	# We have used a BFS approach
	# considering the structure as
	# a tree. It uses a queue based
	# approach to traverse
	# links upto a particular depth.
	queue = []
	queue.append(input_url)
	for level in range(depth):
		print('scanning level: {}'.format(level))
		for count in range(len(queue)):
			url = queue.pop(0)
			urls = level_crawler(url, level)
			for i in urls:
				queue.append(i)
