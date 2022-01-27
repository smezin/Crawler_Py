from flask_restful import Resource, reqparse

from models.url_scrape import UrlScrapeModel

class UrlScrape(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('base_url_to_scrape', type=str, required=True, help='provide url to scrape')
    parser.add_argument('parent', type=str, required=False, help='optional')
    parser.add_argument('depth', type=int, required=True, help='provide scrape depth')

    def post(self):
        data = UrlScrape.parser.parse_args()
        #print(data)
        url_scrape_model = UrlScrapeModel(**data)
        print(url_scrape_model.json())
        return(url_scrape_model.json())