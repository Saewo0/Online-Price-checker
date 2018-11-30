from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
from src.models.users.user import User
from src.models.alerts.alert import Alert
import src.models.users.errors as UserErrors
import src.models.users.decorators as user_decorators


user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for(".user_alerts"))
        except UserErrors.UserError as e:
            return e.message

    return render_template("users/login.jinja2")  # Send the user an error if their login was invalid


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        age = request.form['age']

        try:
            if User.register_user(email, password, name, age):
                session['email'] = email
                return redirect(url_for(".user_alerts"))
        except UserErrors.UserError as e:
            return e.message

    return render_template("users/register.jinja2")  # Send the user an error if their login was invalid


@user_blueprint.route('/alerts')
@user_decorators.requires_login
def user_alerts():
    user = User.find_by_email(session['email'])
    alert_data = user.get_alerts()
    for alert in alert_data:
        if alert.active:
            alert.load_item_price()
            alert.save_to_db()
    return render_template("users/alerts.jinja2", alerts=user.get_alerts(), user=user)


@user_blueprint.route('/addresses')
@user_decorators.requires_login
def user_addresses():
    user = User.find_by_email(session['email'])
    return render_template("users/addresses.jinja2", addresses=user.get_addresses())


@user_blueprint.route('/check&send')
@user_decorators.requires_login
def check_and_send():
    alerts_needing_update = Alert.find_needing_update()
    for alert in alerts_needing_update:
        alert.load_item_price()
        alert.send_email_if_price_reached()
    return render_template('home.jinja2')


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))
