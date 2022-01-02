# coding: utf-8

import uuid

from models import *
from typing import List

class Storage:
    guests: List[Guest] = []
    services: List[Service] = []
    
    ''' Guest methods. Using SSN as id for now. '''
    def guest_getall(self):
        return self.guests

    def guest_getbyid(self, id: str): 
        return list(filter(lambda guest: guest.social_number == id, self.guests))

    def guest_add(self, name: str, social_number: str, birthdate: str, \
                    address_street: str, address_number: str, address_additional_info: str, \
                    address_neighborhood: str, address_zipcode: str, address_city: str, \
                    address_state: str , address_country: str, credit_card_number: str):

        address = Address(address_street, address_number, address_additional_info, address_neighborhood, \
            address_zipcode, address_city, address_state, address_country)
            
        self.guests.append(Guest(name, social_number, birthdate, address, credit_card_number))

    def guest_edit(self, id: str, name: str, social_number: str, birthdate: str, \
                    address_street: str, address_number: str, address_additional_info: str, \
                    address_neighborhood: str, address_zipcode: str, address_city: str, \
                    address_state: str , address_country: str, credit_card_number: str):

        address = Address(address_street, address_number, address_additional_info, address_neighborhood, \
            address_zipcode, address_city, address_state, address_country)
            
        for (index, guest) in enumerate(self.guests):
            if guest.social_number == id:
                self.guests[index] = Guest(name, social_number, birthdate, address, credit_card_number)


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
        return self.services

    def service_getbyid(self, id: str):
        return list(filter(lambda service: service.id == id, self.services))

    def service_add_room(self, rental_type: str, additional_bed: bool, days: int):
        id = uuid.uuid4().hex
        room_rental_type = self.__get_room_rental_type(rental_type)
        self.services.append(RoomRental(id, room_rental_type, additional_bed, days))
        return id

    def service_add_car(self, rental_type: str, car_plate: str, full_gas: bool, car_insurance: bool, days: int):
        id = uuid.uuid4().hex
        car_rental_type = self.__get_car_rental_type(rental_type)
        self.services.append(CarRental(id, car_rental_type, car_plate, full_gas, car_insurance, days))
        return id

    def service_add_babysitter(self, normal_hours: int, extra_hours: int):
        id = uuid.uuid4().hex
        self.services.append(Babysitter(id, normal_hours, extra_hours))
        return id

    def service_add_meal(self, value: float, description: str):
        id = uuid.uuid4().hex
        self.services.append(Meal(id, value, description))
        return id

    def service_add_extra(self, value: float, description: str):
        id = uuid.uuid4().hex
        self.services.append(ExtraService(id, value, description))
        return id

    def service_edit_room(self, id: str, rental_type: str, additional_bed: bool, days: int):
        room_rental_type = self.__get_room_rental_type(rental_type)
        for (index, service) in enumerate(self.services):
            if service.id == id:
                self.services[index] = RoomRental(id, room_rental_type, additional_bed, days)

    def service_edit_car(self, id: str, rental_type: str, car_plate: str, full_gas: bool, car_insurance: bool, days: int):
        car_rental_type = self.__get_car_rental_type(rental_type)
        for (index, service) in enumerate(self.services):
            if service.id == id:
                self.services[index] = CarRental(id, car_rental_type, car_plate, full_gas, car_insurance, days)

    def service_edit_babysitter(self, id: str, normal_hours: int, extra_hours: int):
        for (index, service) in enumerate(self.services):
            if service.id == id:
                self.services[index] = Babysitter(id, normal_hours, extra_hours)

    def service_edit_meal(self, id: str, value: float, description: str):
        for (index, service) in enumerate(self.services):
            if service.id == id:
                self.services[index] = Meal(id, value, description)

    def service_edit_extra(self, id: str, value: float, description: str):
        for (index, service) in enumerate(self.services):
            if service.id == id:
                self.services[index] = ExtraService(id, value, description)
    
    def service_delete(self, id: str):
        self.services = list(filter(lambda service: service.id != id, self.services))