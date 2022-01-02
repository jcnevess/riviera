# coding: utf-8

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar

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


@dataclass
class Service:
    id: str

class RoomRentalType(str, Enum):
    PRESIDENTIAL = 'presidential'
    LUXURY_SIMPLE = 'luxury_simple'
    LUXURY_DOUBLE = 'luxury_double'
    LUXURY_TRIPLE = 'luxury_triple'
    EXECUTIVE_SIMPLE = 'executive_simple'
    EXECUTIVE_DOUBLE = 'executive_double'
    EXECUTIVE_TRIPLE = 'executive_triple'

@dataclass
class RoomRental(Service):
    rental_type: RoomRentalType
    additional_bed: bool
    days: int
    SERVICE_TYPE: str = 'room_rental'

class CarRentalType(str, Enum):
    LUXURY = 'luxury'
    EXECUTIVE = 'executive'

@dataclass
class CarRental(Service):
    rental_type: CarRentalType
    car_plate: str
    full_gas: bool
    car_insurance: bool
    days: int
    SERVICE_TYPE: str = 'car_rental'

@dataclass
class Babysitter(Service):
    value: ClassVar[float] = 25.0
    normal_hours: int
    extra_hours: int
    SERVICE_TYPE: str = 'babysitter'

@dataclass
class Meal(Service):
    value: float
    description: str    
    SERVICE_TYPE: str = 'meal'

@dataclass
class ExtraService(Service):
    value: float
    description: str
    SERVICE_TYPE: str = 'extra_service'