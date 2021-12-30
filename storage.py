# coding: utf-8

from models import *
from typing import List

guests: List[Guest] = []

''' Guest methods. Using SSN as id for now. '''
def guest_getall():
    return guests

def guest_getbyid(id): 
    return list(filter(lambda guest: guest.social_number == id, guests))

def guest_add(name: str, social_number: str, birthdate: str, \
                address_street: str, address_number: str, address_additional_info: str, \
                address_neighborhood: str, address_zipcode: str, address_city: str, \
                address_state: str , address_country: str, credit_card_number: str):

    address = Address(address_street, address_number, address_additional_info, address_neighborhood, \
        address_zipcode, address_city, address_state, address_country)
        
    guests.append(Guest(name, social_number, birthdate, address, credit_card_number))

def guest_edit(id: str, name: str, social_number: str, birthdate: str, \
                address_street: str, address_number: str, address_additional_info: str, \
                address_neighborhood: str, address_zipcode: str, address_city: str, \
                address_state: str , address_country: str, credit_card_number: str):

    address = Address(address_street, address_number, address_additional_info, address_neighborhood, \
        address_zipcode, address_city, address_state, address_country)
        
    for (index, guest) in enumerate(guests):
        if guest.social_number == id:
            guests[index] = Guest(name, social_number, birthdate, address, credit_card_number)