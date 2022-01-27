
from flask import Flask
from flask_restful import Api
#from crawler import level_crawler
from helpers.queue_wrapper import get_queue, create_queue
from consts import SQS_NAME
from resources.url_scrape import UrlScrape

app = Flask(__name__)
api = Api(app)

api.add_resource(UrlScrape, '/scrapeq')
app.run(port=5000, debug=True)

#level_crawler('https://google.com/', 2, SQS_NAME)