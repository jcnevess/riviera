# coding: utf-8
import sys
import uuid
import configparser
import mysql.connector as database

from models import *
from typing import List
from datetime import datetime

db_config = configparser.ConfigParser()
db_config.read(r'database.cfg')

config = dict(db_config.items('riviera'))
config['port'] = int(config['port'])

# TODO: When to close connection?
connection = database.connect(**config)


class Storage:
    guests: List[Guest] = []
    services: List[Service] = []
    contracts: List[Contract] = []
    products: List[Product] = [
        Product(1, 'room_presidential', 1200, 5),
        Product(2, 'room_luxury_simple', 520, 5),
        Product(3, 'room_luxury_double', 570, 15),
        Product(4, 'room_luxury_triple', 620, 20),
        Product(5, 'room_executive_simple', 360, 5),
        Product(6, 'room_executive_double', 385, 15),
        Product(7, 'room_executive_triple', 440, 20),
        Product(8, 'car_luxury', 100, -1),
        Product(9, 'car_executive', 60, -1),
        Product(10, 'car_full_gas', 150, -1),
        Product(11, 'car_insurance', 100, -1),
        Product(12, 'babysitter', 25, -1)
    ]

    ''' Helper methods '''

    def __get_product(self, rental_type: str):
        return list(filter(lambda prod: prod.name == rental_type, self.products))[0]

    @staticmethod
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
        return self.contracts

    def contract_getbyid(self, contract_id: str):
        return list(filter(lambda contract: contract.id == contract_id, self.contracts))[0]

    def contract_add(self, guest_id: str, card_number: str, checkin_time: str, contracted_days: int,
                     billing_strategy: str):
        id = uuid.uuid4().hex
        guest = self.guest_getbyid(guest_id)
        checkin_tm = datetime.fromisoformat(checkin_time)
        bill_strategy = self.__get_billing_strategy(billing_strategy)
        self.contracts.append(
            Contract(id, guest, card_number, checkin_tm, contracted_days, billing_strategy=bill_strategy))
        return id

    def contract_edit(self, contract_id: str, guest_id: str, card_number: str, checkin_time: str, contracted_days: int,
                      is_open: bool):
        guest = self.guest_getbyid(guest_id)
        checkin_tm = datetime.fromisoformat(checkin_time)

        for (index, contract) in enumerate(self.contracts):
            if contract.id == contract_id:
                self.contracts[index] = Contract(contract_id, guest, card_number, checkin_tm, contracted_days,
                                                 contract.services, is_open=is_open)

    def contract_delete(self, contract_id: str):
        self.contracts = list(filter(lambda contract: contract.id != contract_id, self.contracts))

    ''' Service methods '''

    def service_getall(self, contract_id: str):
        return [service for contract in self.contracts if contract.id == contract_id for service in contract.services]

    def service_getbyid(self, contract_id: str, service_id: str):
        return [service for contract in self.contracts if contract.id == contract_id for service in contract.services if
                service.id == service_id][0]

    def service_add_room(self, contract_id: str, rental_type: str, additional_bed: bool, days: int):
        id = uuid.uuid4().hex
        room_rental_type = self.__get_product(rental_type)
        for contract in self.contracts:
            if contract.id == contract_id:
                contract.services.append(RoomRental(id, room_rental_type, additional_bed, days))
        return id

    def service_add_car(self, contract_id: str, rental_type: str, car_plate: str, full_gas: bool, car_insurance: bool,
                        days: int):
        id = uuid.uuid4().hex

        products = [self.__get_product(rental_type)]
        if full_gas:
            products.append(self.__get_product('car_full_gas'))

        if car_insurance:
            products.append(self.__get_product('car_insurance'))

        for contract in self.contracts:
            if contract.id == contract_id:
                contract.services.append(CarRental(id, products, car_plate, full_gas, car_insurance, days))
        return id

    def service_add_babysitter(self, contract_id: str, normal_hours: int, extra_hours: int):
        id = uuid.uuid4().hex
        product = list(filter(lambda prod: prod.name == 'babysitter', self.products))[0]
        for contract in self.contracts:
            if contract.id == contract_id:
                contract.services.append(Babysitter(id, product, normal_hours, extra_hours))
        return id

    def service_add_meal(self, contract_id: str, unit_price: float, description: str):
        id = uuid.uuid4().hex
        for contract in self.contracts:
            if contract.id == contract_id:
                contract.services.append(Meal(id, unit_price, description))
        return id

    def service_add_penalty_fee(self, contract_id: str, unit_price: float, description: str, penalties: int):
        id = uuid.uuid4().hex
        for contract in self.contracts:
            if contract.id == contract_id:
                contract.services.append(PenaltyFee(id, unit_price, description, penalties))
        return id

    def service_add_extra(self, contract_id: str, unit_price: float, description: str):
        id = uuid.uuid4().hex
        for contract in self.contracts:
            if contract.id == contract_id:
                contract.services.append(ExtraService(id, unit_price, description))
        return id

    def service_edit_room(self, contract_id: str, service_id: str, rental_type: str, additional_bed: bool, days: int):
        room_rental_type = self.__get_product(rental_type)
        for contract in self.contracts:
            if contract.id == contract_id:
                for (index, service) in enumerate(contract.services):
                    if service.id == service_id:
                        contract.services[index] = RoomRental(service_id, room_rental_type, additional_bed, days)

    def service_edit_car(self, contract_id: str, service_id: str, rental_type: str, car_plate: str, full_gas: bool,
                         car_insurance: bool,
                         days: int):
        for contract in self.contracts:
            if contract.id == contract_id:
                for (index, service) in enumerate(contract.services):
                    if service.id == service_id:
                        products = [self.__get_product(rental_type)]
                        if full_gas:
                            products.append(self.__get_product('car_full_gas'))

                        if car_insurance:
                            products.append(self.__get_product('car_insurance'))
                        contract.services[index] = CarRental(service_id, products, car_plate, full_gas, car_insurance,
                                                             days)

    def service_edit_babysitter(self, contract_id: str, service_id: str, normal_hours: int, extra_hours: int):
        product = list(filter(lambda prod: prod.name == 'babysitter', self.products))[0]
        for contract in self.contracts:
            if contract.id == contract_id:
                for (index, service) in enumerate(contract.services):
                    if service.id == service_id:
                        contract.services[index] = Babysitter(service_id, product, normal_hours, extra_hours)

    def service_edit_meal(self, contract_id: str, service_id: str, unit_price: float, description: str):
        for contract in self.contracts:
            if contract.id == contract_id:
                for (index, service) in enumerate(contract.services):
                    if service.id == service_id:
                        contract.services[index] = Meal(service_id, unit_price, description)

    def service_edit_penalty_fee(self, contract_id: str, service_id: str, unit_price: float, description: str,
                                 penalties: int):
        for contract in self.contracts:
            if contract.id == contract_id:
                for (index, service) in enumerate(contract.services):
                    if service.id == service_id:
                        contract.services[index] = PenaltyFee(service_id, unit_price, description, penalties)

    def service_edit_extra(self, contract_id: str, service_id: str, unit_price: float, description: str):
        for contract in self.contracts:
            if contract.id == contract_id:
                for (index, service) in enumerate(contract.services):
                    if service.id == service_id:
                        contract.services[index] = ExtraService(service_id, unit_price, description)

    def service_delete(self, contract_id: str, service_id: str):
        for contract in self.contracts:
            if contract.id == contract_id:
                contract.services = list(filter(lambda service: service.id != service_id, contract.services))

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
