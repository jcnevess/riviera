# coding: utf-8

from http import HTTPStatus

from flask import Flask, request, jsonify, url_for, make_response
from mysql.connector.errors import DataError

from storage import Storage

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
        try:
            body = request.json
            storage.guest_add(body['name'], body['social_number'], body['birthdate'], body['phone_number'],
                              body['address_street'], body['address_number'], body['address_additional_info'],
                              body['address_neighborhood'], body['address_zipcode'], body['address_city'],
                              body['address_state'], body['address_country'])

            response = make_response('Resource Created', HTTPStatus.OK)
            response.headers['Location'] = url_for('guest_by_id', guest_id=body['social_number'])
            return response
        except KeyError as err:
            return make_response('Required attribute {} not found on request body.'.format(err.args[0]),
                                 HTTPStatus.BAD_REQUEST)
        except DataError as err:
            return make_response(' '.join(err.__dict__.get('msg').split(' ')[:4]),
                                 HTTPStatus.BAD_REQUEST)


@app.route('/guests/<int:guest_id>', methods=[GET, PUT])
def guest_by_id(guest_id):
    if request.method == GET:
        gst = storage.guest_get_byid(guest_id)
        try:
            return jsonify(gst.to_json())
        except AttributeError:
            if gst is None:
                return make_response(HTTPStatus.NOT_FOUND.phrase, HTTPStatus.NOT_FOUND)

    elif request.method == PUT:
        try:
            body = request.json
            success = storage.guest_edit(guest_id, body['name'], body['social_number'], body['birthdate'],
                                         body['phone_number'],
                                         body['address_street'], body['address_number'],
                                         body['address_additional_info'],
                                         body['address_neighborhood'], body['address_zipcode'], body['address_city'],
                                         body['address_state'], body['address_country'])

            return make_response('Resource Updated', HTTPStatus.OK) if success \
                else make_response(HTTPStatus.NOT_FOUND.phrase, HTTPStatus.NOT_FOUND)

        except KeyError as err:
            return make_response('Required attribute {} not found on request body.'.format(err.args[0]),
                                 HTTPStatus.BAD_REQUEST)
        except DataError as err:
            return make_response(' '.join(err.__dict__.get('msg').split(' ')[:4]),
                                 HTTPStatus.BAD_REQUEST)


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
        try:
            body = request.json
            id = storage.contract_add(body['guest_id'], body['card_number'], body['checkin_date'],
                                      body['days_contracted'], body['billing_strategy_id'])
            response = make_response('Resource created', HTTPStatus.CREATED)
            response.headers['Location'] = url_for('contract_by_id', contract_id=id)
            return response
        except KeyError as err:
            return make_response('Required attribute {} not found on request body.'.format(err.args[0]),
                                 HTTPStatus.BAD_REQUEST)

        except DataError as err:
            return make_response(' '.join(err.__dict__.get('msg').split(' ')[:4]),
                                 HTTPStatus.BAD_REQUEST)


@app.route('/contracts/<int:contract_id>', methods=[GET, PUT, DELETE])
def contract_by_id(contract_id):
    if request.method == GET:
        try:
            contr = storage.contract_get_byid(contract_id)
            return jsonify(contr.to_json())
        except AttributeError:
            return make_response(HTTPStatus.NOT_FOUND.phrase, HTTPStatus.NOT_FOUND)

    elif request.method == PUT:
        try:
            body = request.json
            success = storage.contract_edit(contract_id, body['guest_id'], body['card_number'], body['checkin_date'],
                                            body['days_contracted'], body['is_open'])

            return make_response('Resource updated', HTTPStatus.OK) if success \
                else make_response(HTTPStatus.NOT_FOUND.phrase, HTTPStatus.NOT_FOUND)

        except KeyError as err:
            return make_response('Required attribute {} not found on request body.'.format(err.args[0]),
                                 HTTPStatus.BAD_REQUEST)

        except DataError as err:
            return make_response(' '.join(err.__dict__.get('msg').split(' ')[:4]),
                                 HTTPStatus.BAD_REQUEST)

    elif request.method == DELETE:
        success = storage.contract_delete(contract_id)
        return make_response('Resource deleted', HTTPStatus.OK) if success \
            else make_response(HTTPStatus.NOT_FOUND.phrase, HTTPStatus.NOT_FOUND)


@app.route('/contracts/<int:contract_id>/services', methods=[GET, POST])
def service(contract_id):
    if request.method == GET:
        services = storage.service_get_all(contract_id)
        return jsonify(list(map(lambda s: s.to_json(), services))) if len(services) > 0 \
            else make_response(HTTPStatus.NOT_FOUND.phrase, HTTPStatus.NOT_FOUND)

    elif request.method == POST:
        try:
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

        except KeyError as err:
            return make_response('Required attribute {} not found on request body.'.format(err.args[0]),
                                 HTTPStatus.BAD_REQUEST)

        except DataError as err:
            return make_response(' '.join(err.__dict__.get('msg').split(' ')[:4]),
                                 HTTPStatus.BAD_REQUEST)


