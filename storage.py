# coding: utf-8

import uuid

from models import *
from typing import List
from datetime import datetime


class Storage:
    guests: List[Guest] = []
    services: List[Service] = []
    contracts: List[Contract] = []

    ''' Guest methods. Using SSN as id for now. '''

    def guest_getall(self):
        return self.guests

    # TODO: All methods that take id should explain which id they are referring to (id -> guest_id)
    def guest_getbyid(self, id: str):
        return list(filter(lambda guest: guest.social_number == id, self.guests))[0]

    def guest_add(self, name: str, social_number: str, birthdate: str,
                  address_street: str, address_number: str, address_additional_info: str,
                  address_neighborhood: str, address_zipcode: str, address_city: str,
                  address_state: str, address_country: str):

        address = Address(address_street, address_number, address_additional_info, address_neighborhood,
                          address_zipcode, address_city, address_state, address_country)

        self.guests.append(Guest(name, social_number, birthdate, address))

    def guest_edit(self, id: str, name: str, social_number: str, birthdate: str,
                   address_street: str, address_number: str, address_additional_info: str,
                   address_neighborhood: str, address_zipcode: str, address_city: str,
                   address_state: str, address_country: str):

        address = Address(address_street, address_number, address_additional_info, address_neighborhood,
                          address_zipcode, address_city, address_state, address_country)

        for (index, guest) in enumerate(self.guests):
            if guest.social_number == id:
                self.guests[index] = Guest(name, social_number, birthdate, address)

    ''' Service methods '''

    def __get_room_rental_type(self, rental_type: str):
        if rental_type == 'presidential':
            return RoomRentalType.PRESIDENTIAL
        elif rental_type == 'luxury_simple':
            return RoomRentalType.LUXURY_SIMPLE
        elif rental_type == 'luxury_double':
            return RoomRentalType.LUXURY_DOUBLE
        elif rental_type == 'luxury_triple':
            return RoomRentalType.LUXURY_TRIPLE
        elif rental_type == 'executive_simple':
            return RoomRentalType.EXECUTIVE_SIMPLE
        elif rental_type == 'executive_double':
            return RoomRentalType.EXECUTIVE_DOUBLE
        elif rental_type == 'executive_triple':
            return RoomRentalType.EXECUTIVE_TRIPLE

    def __get_car_rental_type(self, rental_type: str):
        if rental_type == 'luxury':
            return CarRentalType.LUXURY
        elif rental_type == 'executive':
            return CarRentalType.EXECUTIVE

    def service_getall(self):
        return [service for contract in self.contracts for service in contract.services]

    def service_getbyid(self, id: str):
        return list(filter(lambda service: service.id == id, self.service_getall()))[0]

    def service_add_room(self, contract_id: str, rental_type: str, additional_bed: bool, days: int):
        id = uuid.uuid4().hex
        room_rental_type = self.__get_room_rental_type(rental_type)
        for contract in self.contracts:
            if contract.id == contract_id:
                contract.services.append(RoomRental(id, room_rental_type, additional_bed, days))
        return id

    def service_add_car(self, contract_id: str, rental_type: str, car_plate: str, full_gas: bool, car_insurance: bool, days: int):
        id = uuid.uuid4().hex
        car_rental_type = self.__get_car_rental_type(rental_type)
        for contract in self.contracts:
            if contract.id == contract_id:
                contract.services.append(CarRental(id, car_rental_type, car_plate, full_gas, car_insurance, days))
        return id

    def service_add_babysitter(self, contract_id: str, normal_hours: int, extra_hours: int):
        id = uuid.uuid4().hex
        for contract in self.contracts:
            if contract.id == contract_id:
                contract.services.append(Babysitter(id, normal_hours, extra_hours))
        return id

    def service_add_meal(self, contract_id: str, value: float, description: str):
        id = uuid.uuid4().hex
        for contract in self.contracts:
            if contract.id == contract_id:
                contract.services.append(Meal(id, value, description))
        return id

    def service_add_extra(self, contract_id: str, value: float, description: str):
        id = uuid.uuid4().hex
        for contract in self.contracts:
            if contract.id == contract_id:
                contract.services.append(ExtraService(id, value, description))
        return id

    def service_edit_room(self, id: str, contract_id: str, rental_type: str, additional_bed: bool, days: int):
        room_rental_type = self.__get_room_rental_type(rental_type)
        for contract in self.contracts:
            if contract.id == contract_id:
                for (index, service) in enumerate(contract.services):
                    if service.id == id:
                        contract.services[index] = RoomRental(id, room_rental_type, additional_bed, days)

    def service_edit_car(self, id: str, contract_id: str, rental_type: str, car_plate: str, full_gas: bool, car_insurance: bool,
                         days: int):
        car_rental_type = self.__get_car_rental_type(rental_type)
        for contract in self.contracts:
            if contract.id == contract_id:
                for (index, service) in enumerate(contract.services):
                    if service.id == id:
                        contract.services[index] = CarRental(id, car_rental_type, car_plate, full_gas, car_insurance, days)

    def service_edit_babysitter(self, id: str, contract_id: str, normal_hours: int, extra_hours: int):
        for contract in self.contracts:
            if contract.id == contract_id:
                for (index, service) in enumerate(contract.services):
                    if service.id == id:
                        contract.services[index] = Babysitter(id, normal_hours, extra_hours)

    def service_edit_meal(self, id: str, contract_id: str, value: float, description: str):
        for contract in self.contracts:
            if contract.id == contract_id:
                for (index, service) in enumerate(contract.services):
                    if service.id == id:
                        contract.services[index] = Meal(id, value, description)

    def service_edit_extra(self, id: str, contract_id: str, value: float, description: str):
        for contract in self.contracts:
            if contract.id == contract_id:
                for (index, service) in enumerate(contract.services):
                    if service.id == id:
                        contract.services[index] = ExtraService(id, value, description)

    def service_delete(self, id: str):
        for contract in self.contracts:
            contract.services = list(filter(lambda service: service.id != id, contract.services))

    # def service_get_price(self, service_id: str):
    #     service = None
    #     index = 0
    #
    #     while not service:
    #         contract = self.contracts[index]
    #         for serv in contract.services:
    #             if serv.id == service_id:
    #                 service = serv
    #                 break
    #         index += 1
    #
    #     if service:
    #         return service.get_price()
    #     else:
    #         return 0.0  # TODO: This should be an exception

    ''' Contract methods '''

    def contract_getall(self):
        return self.contracts

    def contract_getbyid(self, id: str):
        return list(filter(lambda contract: contract.id == id, self.contracts))[0]

    def contract_add(self, guest_id: str, card_number: str, checkin_date: str, days_contracted: int):
        id = uuid.uuid4().hex
        guest = self.guest_getbyid(guest_id)
        date = datetime.fromisoformat(checkin_date)
        self.contracts.append(Contract(id, guest, card_number, date, days_contracted))
        return id

    def contract_edit(self, id: str, guest_id: str, card_number: str, checkin_date: str, days_contracted: int, is_open: bool):
        guest = self.guest_getbyid(guest_id)
        date = datetime.fromisoformat(checkin_date)

        for (index, contract) in enumerate(self.contracts):
            if contract.id == id:
                self.contracts[index] = Contract(id, guest, card_number, date, days_contracted, contract.services, is_open)

    def contract_delete(self, id: str):
        self.contracts = list(filter(lambda contract: contract.id != id, self.contracts))
