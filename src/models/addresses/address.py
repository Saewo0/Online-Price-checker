import uuid
from src.common.database import Database


class Address(object):
    def __init__(self, user_email, room, street, city, state, zip_code, phone, address_id=None):
        self.user_email = user_email
        self.room = room
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.phone = phone
        self.address_id = uuid.uuid4().hex if address_id is None else address_id

    def __repr__(self):
        return "<Address({0}) for user({1})>".format(self.address_id, self.user_email)

    def save_to_db(self):
        query = "SELECT * FROM address WHERE user_email = \'{0}\' AND address_id = \'{1}\'".format(self.user_email, self.address_id)
        address_data = Database.find_one(query)

        if address_data is None:
            cmd = "INSERT INTO address(address_id, user_email, room, street, city, state, zip_code, phone)\
                   VALUES (\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\', \'{6}\', {7})"\
                   .format(self.address_id, self.user_email, self.room, self.street, self.city, self.state,\
                           self.zip_code, self.phone)
            Database.do(cmd)

    @classmethod
    def find_by_user_email(cls, user_email):
        query = "SELECT * FROM address WHERE user_email = \'{}\'".format(user_email)
        return [cls(**elem) for elem in Database.do(query)]

    @classmethod
    def find_by_id(cls, user_email, address_id):
        query = "SELECT * FROM address WHERE user_email = \'{}\' AND address_id = \'{}\'".format(user_email, address_id)
        return cls(**Database.find_one(query))

    def delete(self):
        cmd = "DELETE FROM address WHERE user_email = \'{0}\' AND address_id = \'{1}\'".format(self.user_email, self.address_id)
        Database.do(cmd)
