import os
from flask import Flask, render_template
from src.common.database import Database

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.config.from_object('src.config')
app.secret_key = "123"


@app.before_first_request
def init_db():
    Database.initialize()


'''
@app.teardown_request
def teardown_request(exception):
    Database.close()
'''


@app.route('/')
def home():
    return render_template('home.jinja2')


from src.models.users.views import user_blueprint
from src.models.stores.views import store_blueprint
from src.models.alerts.views import alert_blueprint
from src.models.addresses.views import address_blueprint
app.register_blueprint(address_blueprint, url_prefix="/addresses")
app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(store_blueprint, url_prefix="/stores")
app.register_blueprint(alert_blueprint, url_prefix="/alerts")
