from flask import Blueprint, request, render_template, session, redirect, url_for
from src.models.alerts.alert import Alert
from src.models.items.item import Item
import src.models.users.decorators as user_decorators
from src.models.users.user import User

alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route('/new', methods=['GET', 'POST'])
@user_decorators.requires_login
def create_alert():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        url = request.form['url']
        price_limit = float(request.form['price_limit'])

        item = Item(url, name, category)
        item.save_to_db()

        item = Item.get_by_url(url)

        alert = Alert(session['email'], item.name, item.category, price_limit)
        alert.load_item_price()
        user = User.find_by_email(session['email'])
        return render_template("users/alerts.jinja2", alerts=user.get_alerts(), user=user)

    return render_template("alerts/new_alert.jinja2")  # Send the user an error if their login was invalid


@alert_blueprint.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
@user_decorators.requires_login
def edit_alert(alert_id):
    if request.method == 'POST':
        price_limit = float(request.form['price_limit'])

        alert = Alert.find_by_id(session['email'], alert_id)
        alert.price_limit = price_limit
        alert.load_item_price()
        user = User.find_by_email(session['email'])
        return render_template("users/alerts.jinja2", alerts=user.get_alerts(), user=user)

    return render_template("alerts/edit_alert.jinja2", alert=Alert.find_by_id(session['email'], alert_id))


@alert_blueprint.route('/deactivate/<string:alert_id>')
@user_decorators.requires_login
def deactivate_alert(alert_id):
    Alert.find_by_id(session['email'], alert_id).deactivate()
    user = User.find_by_email(session['email'])
    return render_template("users/alerts.jinja2", alerts=user.get_alerts(), user=user)


@alert_blueprint.route('/activate/<string:alert_id>')
@user_decorators.requires_login
def activate_alert(alert_id):
    Alert.find_by_id(session['email'], alert_id).activate()
    user = User.find_by_email(session['email'])
    return render_template("users/alerts.jinja2", alerts=user.get_alerts(), user=user)


@alert_blueprint.route('/delete/<string:alert_id>')
@user_decorators.requires_login
def delete_alert(alert_id):
    Alert.find_by_id(session['email'], alert_id).delete()
    user = User.find_by_email(session['email'])
    return render_template("users/alerts.jinja2", alerts=user.get_alerts(), user=user)


@alert_blueprint.route('/<string:alert_id>')
@user_decorators.requires_login
def get_alert_page(alert_id):
    return render_template('alerts/alert.jinja2', alert=Alert.find_by_id(session['email'], alert_id))


@alert_blueprint.route('/check_price/<string:alert_id>')
def check_alert_price(alert_id):
    Alert.find_by_id(session['email'], alert_id).load_item_price()
    return redirect(url_for('.get_alert_page', alert_id=alert_id))
