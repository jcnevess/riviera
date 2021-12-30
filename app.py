# coding: utf-8

from flask.wrappers import Response
import storage

from flask import Flask, request, jsonify, url_for, make_response
from markupsafe import escape

app = Flask(__name__)

@app.route('/guest', methods=['GET', 'POST'])
def guest():
    if request.method == 'GET':
        return jsonify(storage.guest_getall())
    elif request.method == 'POST':
        storage.guest_add(request.form['name'], request.form['social_number'], \
                request.form['birthdate'], request.form['address_street'], request.form['address_number'], \
                request.form['address_additional_info'], request.form['address_neighborhood'], \
                request.form['address_zipcode'], request.form['address_city'], request.form['address_state'], \
                request.form['address_country'], request.form['credit_card_number'])

        response = make_response('Resource Created', 201)
        response.headers['Location'] = url_for('guest_by_id', id = request.form['social_number'])
        return response

# using ssn as id for now
@app.route('/guest/<id>', methods=['GET', 'PUT'])
def guest_by_id(id):
    if request.method == 'GET':
        return jsonify(storage.guest_getbyid(id))
    elif request.method == 'PUT':
        storage.guest_edit(id, request.form['name'], request.form['social_number'], \
                request.form['birthdate'], request.form['address_street'], request.form['address_number'], \
                request.form['address_additional_info'], request.form['address_neighborhood'], \
                request.form['address_zipcode'], request.form['address_city'], request.form['address_state'], \
                request.form['address_country'], request.form['credit_card_number'])
        
        response = make_response('Resource Updated', 200)
        response.headers['Location'] = url_for('guest_by_id', id = request.form['social_number'])
        return response