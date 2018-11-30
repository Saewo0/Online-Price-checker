import datetime
from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as UserErrors
from src.models.alerts.alert import Alert
from src.models.addresses.address import Address


class User(object):
    def __init__(self, email, password, name, age=None, isvip=None, expire_date=None, list_limit=None):
        self.email = email
        self.password = password
        self.name = name
        self.age = age
        self.isvip = False if isvip is None else isvip
        self.expire_date = datetime.datetime.utcnow() if expire_date is None else expire_date
        self.list_limit = 3 if list_limit is None else list_limit

    def __repr__(self):
        return "<User {}>".format(self.email)

    @classmethod
    def find_by_email(cls, email):
        query = "SELECT * FROM appusers WHERE email = \'{}\'".format(email)
        if query:
            return cls(**Database.find_one(query))
        else:
            return None

    @staticmethod
    def is_login_valid(email, password):
        query = "SELECT * FROM appusers WHERE email = \'{}\'".format(email)
        user_data = Database.find_one(query)  # Password in sha512 -> pbkdf2_sha512
        if user_data is None:
            # Tell the user that their e-mail doesn't exist
            raise UserErrors.UserNotExistsError("Your user does not exist.")
        if not Utils.check_hashed_password(password, user_data['password']):
            # Tell the user that their password is wrong
            raise UserErrors.IncorrectPasswordError("Your password was wrong.")

        return True

    @staticmethod
    def register_user(email, password, name, age):
        query = "SELECT * FROM appusers WHERE email = \'{}\'".format(email)
        user_data = Database.find_one(query)

        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("The e-mail you used to register already exists.")
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("The e-mail does not have the right format.")

        User(email, Utils.hash_password(password), name, age).save_to_db()

        return True

    def save_to_db(self):
        cmd = "INSERT INTO appusers(email, password, name, age, isvip, expire_date, list_limit)\
               VALUES (\'{0}\', \'{1}\', \'{2}\', {3}, {4}, \'{5}\', {6})"\
               .format(self.email, self.password, self.name, self.age, self.isvip, self.expire_date, self.list_limit)
        Database.do(cmd)

    def get_alerts(self):
        return Alert.find_by_user_email(self.email)

    def get_addresses(self):
        return Address.find_by_user_email(self.email)
