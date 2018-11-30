import json
from flask import Blueprint, render_template, request, redirect, url_for
from src.models.stores.store import Store

store_blueprint = Blueprint('stores', __name__)


@store_blueprint.route('/')
def index():
    stores = Store.all()
    return render_template('stores/store_index.jinja2', stores=stores)


@store_blueprint.route('/view_by_review/<string:order>', methods=['GET'])
def view_by_review(order, review=0):
    if order == "DESC":
        stores = Store.find_by_gte_review(review)
    else:
        stores = Store.find_by_lt_review(6)
    return render_template('stores/store_index.jinja2', stores=stores)


@store_blueprint.route('/new', methods=['GET', 'POST'])
def create_store():
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = request.form['query']
        review = request.form['review']

        Store(name, url_prefix, tag_name, query, review).save_to_db()
        return render_template('stores/store_index.jinja2', stores=Store.all())

    # What happens if it's a GET request
    return render_template("stores/new_store.jinja2")


@store_blueprint.route('/edit/<string:store_name>', methods=['GET', 'POST'])
def edit_store(store_name):
    if request.method == 'POST':
        tag_name = request.form['tag_name']
        query = request.form['query']
        review = request.form['review']

        store = Store.get_by_name(store_name)

        store.tag_name = tag_name
        store.query = query
        store.review = review

        store.save_to_db()

        return redirect(url_for('.index'))

    return render_template("stores/edit_store.jinja2", store=Store.get_by_name(store_name))


@store_blueprint.route('/<string:store_name>')
def store_page(store_name):
    return render_template('stores/store.jinja2', store=Store.get_by_name(store_name))


@store_blueprint.route('/delete/<string:store_name>')
def delete_store(store_name):
    Store.get_by_name(store_name).delete()
    return render_template('stores/store_index.jinja2', stores=Store.all())

