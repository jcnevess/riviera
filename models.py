# coding: utf-8

from dataclasses import dataclass, field
from enum import Enum
from typing import List
from datetime import datetime, date


@dataclass
class Address:
    id: int
    street: str
    street_number: str
    additional_info: str
    neighborhood: str
    zipcode: str
    city: str
    state: str
    country: str

    def to_json(self):
        result = self.__dict__.copy()
        result.pop('id')
        return result


@dataclass
class Guest:
    id: int
    name: str
    social_number: str
    birth_date: date
    phone_number: str
    address: Address

    def to_json(self):
        return {
            'id': self.id,
            'social_number': self.social_number,
            'name': self.name,
            'birth_date': self.birth_date,
            'phone_number': self.phone_number,
            'address': self.address.to_json()
        }


@dataclass
class Product:
    id: int
    name: str
    price: float
    quantity: int

    def to_json(self):
        return self.__dict__.copy()


@dataclass
class Service:
    id: int

    def get_price(self):
        return 0.0

    def to_json(self):
        pass


@dataclass
class RoomRental(Service):
    product: Product
    additional_bed: bool
    days: int
    SERVICE_TYPE: str = 'room_rental'

    def get_price(self):
        total_value = 0.0
        total_value += self.days * self.product.price

        return total_value

    def to_json(self):
        return {
            'id': self.id,
            'service_type': self.SERVICE_TYPE,
            'rental_type': self.product.name,
            'daily_price': self.product.price,
            'days': self.days,
            'additional_bed': self.additional_bed,
            'service_price': self.get_price()
        }


class CarRentalType(str, Enum):
    LUXURY = 'luxury'
    EXECUTIVE = 'executive'


@dataclass
class CarRental(Service):
    products: List[Product]
    car_plate: str
    full_gas: bool
    car_insurance: bool
    days: int
    SERVICE_TYPE: str = 'car_rental'

    def get_price(self):
        total_value = 0.0

        for product in self.products:
            if product.name in ['car_luxury', 'car_executive']:
                total_value += product.price * self.days
            else:
                total_value += product.price

        return total_value

    def to_json(self):
        rental_type = list(filter(lambda prod: prod.name in ['car_luxury', 'car_executive'], self.products))[0]

        return {
            'id': self.id,
            'service_type': self.SERVICE_TYPE,
            'rental_type': rental_type.name,
            'daily_price': rental_type.price,
            'days': self.days,
            'car_plate': self.car_plate,
            'full_gas': self.full_gas,
            'car_insurance': self.car_insurance,
            'service_price': self.get_price()
        }


@dataclass
class Babysitter(Service):
    product: Product
    normal_hours: int
    extra_hours: int
    SERVICE_TYPE: str = 'babysitter'

    def get_price(self):
        total_value = 0.0
        total_value += self.normal_hours * self.product.price
        total_value += self.extra_hours * (self.product.price * 2)
        return total_value

    def to_json(self):
        return {
            'id': self.id,
            'service_type': self.SERVICE_TYPE,
            'normal_hours': self.normal_hours,
            'hourly_price': self.product.price,
            'extra_hours': self.extra_hours,
            'hourly_price_extra': (self.product.price * 2),
            'service_price': self.get_price()
        }


@dataclass
class Meal(Service):
    unit_price: float
    description: str
    SERVICE_TYPE: str = 'meal'

    def get_price(self):
        return self.unit_price

    def to_json(self):
        return {
            'id': self.id,
            'service_type': self.SERVICE_TYPE,
            'description': self.description,
            'unit_price': self.unit_price,
            'service_price': self.get_price()
        }


@dataclass
class PenaltyFee(Service):
    unit_price: float
    description: str
    penalties: int
    SERVICE_TYPE: str = 'penalty_fee'

    def get_price(self):
        return self.unit_price * self.penalties

    def to_json(self):
        return {
            'id': self.id,
            'service_type': self.SERVICE_TYPE,
            'description': self.description,
            'unit_price': self.unit_price,
            'penalties': self.penalties,
            'service_price': self.get_price()
        }


@dataclass
class ExtraService(Service):
    unit_price: float
    description: str
    SERVICE_TYPE: str = 'extra_service'

    def get_price(self):
        return self.unit_price

    def to_json(self):
        return {
            'id': self.id,
            'service_type': self.SERVICE_TYPE,
            'description': self.description,
            'unit_price': self.unit_price,
            'service_price': self.get_price()
        }


class BillingStrategy:
    def get_base_bill(self, services: List[Service]):
        bill_value = 0.0
        for service in services:
            bill_value += service.get_price()

        return bill_value

    def get_multiplier(self):
        return 1.0

    def get_bill(self, services: List[Service]):
        return self.get_base_bill(services) * self.get_multiplier()


class HolidaySeasonStrategy(BillingStrategy):
    __MULTIPLIER = 1.2

    def get_multiplier(self):
        return self.__MULTIPLIER

    def get_bill(self, services: List[Service]):
        return super().get_base_bill(services) * self.get_multiplier()


class JuneSeasonStrategy(BillingStrategy):
    __MULTIPLIER = 1.1

    def get_multiplier(self):
        return self.__MULTIPLIER

    def get_bill(self, services: List[Service]):
        return super().get_base_bill(services) * self.get_multiplier()


class JuneHighSeasonStrategy(BillingStrategy):
    __MULTIPLIER = 1.5

    def get_multiplier(self):
        return self.__MULTIPLIER

    def get_bill(self, services: List[Service]):
        return super().get_base_bill(services) * self.get_multiplier()


class LowSeasonStrategy(BillingStrategy):
    __MULTIPLIER = 0.8

    def get_multiplier(self):
        return self.__MULTIPLIER

    def get_bill(self, services: List[Service]):
        return super().get_base_bill(services) * self.get_multiplier()


@dataclass
class Review:
    id: int
    rating: int
    comment: str

    def to_json(self):
        return self.__dict__.copy()


@dataclass
class Contract:
    id: int
    guest: Guest
    card_number: str
    checkin_time: datetime
    contracted_days: int
    services: List[Service] = field(default_factory=list)
    billing_strategy: BillingStrategy = BillingStrategy()
    is_open: bool = True
    review: Review = None

    def to_json(self):
        return {
            'id': self.id,
            'guest': self.guest.to_json(),
            'card_number': self.card_number,
            'checkin_time': self.checkin_time,
            'contracted_days': self.contracted_days,
            'is_open': self.is_open,
            'services': list(map(lambda s: s.to_json(), self.services)),
            'services_price': self.billing_strategy.get_base_bill(self.services),
            'price_multiplier': self.billing_strategy.get_multiplier(),
            'total_price': self.billing_strategy.get_bill(self.services)
        }
