from flask import Blueprint, request, render_template, session, redirect, url_for
from src.models.addresses.address import Address
import src.models.users.decorators as user_decorators

address_blueprint = Blueprint('addresses', __name__)


@address_blueprint.route('/new', methods=['GET', 'POST'])
@user_decorators.requires_login
def create_address():
    if request.method == 'POST':
        room = request.form['room']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']
        phone = request.form['phone']

        address = Address(session['email'], room, street, city, state, zip_code, phone)
        address.save_to_db()
        return redirect(url_for('users.user_addresses'))

    return render_template("addresses/new_address.jinja2")


@address_blueprint.route('/delete/<string:address_id>')
@user_decorators.requires_login
def delete_address(address_id):
    Address.find_by_id(session['email'], address_id).delete()
    return redirect(url_for('users.user_addresses'))
