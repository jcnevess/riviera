# coding: utf-8

from storage import Storage
from flask import Flask, request, jsonify, url_for, make_response
from distutils.util import strtobool

app = Flask(__name__)
storage = Storage()


# TODO: Routes should be in the plural
@app.route('/guest', methods=['GET', 'POST'])
def guest():
    if request.method == 'GET':
        return jsonify(list(map(lambda i: i.to_json(), storage.guest_getall())))
    elif request.method == 'POST':
        form = request.form
        storage.guest_add(form['name'], form['social_number'], form['birthdate'], form['address_street'], form['address_number'],
                          form['address_additional_info'], form['address_neighborhood'], form['address_zipcode'], form['address_city'],
                          form['address_state'], form['address_country'])

        response = make_response('Resource Created', 201)
        response.headers['Location'] = url_for('guest_by_id', id=form['social_number'])
        return response


# using ssn as id for now
@app.route('/guest/<id>', methods=['GET', 'PUT'])
def guest_by_id(id):
    if request.method == 'GET':
        return jsonify(storage.guest_getbyid(id).to_json())
    elif request.method == 'PUT':
        form = request.form
        storage.guest_edit(id, form['name'], form['social_number'], form['birthdate'], form['address_street'],
                           form['address_number'], form['address_additional_info'], form['address_neighborhood'],
                           form['address_zipcode'], form['address_city'], form['address_state'], form['address_country'])

        response = make_response('Resource Updated', 200)
        response.headers['Location'] = url_for('guest_by_id', id=form['social_number'])
        return response


# TODO: Service routes should receive their contracts in the url
@app.route('/service', methods=['GET', 'POST'])
def service():
    if request.method == 'GET':
        return jsonify(list(map(lambda s: s.to_json(), storage.service_getall())))
    elif request.method == 'POST':
        form = request.form
        service_type = form['service_type']
        id = -1

        if service_type == 'room_rental':
            id = storage.service_add_room(form['contract_id'], form['rental_type'], bool(strtobool(form['additional_bed'])), form['days'])
        elif service_type == 'car_rental':
            id = storage.service_add_car(form['contract_id'], form['rental_type'], form['car_plate'], bool(strtobool(form['full_gas'])),
                                         bool(strtobool(form['car_insurance'])), form['days'])
        elif service_type == 'babysitter':
            id = storage.service_add_babysitter(form['contract_id'], form['normal_hours'], form['extra_hours'])
        elif service_type == 'meal':
            id = storage.service_add_meal(form['contract_id'], form['value'], form['description'])
        elif service_type == 'extra_service':
            id = storage.service_add_extra(form['contract_id'], form['value'], form['description'])

        response = make_response('Resource created', 201)
        response.headers['Location'] = url_for('service_by_id', id=id)
        return response


@app.route('/service/<id>', methods=['GET', 'PUT', 'DELETE'])
def service_by_id(id):
    if request.method == 'GET':
        return jsonify(storage.service_getbyid(id).to_json())

    elif request.method == 'DELETE':
        storage.service_delete(id)
        return make_response('Resource deleted', 200)

    elif request.method == 'PUT':
        form = request.form
        service_type = form['service_type']

        if service_type == 'room_rental':
            storage.service_edit_room(id, form['contract_id'], form['rental_type'], bool(strtobool(form['additional_bed'])), form['days'])
        elif service_type == 'car_rental':
            storage.service_edit_car(id, form['contract_id'], form['rental_type'], form['car_plate'], bool(strtobool(form['full_gas'])),
                                         bool(strtobool(form['car_insurance'])), form['days'])
        elif service_type == 'babysitter':
            storage.service_edit_babysitter(id, form['contract_id'], form['normal_hours'], form['extra_hours'])
        elif service_type == 'meal':
            storage.service_edit_meal(id, form['contract_id'], form['value'], form['description'])
        elif service_type == 'extra_service':
            storage.service_edit_extra(id, form['contract_id'], form['value'], form['description'])

        return make_response('Resource updated', 200)


# @app.route('/service/<service_id>/price', methods=['GET'])
# def service_price(service_id: str):
#     return storage.service_get_price(service_id)


@app.route('/contract', methods=['GET', 'POST'])
def contract():
    if request.method == 'GET':
        return jsonify(list(map(lambda c: c.to_json(), storage.contract_getall())))
    elif request.method == 'POST':
        form = request.form
        id = storage.contract_add(form['guest_id'], form['card_number'], form['checkin_date'], form['days_contracted'])
        response = make_response('Resource created', 201)
        response.headers['Location'] = url_for('contract_by_id', id=id)
        return response


@app.route('/contract/<id>', methods=['GET', 'PUT', 'DELETE'])
def contract_by_id(id: str):
    if request.method == 'GET':
        return jsonify(storage.contract_getbyid(id).to_json())
    elif request.method == 'PUT':
        form = request.form
        storage.contract_edit(id, form['guest_id'], form['card_number'], form['checkin_date'],
                              form['days_contracted'], bool(strtobool(form['is_open'])))
        return make_response('Resource updated', 200)
    elif request.method == 'DELETE':
        storage.contract_delete(id)
        return make_response('Resource deleted', 200)
