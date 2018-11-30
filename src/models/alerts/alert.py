import uuid
import datetime
import smtplib
from email.mime.text import MIMEText
from src.common.database import Database
import src.models.alerts.constants as AlertConstants
from src.models.items.item import Item


class Alert(object):
    def __init__(self, user_email, item_name, category, price_limit, active=True, last_check_time=None, alert_id=None, min_price=None):
        self.user_email = user_email
        self.item_name = item_name
        self.category = category
        self.price_limit = price_limit
        self.active = active
        self.last_check_time = datetime.datetime.utcnow() if last_check_time is None else last_check_time
        self.alert_id = uuid.uuid4().hex if alert_id is None else alert_id
        self.prices = []
        self.urls = []
        self.min_price = min_price
        self.load_prices()

    def __repr__(self):
        return "<Alert for user({0}) on item {1} with price_limit {2}>".format(self.user_email, self.item_name, self.price_limit)

    def send(self):
        print("start to send eamil\n")
        msg = MIMEText("We've found a deal!")
        msg['Subject'] = "Price limit reached for Category {0} Item {1}".format(self.category, self.item_name)
        msg['From'] = AlertConstants.LOGIN
        msg['To'] = self.user_email

        s = smtplib.SMTP('smtp.mailgun.org', 587)

        s.login(AlertConstants.LOGIN, AlertConstants.API_KEY)
        s.sendmail(msg['From'], msg['To'], msg.as_string())
        s.quit()

    @classmethod
    def find_needing_update(cls, minutes_since_update=AlertConstants.ALERT_TIMEOUT):
        last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes_since_update)
        query = "SELECT * FROM alerts WHERE active AND last_check_time < \'{}\'".format(last_updated_limit)
        return [cls(**elem) for elem in Database.do(query)]

    def save_to_db(self):
        query = "SELECT * FROM alerts WHERE user_email = \'{0}\' AND alert_id = \'{1}\'".format(self.user_email, self.alert_id)
        alert_data = Database.find_one(query)

        if alert_data is None:
            cmd = "INSERT INTO alerts(alert_id, user_email, item_name, category, price_limit, active, last_check_time, min_price)\
                   VALUES (\'{0}\', \'{1}\', \'{2}\', \'{3}\', {4}, {5}, \'{6}\', {7})"\
                   .format(self.alert_id, self.user_email, self.item_name, self.category, self.price_limit, self.active,\
                           self.last_check_time, 'NULL' if self.min_price is None else self.min_price)
            Database.do(cmd)
        else:
            cmd = "UPDATE alerts SET price_limit = {0}, active = {1}, last_check_time = \'{2}\', min_price = {3} WHERE user_email = \'{4}\' AND alert_id = \'{5}\'"\
                  .format(self.price_limit, self.active, self.last_check_time, self.min_price , self.user_email, self.alert_id)
            Database.do(cmd)

    def load_prices(self):
        prices = []
        urls = []
        item_data = Item.get_by_name(self.item_name, self.category)
        for item in item_data:
            prices.append(item.price)
            urls.append(item.url)
            print(prices)
        self.prices = prices.copy()
        self.urls = urls.copy()
        return prices

    def load_item_price(self):
        min = -1
        item_data = Item.get_by_name(self.item_name, self.category)
        for item in item_data:
            price = item.load_price()
            if price < min or min < 0:
                min = price
            item.save_to_db()
        self.last_check_time = datetime.datetime.utcnow()
        self.min_price = min
        self.save_to_db()
        return min

    def send_email_if_price_reached(self):
        if self.min_price < self.price_limit:
            self.send()

    @classmethod
    def find_by_user_email(cls, user_email):
        query = "SELECT * FROM alerts WHERE user_email = \'{}\'".format(user_email)
        return [cls(**elem) for elem in Database.do(query)]

    @classmethod
    def find_by_id(cls, user_email, alert_id):
        query = "SELECT * FROM alerts WHERE user_email = \'{}\' AND alert_id = \'{}\'".format(user_email, alert_id)
        return cls(**Database.find_one(query))

    def deactivate(self):
        self.active = False
        self.save_to_db()

    def activate(self):
        self.active = True
        self.save_to_db()

    def delete(self):
        cmd = "DELETE FROM alerts WHERE user_email = \'{0}\' AND alert_id = \'{1}\'".format(self.user_email, self.alert_id)
        Database.do(cmd)
