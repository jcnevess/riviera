# coding: utf-8

from storage import Storage
from flask import Flask, request, jsonify, url_for, make_response
from http import HTTPStatus

app = Flask(__name__)
storage = Storage()

GET = 'GET'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'


@app.route('/guests', methods=[GET, POST])
def guest():
    if request.method == GET:
        return jsonify(list(map(lambda i: i.to_json(), storage.guest_get_all())))
    elif request.method == POST:
        body = request.json
        storage.guest_add(body['name'], body['social_number'], body['birthdate'], body['phone_number'],
                          body['address_street'], body['address_number'], body['address_additional_info'],
                          body['address_neighborhood'], body['address_zipcode'], body['address_city'],
                          body['address_state'], body['address_country'])

        response = make_response('Resource Created', HTTPStatus.OK)
        response.headers['Location'] = url_for('guest_by_id', guest_id=body['social_number'])
        return response


@app.route('/guests/<int:guest_id>', methods=[GET, PUT])
def guest_by_id(guest_id):
    if request.method == GET:
        return jsonify(storage.guest_get_byid(guest_id).to_json())
    elif request.method == PUT:
        body = request.json
        storage.guest_edit(guest_id, body['name'], body['social_number'], body['birthdate'], body['phone_number'],
                           body['address_street'], body['address_number'], body['address_additional_info'],
                           body['address_neighborhood'], body['address_zipcode'], body['address_city'],
                           body['address_state'], body['address_country'])

        response = make_response('Resource Updated', HTTPStatus.OK)
        response.headers['Location'] = url_for('guest_by_id', guest_id=body['social_number'])
        return response


@app.route('/contracts', methods=[GET, POST])
def contract():
    if request.method == GET:
        args = request.args
        result = storage.contract_get_all()

        if args.get('month'):
            result = filter(lambda c: c.checkin_time.month == int(args.get('month')), result)

        if args.get('open') == 'true':
            result = filter(lambda c: c.is_open, result)

        return jsonify(list(map(lambda c: c.to_json(), result)))

    elif request.method == POST:
        body = request.json
        id = storage.contract_add(int(body['guest_id']), body['card_number'], body['checkin_date'],
                                  int(body['days_contracted']), body['billing_strategy_id'])
        response = make_response('Resource created', HTTPStatus.CREATED)
        response.headers['Location'] = url_for('contract_by_id', contract_id=id)
        return response


@app.route('/contracts/<int:contract_id>', methods=[GET, PUT, DELETE])
def contract_by_id(contract_id):
    if request.method == GET:
        return jsonify(storage.contract_get_byid(contract_id).to_json())
    elif request.method == PUT:
        body = request.json
        storage.contract_edit(contract_id, body['guest_id'], body['card_number'], body['checkin_date'],
                              body['days_contracted'], body['is_open'])
        return make_response('Resource updated', HTTPStatus.OK)
    elif request.method == DELETE:
        storage.contract_delete(contract_id)
        return make_response('Resource deleted', HTTPStatus.OK)


@app.route('/contracts/<int:contract_id>/services', methods=[GET, POST])
def service(contract_id):
    if request.method == GET:
        return jsonify(list(map(lambda s: s.to_json(), storage.service_get_all(contract_id))))
    elif request.method == POST:
        body = request.json
        service_type = body['service_type']
        id = -1

        if service_type == 'room_rental':
            id = storage.service_add_room(contract_id, body['rental_type'],
                                          body['additional_bed'], body['days'])

        elif service_type == 'car_rental':
            id = storage.service_add_car(contract_id, body['rental_type'], body['car_plate'],
                                         body['full_gas'], body['car_insurance'], body['days'])

        elif service_type == 'babysitter':
            id = storage.service_add_babysitter(contract_id, body['normal_hours'], body['extra_hours'])

        elif service_type == 'meal':
            id = storage.service_add_meal(contract_id, body['unit_price'], body['description'])

        elif service_type == 'penalty_fee':
            id = storage.service_add_penalty_fee(contract_id, body['unit_price'],
                                                 body['description'], body['penalties'])

        elif service_type == 'extra_service':
            id = storage.service_add_extra(contract_id, body['unit_price'], body['description'])

        response = make_response('Resource created', HTTPStatus.CREATED)
        response.headers['Location'] = url_for('service_by_id', contract_id=contract_id, service_id=id)
        return response


@app.route('/contracts/<int:contract_id>/services/<int:service_id>', methods=[GET, PUT, DELETE])
def service_by_id(contract_id, service_id):
    if request.method == GET:
        return jsonify(storage.service_get_byid(service_id).to_json())

    elif request.method == DELETE:
        storage.service_delete(service_id)
        return make_response('Resource deleted', HTTPStatus.OK)

    elif request.method == PUT:
        body = request.json
        service_type = body['service_type']

        if service_type == 'room_rental':
            storage.service_edit_room(service_id, body['rental_type'], body['additional_bed'], body['days'])

        elif service_type == 'car_rental':
            storage.service_edit_car(service_id, body['rental_type'], body['car_plate'],
                                     body['full_gas'], body['car_insurance'], body['days'])

        elif service_type == 'babysitter':
            storage.service_edit_babysitter(service_id, body['normal_hours'], body['extra_hours'])

        elif service_type == 'meal':
            storage.service_edit_meal(service_id, body['unit_price'], body['description'])

        elif service_type == 'penalty_fee':
            storage.service_edit_penalty_fee(service_id, body['unit_price'], body['description'], body['penalties'])

        elif service_type == 'extra_service':
            storage.service_edit_extra(service_id, body['unit_price'], body['description'])

        return make_response('Resource updated', HTTPStatus.OK)


@app.route('/contracts/<int:contract_id>/review', methods=[GET, POST, PUT, DELETE])
def review(contract_id):
    body = request.json

    if request.method == GET:
        rev = storage.review_get(contract_id)
        return rev.to_json() if rev else {}

    elif request.method == POST:
        storage.review_add(contract_id, body['rating'], body['comment'])
        response = make_response('Resource created', HTTPStatus.CREATED)
        response.headers['Location'] = url_for('review', contract_id=contract_id)
        return response

    elif request.method == PUT:
        storage.review_edit(contract_id, body['rating'], body['comment'])
        return make_response('Resource updated', HTTPStatus.OK)

    elif request.method == DELETE:
        storage.review_delete(contract_id)
        return make_response('Resource deleted', HTTPStatus.OK)


@app.route('/rooms', methods=[GET, PUT])
def room():
    body = request.json

    if request.method == GET:
        return jsonify(storage.room_get_all())

    elif request.method == PUT:
        action = request.args.get('action')
        if action == 'book':
            storage.room_book(body['rental_type'])
        elif action == 'unbook':
            storage.room_unbook(body['rental_type'])

    return make_response('Resource updated', HTTPStatus.OK)
