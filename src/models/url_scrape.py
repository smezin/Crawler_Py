from typing import Dict, List, Union
from db import db

UrlScrapeJSON = Dict[str, Union[int, str]]
class UrlScrapeModel():
    # __tablename__ = "urls"
    # my_url = db.Column(db.String(255), primary_key=True)
    # parent = db.Column(db.String(255), nullable=True)
    # title = db.Column(db.String(255), nullable=True)
    # depth = db.Column(db.Integer, nullable=True)

    def __init__(self, base_url_to_scrape: str, parent: str, depth: int):
        self.my_url = base_url_to_scrape
        self.parent_url = parent
        self.depth = depth
        self.title = None

    def json(self) -> UrlScrapeJSON:
        return {
            "my_url": self.my_url,
            "parent_url": self.parent_url,
            "title": self.title,
            "depth": self.depth
        }

    def save_to_db(self) -> None:
            db.session.add(self)
            db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
