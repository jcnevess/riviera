# coding: utf-8

from storage import Storage
from flask import Flask, request, jsonify, url_for, make_response
from markupsafe import escape

app = Flask(__name__)
storage = Storage()

@app.route('/guest', methods=['GET', 'POST'])
def guest():
    if request.method == 'GET':
        return jsonify(storage.guest_getall())
    elif request.method == 'POST':
        form = request.form
        storage.guest_add(form['name'], form['social_number'], \
                form['birthdate'], form['address_street'], form['address_number'], \
                form['address_additional_info'], form['address_neighborhood'], \
                form['address_zipcode'], form['address_city'], form['address_state'], \
                form['address_country'], form['credit_card_number'])

        response = make_response('Resource Created', 201)
        response.headers['Location'] = url_for('guest_by_id', id = form['social_number'])
        return response


# using ssn as id for now
@app.route('/guest/<id>', methods=['GET', 'PUT'])
def guest_by_id(id):
    if request.method == 'GET':
        return jsonify(storage.guest_getbyid(id))
    elif request.method == 'PUT':
        form = request.form
        storage.guest_edit(id, form['name'], form['social_number'], form['birthdate'], form['address_street'], \
                form['address_number'], form['address_additional_info'], form['address_neighborhood'], \
                form['address_zipcode'], form['address_city'], form['address_state'], \
                form['address_country'], form['credit_card_number'])
        
        response = make_response('Resource Updated', 200)
        response.headers['Location'] = url_for('guest_by_id', id = form['social_number'])
        return response


@app.route('/service', methods=['GET', 'POST'])
def service():
    if request.method == 'GET':
        return jsonify(storage.service_getall())
    elif request.method == 'POST':
        form = request.form
        service_type = form['service_type']
        id = -1

        if service_type == 'room_rental':
            id = storage.service_add_room(form['rental_type'], form['additional_bed'], form['days'])
        elif service_type == 'car_rental':
            id = storage.service_add_car(form['rental_type'], form['car_plate'], form['full_gas'], \
                    form['car_insurance'], form['days'])
        elif service_type == 'babysitter':
            id = storage.service_add_babysitter(form['normal_hours'], form['extra_hours'])
        elif service_type == 'meal':
            id = storage.service_add_meal(form['value'], form['description'])
        elif service_type == 'extra_service':
            id = storage.service_add_extra(form['value'], form['description'])

        response = make_response('Resource created', 201)
        response.headers['Location'] = url_for('service_by_id', id = id)
        return response


@app.route('/service/<id>', methods=['GET', 'PUT', 'DELETE'])
def service_by_id(id):
    if request.method == 'GET':
        return jsonify(storage.service_getbyid(id))

    elif request.method == 'DELETE':
        storage.service_delete(id)
        return make_response('Resource deleted', 200)
        
    elif request.method == 'PUT':
        form = request.form
        service_type = form['service_type']

        if service_type == 'room_rental':
            id = storage.service_edit_room(id, form['rental_type'], form['additional_bed'], form['days'])
        elif service_type == 'car_rental':
            id = storage.service_edit_car(id, form['rental_type'], form['car_plate'], form['full_gas'], \
                    form['car_insurance'], form['days'])
        elif service_type == 'babysitter':
            id = storage.service_edit_babysitter(id, form['normal_hours'], form['extra_hours'])
        elif service_type == 'meal':
            id = storage.service_edit_meal(id, form['value'], form['description'])
        elif service_type == 'extra_service':
            id = storage.service_edit_extra(id, form['value'], form['description'])

        return make_response('Resource updated', 200)