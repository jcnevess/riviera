# coding: utf-8

from dataclasses import dataclass

@dataclass
class Address:
    street: str
    number: str
    additional_info: str
    neighborhood: str
    zipcode: str
    city: str
    state: str 
    country: str


@dataclass
class Guest:
    name: str 
    social_number: str
    birthdate: str
    address: Address
    credit_card_number: str

