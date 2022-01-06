# coding: utf-8

from storage import Storage
from flask import Flask, request, jsonify, url_for, make_response
from distutils.util import strtobool

app = Flask(__name__)
storage = Storage()


@app.route('/guests', methods=['GET', 'POST'])
def guest():
    if request.method == 'GET':
        return jsonify(list(map(lambda i: i.to_json(), storage.guest_getall())))
    elif request.method == 'POST':
        form = request.form
        storage.guest_add(form['name'], form['social_number'], form['birthdate'], form['address_street'], form['address_number'],
                          form['address_additional_info'], form['address_neighborhood'], form['address_zipcode'],
                          form['address_city'], form['address_state'], form['address_country'])

        response = make_response('Resource Created', 201)
        response.headers['Location'] = url_for('guest_by_id', guest_id=form['social_number'])
        return response


# using ssn as id for now
@app.route('/guests/<guest_id>', methods=['GET', 'PUT'])
def guest_by_id(guest_id):
    if request.method == 'GET':
        return jsonify(storage.guest_getbyid(guest_id).to_json())
    elif request.method == 'PUT':
        form = request.form
        storage.guest_edit(guest_id, form['name'], form['social_number'], form['birthdate'], form['address_street'],
                           form['address_number'], form['address_additional_info'], form['address_neighborhood'],
                           form['address_zipcode'], form['address_city'], form['address_state'], form['address_country'])

        response = make_response('Resource Updated', 200)
        response.headers['Location'] = url_for('guest_by_id', guest_id=form['social_number'])
        return response


@app.route('/contracts', methods=['GET', 'POST'])
def contract():
    if request.method == 'GET':
        return jsonify(list(map(lambda c: c.to_json(), storage.contract_getall())))
    elif request.method == 'POST':
        form = request.form
        id = storage.contract_add(form['guest_id'], form['card_number'], form['checkin_date'],
                                  int(form['days_contracted']), form['billing_strategy'])
        response = make_response('Resource created', 201)
        response.headers['Location'] = url_for('contract_by_id', contract_id=id)
        return response


@app.route('/contracts/<contract_id>', methods=['GET', 'PUT', 'DELETE'])
def contract_by_id(contract_id):
    if request.method == 'GET':
        return jsonify(storage.contract_getbyid(contract_id).to_json())
    elif request.method == 'PUT':
        form = request.form
        storage.contract_edit(contract_id, form['guest_id'], form['card_number'], form['checkin_date'],
                              int(form['days_contracted']), bool(strtobool(form['is_open'])))
        return make_response('Resource updated', 200)
    elif request.method == 'DELETE':
        storage.contract_delete(contract_id)
        return make_response('Resource deleted', 200)


@app.route('/contracts/<contract_id>/services', methods=['GET', 'POST'])
def service(contract_id):
    if request.method == 'GET':
        return jsonify(list(map(lambda s: s.to_json(), storage.service_getall(contract_id))))
    elif request.method == 'POST':
        form = request.form
        service_type = form['service_type']
        id = -1

        if service_type == 'room_rental':
            id = storage.service_add_room(contract_id, form['rental_type'], bool(strtobool(form['additional_bed'])), int(form['days']))
        elif service_type == 'car_rental':
            id = storage.service_add_car(contract_id, form['rental_type'], form['car_plate'], bool(strtobool(form['full_gas'])),
                                         bool(strtobool(form['car_insurance'])), int(form['days']))
        elif service_type == 'babysitter':
            id = storage.service_add_babysitter(contract_id, int(form['normal_hours']), int(form['extra_hours']))
        elif service_type == 'meal':
            id = storage.service_add_meal(contract_id, float(form['value']), form['description'])
        elif service_type == 'extra_service':
            id = storage.service_add_extra(contract_id, float(form['value']), form['description'])

        response = make_response('Resource created', 201)
        response.headers['Location'] = url_for('service_by_id', contract_id=contract_id, service_id=id)
        return response


@app.route('/contracts/<contract_id>/services/<service_id>', methods=['GET', 'PUT', 'DELETE'])
def service_by_id(contract_id, service_id):
    if request.method == 'GET':
        return jsonify(storage.service_getbyid(contract_id, service_id).to_json())

    elif request.method == 'DELETE':
        storage.service_delete(contract_id, service_id)
        return make_response('Resource deleted', 200)

    elif request.method == 'PUT':
        form = request.form
        service_type = form['service_type']

        if service_type == 'room_rental':
            storage.service_edit_room(contract_id, service_id, form['rental_type'], bool(strtobool(form['additional_bed'])), int(form['days']))
        elif service_type == 'car_rental':
            storage.service_edit_car(contract_id, service_id, form['rental_type'], form['car_plate'], bool(strtobool(form['full_gas'])),
                                     bool(strtobool(form['car_insurance'])), int(form['days']))
        elif service_type == 'babysitter':
            storage.service_edit_babysitter(contract_id, service_id, int(form['normal_hours']), int(form['extra_hours']))
        elif service_type == 'meal':
            storage.service_edit_meal(contract_id, service_id, float(form['value']), form['description'])
        elif service_type == 'extra_service':
            storage.service_edit_extra(contract_id, service_id, float(form['value']), form['description'])

        return make_response('Resource updated', 200)
