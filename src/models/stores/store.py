from src.common.database import Database


class Store(object):
    def __init__(self, name, url_prefix, tag_name, query, review):
        self.name = name                # PRIMARY KEY
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self.review = review

    def __repr__(self):
        return "<Store {}>".format(self.name)

    def delete(self):
        cmd = "DELETE FROM stores WHERE name = \'{}\'".format(self.name)
        Database.do(cmd)

    @classmethod
    def all(cls):
        query = "SELECT * FROM stores"
        return [cls(**elem) for elem in Database.do(query)]

    def save_to_db(self):
        print(self.query)
        query = "SELECT * FROM stores WHERE name = \'{}\'".format(self.name)
        store_data = Database.find_one(query)

        if store_data is None:
            cmd = "INSERT INTO stores(name, url_prefix, tag_name, query, review)\
                   VALUES (\'{0}\', \'{1}\', \'{2}\', \'{3}\', {4})"\
                  .format(self.name, self.url_prefix, self.tag_name, self.query, self.review)
            Database.do(cmd)
        else:
            cmd = "UPDATE stores SET tag_name = \'{0}\', query = \'{1}\', review = {2} WHERE name = \'{3}\'"\
                  .format(self.tag_name, self.query, self.review, self.name)
            Database.do(cmd)

    @classmethod
    def find_by_gte_review(cls, preferred_review):
        query = "SELECT * FROM stores WHERE review >= \'{}\' ORDER BY review DESC".format(preferred_review)
        return [cls(**elem) for elem in Database.do(query)]

    @classmethod
    def find_by_lt_review(cls, preferred_review):
        query = "SELECT * FROM stores WHERE review < \'{}\' ORDER BY review".format(preferred_review)
        return [cls(**elem) for elem in Database.do(query)]

    @classmethod
    def get_by_name(cls, store_name):
        query = "SELECT * FROM stores WHERE name = \'{}\'".format(store_name)
        return cls(**Database.find_one(query))

    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        query = "SELECT * FROM stores WHERE url_prefix = \'{}\'".format(url_prefix)
        return cls(**Database.find_one(query))

    @classmethod
    def find_by_url(cls, url):
        store_data = cls.all()
        for store in store_data:
            if store.url_prefix in url:
                return store
