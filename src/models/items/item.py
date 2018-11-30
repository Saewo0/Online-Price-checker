from bs4 import BeautifulSoup
import requests
import re
from src.common.database import Database
from src.models.stores.store import Store


class Item(object):
    def __init__(self, url, name, category, price=None):
        self.url = url
        self.name = name
        self.category = category
        self.price = None if price is None else price
        store = Store.find_by_url(url)
        self.tag_name = store.tag_name
        self.query = store.query

    def __repr__(self):
        return "<Category {0}: Item {1} with URL {2}>".format(self.category, self.name, self.url)

    def load_price(self):
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "lxml")
        #print("print soup...")
        #print(soup)
        element = soup.find(self.tag_name, self.query)
        #print("print element...")
        #print(element)
        string_price = element.text.strip().replace(',', '')
        #print("print string_price...")
        #print(string_price)

        pattern = re.compile("(\d+\.*\d*)")
        match = pattern.search(string_price)
        self.price = float(match.group())

        return self.price

    def save_to_db(self):
        query = "SELECT * FROM items WHERE url = \'{}\'".format(self.url)
        item_data = Database.find_one(query)

        if item_data is None:
            cmd = "INSERT INTO items(url, name, category, price)\
                   VALUES (\'{0}\', \'{1}\', \'{2}\', {3})" \
                   .format(self.url, self.name, self.category, 'NULL' if self.price is None else self.price)
            Database.do(cmd)
        else:
            print("The {0} with url({1}) already exists! Update info...\n".format(self.name, self.url))
            cmd = "UPDATE items SET price = {0} WHERE url = \'{1}\'".format('NULL' if self.price is None else self.price, self.url)
            Database.do(cmd)

    @classmethod
    def get_by_name(cls, name, category):
        query = "SELECT * FROM items  WHERE name = \'{0}\' AND category = \'{1}\'".format(name, category)
        return [cls(**elem) for elem in Database.do(query)]

    @classmethod
    def get_by_url(cls, url):
        query = "SELECT * FROM items  WHERE url = \'{}\'".format(url)
        return cls(**Database.find_one(query))
