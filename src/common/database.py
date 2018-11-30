from sqlalchemy import *


class Database(object):
    DB_USER = "xz2732"
    DB_PASSWORD = "5iuk9amo"
    DB_SERVER = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"
    DATABASEURI = "postgresql://" + DB_USER + ":" + DB_PASSWORD + "@" + DB_SERVER + "/w4111"
    DATABASE = None

    @staticmethod
    def initialize():
        """
        This function is run at the beginning of every web request
        (every time you enter an address in the web browser).
        We use it to setup a database connection that can be used throughout the request
        """
        engine = create_engine(Database.DATABASEURI)
        try:
            Database.DATABASE = engine.connect()
        except:
            print("uh oh, problem connecting to database")
            import traceback
            traceback.print_exc()
            Database.DATABASE = None

    @staticmethod
    def close():
        """
        At the end of the web request, this makes sure to close the database connection.
        If you don't the database could run out of memory!
        """
        try:
            Database.DATABASE.close()
        except Exception as e:
            print(e)
            pass

    @staticmethod
    def find_one(query):
        return Database.DATABASE.execute(query).fetchone()

    @staticmethod
    def do(query):
        return Database.DATABASE.execute(query)
