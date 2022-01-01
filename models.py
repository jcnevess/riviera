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
    pass

class RoomRentalKind(Enum):
    PRESIDENTIAL = 1200.0
    LUXURY_SIMPLE = 520.0
    LUXURY_DOUBLE = 570.0
    LUXURY_TRIPLE = 620.0
    EXECUTIVE_SIMPLE = 360.0
    EXECUTIVE_DOUBLE = 385.0
    EXECUTIVE_TRIPLE = 440.0

@dataclass
class RoomRental(Service):
    rental_kind: RoomRentalKind
    additional_bed: bool
    days: int

class CarRentalKind(Enum):
    LUXURY = 100.0
    EXECUTIVE = 60.0

@dataclass
class CarRental(Service):
    rental_kind: CarRentalKind
    car_plate: str
    full_gas: bool
    car_insurance: bool
    days: int

@dataclass
class Babysitter(Service):
    value: ClassVar[float] = 25.0
    normal_hours: int
    extra_hours: int

@dataclass
class Meal(Service):
    value: float

@dataclass
class ExtraService(Service):
    value: float