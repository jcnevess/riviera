# coding: utf-8
import uuid
import configparser
import mysql.connector as database

from models import *

db_config = configparser.ConfigParser()
db_config.read(r'database.cfg')

config = dict(db_config.items('riviera'))
config['port'] = int(config['port'])

# TODO: When to close connection?
connection = database.connect(**config)


class Storage:

    ''' Helper methods '''

    def __get_product(self, name: str):
        cursor = connection.cursor(buffered=True, dictionary=True)
        product = None

        query = 'select * from product where name = %s'
        params = tuple([name])

        cursor.execute(query, params)

        for entry in cursor:
            product = Product(entry['id'], entry['name'], float(entry['price']), entry['quantity'])

        connection.commit()
        cursor.close()

        return product

    def __get_product_id(self, id: int):
        cursor = connection.cursor(buffered=True, dictionary=True)
        product = None

        query = 'select * from product where id = %s'
        params = tuple([id])

        cursor.execute(query, params)

        for entry in cursor:
            product = Product(entry['id'], entry['name'], float(entry['price']), entry['quantity'])

        connection.commit()
        cursor.close()

        return product

    @staticmethod  # FIXME This won't be needed if we pass strategy_id as param to contract creation
    def __get_billing_strategy(billing_strategy: str):
        if billing_strategy == 'holiday_season':
            return HolidaySeasonStrategy()
        elif billing_strategy == 'june_season':
            return JuneSeasonStrategy()
        elif billing_strategy == 'june_high_season':
            return JuneHighSeasonStrategy()
        elif billing_strategy == 'low_season':
            return LowSeasonStrategy()
        else:
            return BillingStrategy()

    ''' Guest methods. Using SSN as id for now. '''

    def guest_getall(self):
        cursor = connection.cursor(buffered=True, dictionary=True)
        data = []

        query = 'select * from guest'
        cursor.execute(query)

        if cursor.rowcount > 0:
            for entry in cursor:
                address = Address(entry['id'], entry['address_street'], entry['address_street_number'],
                                  entry['address_additional_info'], entry['address_neighborhood'],
                                  entry['address_zipcode'],
                                  entry['address_city'], entry['address_state'], entry['address_country'])
                guest = Guest(entry['id'], entry['name'], entry['social_number'],
                              entry['birth_date'], entry['phone_number'], address)
                data.append(guest)

        cursor.close()
        return data

    # TODO: This is almost the same as get_all, only the query is different. Refactor.
    def guest_getbyid(self, guest_id: int):
        cursor = connection.cursor(buffered=True, dictionary=True)
        guest = None

        query = 'select * from guest where id = %s'
        params = tuple([guest_id])
        cursor.execute(query, params)

        if cursor.rowcount > 0:
            for entry in cursor:
                address = Address(entry['id'], entry['address_street'], entry['address_street_number'],
                                  entry['address_additional_info'], entry['address_neighborhood'],
                                  entry['address_zipcode'],
                                  entry['address_city'], entry['address_state'], entry['address_country'])
                guest = Guest(entry['id'], entry['name'], entry['social_number'],
                              entry['birth_date'], entry['phone_number'], address)

        cursor.close()
        return guest

    def guest_add(self, name: str, social_number: str, birthdate: str, phone_number: str,
                  address_street: str, address_number: str, address_additional_info: str,
                  address_neighborhood: str, address_zipcode: str, address_city: str,
                  address_state: str, address_country: str):

        cursor = connection.cursor()

        query = ('insert into guest '
                 '(name, social_number, birth_date, phone_number, address_street, '
                 'address_street_number, address_additional_info, address_neighborhood, address_zipcode, address_city, '
                 'address_state, address_country) '
                 'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')

        params = (name, social_number, birthdate, phone_number, address_street,
                  address_number, address_additional_info, address_neighborhood, address_zipcode, address_city,
                  address_state, address_country)

        cursor.execute(query, params)
        connection.commit()
        cursor.close()

    def guest_edit(self, id: int, name: str, social_number: str, birthdate: str, phone_number: str,
                   address_street: str, address_number: str, address_additional_info: str,
                   address_neighborhood: str, address_zipcode: str, address_city: str,
                   address_state: str, address_country: str):

        cursor = connection.cursor()

        query = ('update guest '
                 'set name = %s, '
                 'social_number = %s, '
                 'birth_date = %s, '
                 'phone_number = %s, '
                 'address_street = %s, '
                 'address_street_number = %s, '
                 'address_additional_info = %s, '
                 'address_neighborhood = %s, '
                 'address_zipcode = %s, '
                 'address_city = %s, '
                 'address_state = %s, '
                 'address_country = %s '
                 'where id = %s')

        params = (name, social_number, birthdate, phone_number, address_street,
                  address_number, address_additional_info, address_neighborhood, address_zipcode, address_city,
                  address_state, address_country, id)

        cursor.execute(query, params)
        connection.commit()
        cursor.close()

    ''' Contract methods '''

    def contract_getall(self):
        cursor = connection.cursor(buffered=True, dictionary=True)
        contracts = []

        query = ('select c.*, '
                 'cbs.name as strategy_name, cbs.multiplier as strategy_multiplier, '
                 'g.name as g_name, '
                 'g.social_number as g_social_number, '
                 'g.birth_date as g_birth_date, '
                 'g.phone_number as g_phone_number, '
                 'g.address_street as g_address_street, '
                 'g.address_street_number as g_address_street_number, '
                 'g.address_additional_info as g_address_additional_info, '
                 'g.address_neighborhood as g_address_neighborhood, '
                 'g.address_zipcode as g_address_zipcode, '
                 'g.address_city as g_address_city, '
                 'g.address_state as g_address_state, '
                 'g.address_country as g_address_country '
                 'from contract c join contract_billing_strategy cbs on c.billing_strategy_id = cbs.id '
                 'join guest g on c.guest_id = g.id')

        cursor.execute(query)

        for entry in cursor:
            address = Address(entry['guest_id'], entry['g_address_street'], entry['g_address_street_number'],
                              entry['g_address_additional_info'], entry['g_address_neighborhood'], entry['g_address_zipcode'],
                              entry['g_address_city'], entry['g_address_state'], entry['g_address_country'])
            guest = Guest(entry['guest_id'], entry['g_name'], entry['g_social_number'], entry['g_birth_date'],
                          entry['g_phone_number'], address)
            billing_strategy = self.__get_billing_strategy(entry['strategy_name'])  # TODO Could be better
            contract = Contract(entry['id'], guest, entry['credit_card_number'], entry['checkin_time'],
                                entry['contracted_days'], services=[], billing_strategy=billing_strategy, is_open=bool(entry['is_open']), review=None)  # FIXME Retrieve services and reviews
            contracts.append(contract)

        connection.commit()
        cursor.close()

        return contracts

    def contract_getbyid(self, contract_id: int):
        cursor = connection.cursor(buffered=True, dictionary=True)
        contract = None

        query = ('select c.*, '
                 'cbs.name as strategy_name, cbs.multiplier as strategy_multiplier, '
                 'g.name as g_name, '
                 'g.social_number as g_social_number, '
                 'g.birth_date as g_birth_date, '
                 'g.phone_number as g_phone_number, '
                 'g.address_street as g_address_street, '
                 'g.address_street_number as g_address_street_number, '
                 'g.address_additional_info as g_address_additional_info, '
                 'g.address_neighborhood as g_address_neighborhood, '
                 'g.address_zipcode as g_address_zipcode, '
                 'g.address_city as g_address_city, '
                 'g.address_state as g_address_state, '
                 'g.address_country as g_address_country '
                 'from contract c join contract_billing_strategy cbs on c.billing_strategy_id = cbs.id '
                 'join guest g on c.guest_id = g.id '
                 'where c.id = %s')
        params = tuple([contract_id])

        cursor.execute(query, params)

        for entry in cursor:
            address = Address(entry['guest_id'], entry['g_address_street'], entry['g_address_street_number'],
                              entry['g_address_additional_info'], entry['g_address_neighborhood'], entry['g_address_zipcode'],
                              entry['g_address_city'], entry['g_address_state'], entry['g_address_country'])
            guest = Guest(entry['guest_id'], entry['g_name'], entry['g_social_number'], entry['g_birth_date'],
                          entry['g_phone_number'], address)
            billing_strategy = self.__get_billing_strategy(entry['strategy_name'])  # TODO Could be better
            contract = Contract(entry['id'], guest, entry['credit_card_number'], entry['checkin_time'],
                                entry['contracted_days'], services=[], billing_strategy=billing_strategy, is_open=bool(entry['is_open']), review=None)  # FIXME Retrieve services and reviews

        connection.commit()
        cursor.close()
        return contract

    def contract_add(self, guest_id: int, card_number: str, checkin_time: str, contracted_days: int,
                     billing_strategy_id: int):
        cursor = connection.cursor()

        query = ('insert into contract '
                 '(guest_id, checkin_time, contracted_days, credit_card_number, is_open, '
                 'billing_strategy_id) '
                 'values (%s, %s, %s, %s, %s, %s)')
        params = (guest_id, checkin_time, contracted_days, card_number, True, billing_strategy_id)
        cursor.execute(query, params)

        connection.commit()
        id = cursor.lastrowid

        cursor.close()

        return id

    def contract_edit(self, contract_id: int, guest_id: int, card_number: str, checkin_time: str, contracted_days: int,
                      is_open: bool):
        cursor = connection.cursor()

        query = ('update contract '
                 'set guest_id = %s, '
                 'checkin_time = %s, '
                 'contracted_days = %s, '
                 'credit_card_number = %s, '
                 'is_open = %s '
                 'where id = %s')
        params = (guest_id, checkin_time, contracted_days, card_number, is_open, contract_id)
        cursor.execute(query, params)

        connection.commit()
        cursor.close()

    def contract_delete(self, contract_id: str):
        cursor = connection.cursor()

        query = 'delete from contract where id = %s'
        params = tuple([contract_id])
        cursor.execute(query, params)

        connection.commit()
        cursor.close()

    ''' Service methods '''

    def service_getall(self, contract_id: int):
        cursor = connection.cursor(buffered=True, dictionary=True)
        services = []

        query = ('select *, s.id as service_id, p.id as product_id from service s '
                 'inner join room_rental rr '
                 'inner join product p '
                 'on s.id = rr.service_id '
                 'and rr.product_id = p.id')
        cursor.execute(query)

        for entry in cursor:
            product = Product(entry['product_id'], entry['name'], float(entry['price']), entry['quantity'])
            service = RoomRental(entry['service_id'], product, bool(entry['has_additional_bed']),
                                 entry['contracted_days'])
            services.append(service)

        connection.commit()

        query = ('select *, s.id as service_id, p.id as product_id from service s '
                 'inner join car_rental cr '
                 'inner join product p '
                 'on s.id = cr.service_id '
                 'and cr.product_id = p.id')
        cursor.execute(query)

        for entry in cursor:
            products = [self.__get_product_id(entry['product_id'])]
            if bool(entry['has_full_gas']):
                products.append(self.__get_product('car_full_gas'))
            if bool(entry['has_insurance']):
                products.append(self.__get_product('car_insurance'))
            service = CarRental(entry['service_id'], products, entry['car_plate'], bool(entry['has_full_gas']),
                                bool(entry['has_insurance']), entry['contracted_days'])
            services.append(service)

        connection.commit()

        query = ('select *, s.id as service_id, p.id as product_id from service s '
                 'inner join babysitter b '
                 'inner join product p '
                 'on s.id = b.service_id '
                 'and b.product_id = p.id')
        cursor.execute(query)

        for entry in cursor:
            product = Product(entry['product_id'], entry['name'], float(entry['price']), entry['quantity'])
            service = Babysitter(entry['service_id'], product, entry['normal_hours'], entry['extra_hours'])
            services.append(service)

        connection.commit()

        query = ('select * from service s '
                 'inner join meal m '
                 'on s.id = m.service_id')
        cursor.execute(query)

        for entry in cursor:
            service = Meal(entry['service_id'], float(entry['unit_price']), entry['description'])
            services.append(service)

        connection.commit()

        query = ('select * from service s '
                 'inner join penalty_fee p '
                 'on s.id = p.service_id')
        cursor.execute(query)

        for entry in cursor:
            service = PenaltyFee(entry['service_id'], float(entry['unit_price']), entry['description'],
                                 entry['penalties'])
            services.append(service)

        connection.commit()

        query = ('select * from service s '
                 'inner join extra_service e '
                 'on s.id = e.service_id')
        cursor.execute(query)

        for entry in cursor:
            service = ExtraService(entry['service_id'], float(entry['unit_price']), entry['description'])
            services.append(service)

        connection.commit()

        cursor.close()
        return services

    def service_getbyid(self, service_id: int):
        cursor = connection.cursor(buffered=True, dictionary=True)
        service_type = ''
        service = None

        query = 'select * from service where id = %s'
        params = tuple([service_id])
        cursor.execute(query, params)
        for entry in cursor:
            service_type = entry['service_type']
        connection.commit()

        if service_type == 'room_rental':
            query = ('select *, s.id as service_id, p.id as product_id from service s '
                     'inner join room_rental rr '
                     'inner join product p '
                     'on s.id = rr.service_id '
                     'and rr.product_id = p.id '
                     'where s.id = %s')
            params = tuple([service_id])
            cursor.execute(query, params)

            for entry in cursor:
                product = Product(entry['product_id'], entry['name'], float(entry['price']), entry['quantity'])
                service = RoomRental(entry['service_id'], product, bool(entry['has_additional_bed']), entry['contracted_days'])
            connection.commit()

        elif service_type == 'car_rental':
            query = ('select *, s.id as service_id, p.id as product_id from service s '
                     'inner join car_rental cr '
                     'inner join product p '
                     'on s.id = cr.service_id '
                     'and cr.product_id = p.id '
                     'where s.id = %s')
            params = tuple([service_id])
            cursor.execute(query, params)

            for entry in cursor:
                products = [self.__get_product_id(entry['product_id'])]
                if bool(entry['has_full_gas']):
                    products.append(self.__get_product('car_full_gas'))
                if bool(entry['has_insurance']):
                    products.append(self.__get_product('car_insurance'))
                service = CarRental(entry['service_id'], products, entry['car_plate'], bool(entry['has_full_gas']),
                                    bool(entry['has_insurance']), entry['contracted_days'])
            connection.commit()

        elif service_type == 'babysitter':
            query = ('select *, s.id as service_id, p.id as product_id from service s '
                     'inner join babysitter b '
                     'inner join product p '
                     'on s.id = b.service_id '
                     'and b.product_id = p.id '
                     'where s.id = %s')
            params = tuple([service_id])
            cursor.execute(query, params)

            for entry in cursor:
                product = Product(entry['product_id'], entry['name'], float(entry['price']), entry['quantity'])
                service = Babysitter(entry['service_id'], product, entry['normal_hours'], entry['extra_hours'])
            connection.commit()

        elif service_type == 'meal':
            query = ('select * from service s '
                     'inner join meal m '
                     'on s.id = m.service_id '
                     'where s.id = %s')
            params = tuple([service_id])
            cursor.execute(query, params)

            for entry in cursor:
                service = Meal(entry['service_id'], float(entry['unit_price']), entry['description'])
            connection.commit()

        elif service_type == 'penalty_fee':
            query = ('select * from service s '
                     'inner join penalty_fee p '
                     'on s.id = p.service_id '
                     'where s.id = %s')
            params = tuple([service_id])
            cursor.execute(query, params)

            for entry in cursor:
                service = PenaltyFee(entry['service_id'], float(entry['unit_price']), entry['description'], entry['penalties'])
            connection.commit()

        elif service_type == 'extra_service':
            query = ('select * from service s '
                     'inner join extra_service e '
                     'on s.id = e.service_id '
                     'where s.id = %s')
            params = tuple([service_id])
            cursor.execute(query, params)

            for entry in cursor:
                service = ExtraService(entry['service_id'], float(entry['unit_price']), entry['description'])
            connection.commit()

        cursor.close()
        return service

    def service_add_room(self, contract_id: str, rental_type: str, additional_bed: bool, days: int):
        cursor = connection.cursor()

        query = ('insert into service '
                 '(contract_id, service_type) values '
                 '(%s, %s)')
        params = (contract_id, 'room_rental')
        cursor.execute(query, params)
        connection.commit()

        service_id = cursor.lastrowid

        product_id = self.__get_product(rental_type).id

        query = ('insert into room_rental '
                 '(service_id, product_id, contracted_days, has_additional_bed) values '
                 '(%s, %s, %s, %s)')
        params = (service_id, product_id, days, additional_bed)
        cursor.execute(query, params)

        connection.commit()
        cursor.close()

        return service_id

    def service_add_car(self, contract_id: int, rental_type: str, car_plate: str, full_gas: bool, car_insurance: bool,
                        days: int):
        cursor = connection.cursor()

        query = ('insert into service '
                 '(contract_id, service_type) values '
                 '(%s, %s)')
        params = (contract_id, 'car_rental')
        cursor.execute(query, params)
        connection.commit()

        service_id = cursor.lastrowid

        product_id = self.__get_product(rental_type).id

        query = ('insert into car_rental '
                 '(service_id, product_id, contracted_days, car_plate, has_full_gas, has_insurance) values '
                 '(%s, %s, %s, %s, %s, %s)')
        params = (service_id, product_id, days, car_plate, full_gas, car_insurance)
        cursor.execute(query, params)

        connection.commit()
        cursor.close()

        return service_id

    def service_add_babysitter(self, contract_id: int, normal_hours: int, extra_hours: int):
        cursor = connection.cursor()

        query = ('insert into service '
                 '(contract_id, service_type) values '
                 '(%s, %s)')
        params = (contract_id, 'babysitter')
        cursor.execute(query, params)
        connection.commit()

        service_id = cursor.lastrowid

        product_id = self.__get_product('babysitter').id

        query = ('insert into babysitter '
                 '(service_id, product_id, normal_hours, extra_hours) values '
                 '(%s, %s, %s, %s)')
        params = (service_id, product_id, normal_hours, extra_hours)
        cursor.execute(query, params)

        connection.commit()
        cursor.close()

        return service_id

    def service_add_meal(self, contract_id: int, unit_price: float, description: str):
        cursor = connection.cursor()

        query = ('insert into service '
                 '(contract_id, service_type) values '
                 '(%s, %s)')
        params = (contract_id, 'meal')
        cursor.execute(query, params)
        connection.commit()

        service_id = cursor.lastrowid

        query = ('insert into meal '
                 '(service_id, unit_price, description) values '
                 '(%s, %s, %s)')
        params = (service_id, unit_price, description)
        cursor.execute(query, params)

        connection.commit()
        cursor.close()

        return service_id

    def service_add_penalty_fee(self, contract_id: int, unit_price: float, description: str, penalties: int):
        cursor = connection.cursor()

        query = ('insert into service '
                 '(contract_id, service_type) values '
                 '(%s, %s)')
        params = (contract_id, 'penalty_fee')
        cursor.execute(query, params)
        connection.commit()

        service_id = cursor.lastrowid

        query = ('insert into penalty_fee '
                 '(service_id, unit_price, description, penalties) values '
                 '(%s, %s, %s, %s)')
        params = (service_id, unit_price, description, penalties)
        cursor.execute(query, params)

        connection.commit()
        cursor.close()

        return service_id

    def service_add_extra(self, contract_id: int, unit_price: float, description: str):
        cursor = connection.cursor()

        query = ('insert into service '
                 '(contract_id, service_type) values '
                 '(%s, %s)')
        params = (contract_id, 'extra_service')
        cursor.execute(query, params)
        connection.commit()

        service_id = cursor.lastrowid

        query = ('insert into extra_service '
                 '(service_id, unit_price, description) values '
                 '(%s, %s, %s)')
        params = (service_id, unit_price, description)
        cursor.execute(query, params)

        connection.commit()
        cursor.close()

        return service_id

    def service_edit_room(self, service_id: int, rental_type: str, additional_bed: bool, days: int):
        cursor = connection.cursor()

        product_id = self.__get_product(rental_type).id

        query = ('update room_rental '
                 'set product_id = %s, '
                 'contracted_days = %s, '
                 'has_additional_bed = %s '
                 'where service_id = %s')
        params = (product_id, days, additional_bed, service_id)
        cursor.execute(query, params)

        connection.commit()
        cursor.close()

        return service_id

    def service_edit_car(self, service_id: int, rental_type: str, car_plate: str, full_gas: bool,
                         car_insurance: bool, days: int):
        cursor = connection.cursor()

        product_id = self.__get_product(rental_type).id

        query = ('update car_rental '
                 'set product_id = %s, '
                 'contracted_days = %s, '
                 'car_plate = %s, '
                 'has_full_gas = %s, '
                 'has_insurance = %s '
                 'where service_id = %s')
        params = (product_id, days, car_plate, full_gas, car_insurance, service_id)
        cursor.execute(query, params)

        connection.commit()
        cursor.close()

        return service_id

    def service_edit_babysitter(self, service_id: int, normal_hours: int, extra_hours: int):
        cursor = connection.cursor()

        product_id = self.__get_product('babysitter').id

        query = ('update babysitter '
                 'set product_id = %s, '
                 'normal_hours = %s, '
                 'extra_hours = %s '
                 'where service_id = %s')
        params = (product_id, normal_hours, extra_hours, service_id)
        cursor.execute(query, params)

        connection.commit()
        cursor.close()

    def service_edit_meal(self, service_id: int, unit_price: float, description: str):
        cursor = connection.cursor()

        query = ('update meal '
                 'set unit_price = %s, '
                 'description = %s '
                 'where service_id = %s')
        params = (unit_price, description, service_id)
        cursor.execute(query, params)

        connection.commit()
        cursor.close()

    def service_edit_penalty_fee(self, service_id: int, unit_price: float, description: str,
                                 penalties: int):
        cursor = connection.cursor()

        query = ('update penalty_fee '
                 'set unit_price = %s, '
                 'description = %s, '
                 'penalties = %s '
                 'where service_id = %s')
        params = (unit_price, description, penalties, service_id)
        cursor.execute(query, params)

        connection.commit()
        cursor.close()

    def service_edit_extra(self, service_id: int, unit_price: float, description: str):
        cursor = connection.cursor()

        query = ('update extra_service '
                 'set unit_price = %s, '
                 'description = %s '
                 'where service_id = %s')
        params = (unit_price, description, service_id)
        cursor.execute(query, params)

        connection.commit()
        cursor.close()

    def service_delete(self, service_id: int):
        cursor = connection.cursor()

        query = ('delete from service '
                 'where id = %s')
        params = tuple([service_id])
        cursor.execute(query, params)

        connection.commit()
        cursor.close()

    ''' Room methods '''

    def room_getall(self):
        return list(filter(lambda prod: prod.name.startswith('room'), self.products))

    def room_book(self, rental_type: str):
        for product in self.products:
            if product.name == rental_type:
                product.quantity -= 1

    def room_unbook(self, rental_type: str):
        for product in self.products:
            if product.name == rental_type:
                product.quantity += 1

    ''' Review methods '''

    def review_get(self, contract_id: str):
        for contract in self.contracts:
            if contract.id == contract_id:
                return contract.review

    def review_add(self, contract_id: str, rating: int, comment: str):
        id = uuid.uuid4().hex
        for contract in self.contracts:
            if contract.id == contract_id:
                contract.review = Review(id, rating, comment)

    def review_edit(self, contract_id: str, rating: int, comment: str):
        for contract in self.contracts:
            if contract.id == contract_id:
                id = contract.review.id
                contract.review = Review(id, rating, comment)

    def review_delete(self, contract_id: str):
        for contract in self.contracts:
            if contract.id == contract_id:
                contract.review = None