@app.route('/contracts/<int:contract_id>/services/<int:service_id>', methods=[GET, PUT, DELETE])
def service_by_id(contract_id, service_id):
    if request.method == GET:
        try:
            serv = storage.service_get_byid(contract_id, service_id)
            return jsonify(serv.to_json())
        except AttributeError:
            return make_response(HTTPStatus.NOT_FOUND.phrase, HTTPStatus.NOT_FOUND)

    elif request.method == DELETE:
        success = storage.service_delete(service_id)
        return make_response('Resource deleted', HTTPStatus.OK) if success \
            else make_response(HTTPStatus.NOT_FOUND.phrase, HTTPStatus.NOT_FOUND)

    elif request.method == PUT:
        body = request.json
        service_type = body['service_type']
        success = False

        try:
            if service_type == 'room_rental':
                success = storage.service_edit_room(service_id, body['rental_type'],
                                                    body['additional_bed'], body['days'])

            elif service_type == 'car_rental':
                success = storage.service_edit_car(service_id, body['rental_type'], body['car_plate'],
                                                   body['full_gas'], body['car_insurance'], body['days'])

            elif service_type == 'babysitter':
                success = storage.service_edit_babysitter(service_id, body['normal_hours'], body['extra_hours'])

            elif service_type == 'meal':
                success = storage.service_edit_meal(service_id, body['unit_price'], body['description'])

            elif service_type == 'penalty_fee':
                success = storage.service_edit_penalty_fee(service_id, body['unit_price'],
                                                           body['description'], body['penalties'])

            elif service_type == 'extra_service':
                success = storage.service_edit_extra(service_id, body['unit_price'], body['description'])

            return make_response('Resource updated', HTTPStatus.OK) if success \
                else make_response(HTTPStatus.NOT_FOUND.phrase, HTTPStatus.NOT_FOUND)

        except KeyError as err:
            return make_response('Required attribute {} not found on request body.'.format(err.args[0]),
                                 HTTPStatus.BAD_REQUEST)

        except DataError as err:
            return make_response(' '.join(err.__dict__.get('msg').split(' ')[:4]),
                                 HTTPStatus.BAD_REQUEST)


@app.route('/contracts/<int:contract_id>/review', methods=[GET, POST, PUT, DELETE])
def review(contract_id):
    body = request.json
    rev = None

    if request.method == GET:
        try:
            rev = storage.review_get(contract_id)
            return rev.to_json() if rev else {}
        except AttributeError:
            if rev is None:
                return make_response(HTTPStatus.NOT_FOUND.phrase, HTTPStatus.NOT_FOUND)

    elif request.method == POST:
        try:
            id = storage.review_add(contract_id, body['rating'], body['comment'])

            response = make_response('Resource created', HTTPStatus.CREATED)
            response.headers['Location'] = url_for('review', contract_id=contract_id)
            return response if id != -1 else make_response(HTTPStatus.NOT_FOUND.phrase, HTTPStatus.NOT_FOUND)

        except KeyError as err:
            return make_response('Required attribute {} not found on request body.'.format(err.args[0]),
                                 HTTPStatus.BAD_REQUEST)

        except DataError as err:
            return make_response(' '.join(err.__dict__.get('msg').split(' ')[:4]),
                                 HTTPStatus.BAD_REQUEST)

    elif request.method == PUT:
        try:
            success = storage.review_edit(contract_id, body['rating'], body['comment'])
            return make_response('Resource updated', HTTPStatus.OK) if success \
                else make_response(HTTPStatus.NOT_FOUND.phrase, HTTPStatus.NOT_FOUND)
        except AttributeError:
            return make_response(HTTPStatus.NOT_FOUND.phrase, HTTPStatus.NOT_FOUND)

    elif request.method == DELETE:
        try:
            success = storage.review_delete(contract_id)
            return make_response('Resource deleted', HTTPStatus.OK) if success \
                else make_response(HTTPStatus.NOT_FOUND.phrase, HTTPStatus.NOT_FOUND)
        except AttributeError:
            return make_response(HTTPStatus.NOT_FOUND.phrase, HTTPStatus.NOT_FOUND)


@app.route('/rooms', methods=[GET, PUT])
def room():
    body = request.json

    if request.method == GET:
        return jsonify(storage.room_get_all())

    elif request.method == PUT:
        try:
            action = request.args.get('action')

            if action == 'book':
                success = storage.room_book(body['rental_type'])
                return make_response('Resource updated', HTTPStatus.OK) if success \
                    else make_response(HTTPStatus.NOT_FOUND.phrase, HTTPStatus.NOT_FOUND)

            elif action == 'unbook':
                success = storage.room_unbook(body['rental_type'])
                return make_response('Resource updated', HTTPStatus.OK) if success \
                    else make_response(HTTPStatus.NOT_FOUND.phrase, HTTPStatus.NOT_FOUND)

            else:
                return make_response('Unknown action: {}'.format(action), HTTPStatus.BAD_REQUEST)

        except KeyError as err:
            return make_response('Required attribute {} not found on request body.'.format(err.args[0]),
                                 HTTPStatus.BAD_REQUEST)

        except DataError as err:
            return make_response(' '.join(err.__dict__.get('msg').split(' ')[:4]),
                                 HTTPStatus.BAD_REQUEST)
