# coding: utf-8

import uuid

from models import *
from typing import List, Dict
from datetime import datetime


class Storage:
    guests: List[Guest] = []
    services: List[Service] = []
    contracts: List[Contract] = []

    available_rooms: Dict[RoomRentalType, int] = {
        RoomRentalType.PRESIDENTIAL: 5,
        RoomRentalType.LUXURY_SIMPLE: 5,
        RoomRentalType.LUXURY_DOUBLE: 15,
        RoomRentalType.LUXURY_TRIPLE: 20,
        RoomRentalType.EXECUTIVE_SIMPLE: 5,
        RoomRentalType.EXECUTIVE_DOUBLE: 15,
        RoomRentalType.EXECUTIVE_TRIPLE: 20
    }

    ''' Helper methods '''

    @staticmethod
    def __get_room_rental_type(rental_type: str):
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

    @staticmethod
    def __get_car_rental_type(rental_type: str):
        if rental_type == 'luxury':
            return CarRentalType.LUXURY
        elif rental_type == 'executive':
            return CarRentalType.EXECUTIVE

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
        return self.guests

    def guest_getbyid(self, guest_id: str):
        return list(filter(lambda guest: guest.social_number == guest_id, self.guests))[0]

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

    ''' Contract methods '''

    def contract_getall(self):
        return self.contracts

    def contract_getbyid(self, contract_id: str):
        return list(filter(lambda contract: contract.id == contract_id, self.contracts))[0]

    def contract_add(self, guest_id: str, card_number: str, checkin_date: str, days_contracted: int, billing_strategy: str):
        id = uuid.uuid4().hex
        guest = self.guest_getbyid(guest_id)
        date = datetime.fromisoformat(checkin_date)
        bill_strategy = self.__get_billing_strategy(billing_strategy)
        self.contracts.append(Contract(id, guest, card_number, date, days_contracted, billing_strategy=bill_strategy))
        return id

    def contract_edit(self, contract_id: str, guest_id: str, card_number: str, checkin_date: str, days_contracted: int, is_open: bool):
        guest = self.guest_getbyid(guest_id)
        date = datetime.fromisoformat(checkin_date)

        for (index, contract) in enumerate(self.contracts):
            if contract.id == contract_id:
                self.contracts[index] = Contract(contract_id, guest, card_number, date, days_contracted, contract.services, is_open=is_open)

    def contract_delete(self, contract_id: str):
        self.contracts = list(filter(lambda contract: contract.id != contract_id, self.contracts))

    ''' Service methods '''

    def service_getall(self, contract_id: str):
        return [service for contract in self.contracts if contract.id == contract_id for service in contract.services]

    def service_getbyid(self, contract_id: str, service_id: str):
        return [service for contract in self.contracts if contract.id == contract_id for service in contract.services if service.id == service_id][0]

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
        room_rental_type = self.__get_room_rental_type(rental_type)
        for contract in self.contracts:
            if contract.id == contract_id:
                for (index, service) in enumerate(contract.services):
                    if service.id == service_id:
                        contract.services[index] = RoomRental(service_id, room_rental_type, additional_bed, days)

    def service_edit_car(self, contract_id: str, service_id: str, rental_type: str, car_plate: str, full_gas: bool, car_insurance: bool,
                         days: int):
        car_rental_type = self.__get_car_rental_type(rental_type)
        for contract in self.contracts:
            if contract.id == contract_id:
                for (index, service) in enumerate(contract.services):
                    if service.id == service_id:
                        contract.services[index] = CarRental(service_id, car_rental_type, car_plate, full_gas, car_insurance, days)

    def service_edit_babysitter(self, contract_id: str, service_id: str, normal_hours: int, extra_hours: int):
        for contract in self.contracts:
            if contract.id == contract_id:
                for (index, service) in enumerate(contract.services):
                    if service.id == service_id:
                        contract.services[index] = Babysitter(service_id, normal_hours, extra_hours)

    def service_edit_meal(self, contract_id: str, service_id: str, unit_price: float, description: str):
        for contract in self.contracts:
            if contract.id == contract_id:
                for (index, service) in enumerate(contract.services):
                    if service.id == service_id:
                        contract.services[index] = Meal(service_id, unit_price, description)

    def service_edit_penalty_fee(self, contract_id: str, service_id: str, unit_price: float, description: str, penalties: int):
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
        return self.available_rooms

    def room_book(self, rental_type: str):
        self.available_rooms[Storage.__get_room_rental_type(rental_type)] -= 1

    def room_unbook(self, rental_type: str):
        self.available_rooms[Storage.__get_room_rental_type(rental_type)] += 1

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
