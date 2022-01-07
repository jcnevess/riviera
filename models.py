# coding: utf-8

from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar, List, Dict
from datetime import datetime


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

    def to_json(self):
        return self.__dict__


@dataclass
class Guest:
    name: str 
    social_number: str
    birthdate: str
    address: Address

    def to_json(self):
        return {
            'social_number': self.social_number,
            'name': self.social_number,
            'birthdate': self.birthdate,
            'address': self.address.to_json()
        }


@dataclass
class Service:
    id: str

    def get_price(self):
        return 0.0

    def to_json(self):
        pass


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
    
    __price: ClassVar[Dict[RoomRentalType, float]] = {
        RoomRentalType.PRESIDENTIAL: 1200.0,
        RoomRentalType.LUXURY_SIMPLE: 520.0,
        RoomRentalType.LUXURY_DOUBLE: 570.0,
        RoomRentalType.LUXURY_TRIPLE: 620.0,
        RoomRentalType.EXECUTIVE_SIMPLE: 360.0,
        RoomRentalType.EXECUTIVE_DOUBLE: 385.0,
        RoomRentalType.EXECUTIVE_TRIPLE: 440.0
    }

    def get_price(self):
        total_value = 0.0
        total_value += self.days * RoomRental.__price[self.rental_type]

        return total_value

    def to_json(self):
        return {
            'id': self.id,
            'service_type': self.SERVICE_TYPE,
            'rental_type': self.rental_type.value,
            'daily_price': self.__price[self.rental_type],
            'days': self.days,
            'additional_bed': self.additional_bed,
            'service_price': self.get_price()
        }


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

    __price: ClassVar[Dict[CarRentalType, float]] = {
        CarRentalType.LUXURY: 100.0,
        CarRentalType.EXECUTIVE: 60.0
    }
    __FULL_GAS_FEE: ClassVar[float] = 60.0
    __INSURANCE_FEE: ClassVar[float] = 60.0

    def get_price(self):
        total_value = 0.0

        if self.rental_type == CarRentalType.LUXURY:
            total_value += self.days * CarRental.__price[CarRentalType.LUXURY]
        elif self.rental_type == CarRentalType.EXECUTIVE:
            total_value += self.days * CarRental.__price[CarRentalType.EXECUTIVE]

        if self.full_gas:
            total_value += CarRental.__FULL_GAS_FEE

        if self.car_insurance:
            total_value += CarRental.__INSURANCE_FEE

        return total_value

    def to_json(self):
        return {
            'id': self.id,
            'service_type': self.SERVICE_TYPE,
            'rental_type': self.rental_type.value,
            'daily_price': self.__price[self.rental_type],
            'days': self.days,
            'car_plate': self.car_plate,
            'full_gas': self.full_gas,
            'car_insurance': self.car_insurance,
            'service_price': self.get_price()
        }


@dataclass
class Babysitter(Service):
    normal_hours: int
    extra_hours: int
    SERVICE_TYPE: str = 'babysitter'

    __NORMAL_PRICE: ClassVar[float] = 25.0
    __EXTRA_PRICE: ClassVar[float] = __NORMAL_PRICE * 2

    def get_price(self):
        total_value = 0.0
        total_value += self.normal_hours * Babysitter.__NORMAL_PRICE
        total_value += self.extra_hours * Babysitter.__EXTRA_PRICE
        return total_value

    def to_json(self):
        return {
            'id': self.id,
            'service_type': self.SERVICE_TYPE,
            'normal_hours': self.normal_hours,
            'hourly_price': self.__NORMAL_PRICE,
            'extra_hours': self.extra_hours,
            'hourly_price_extra': self.__EXTRA_PRICE,
            'service_price': self.get_price()
        }


@dataclass
class Meal(Service):
    value: float
    description: str    
    SERVICE_TYPE: str = 'meal'

    def get_price(self):
        return self.value

    def to_json(self):
        return {
            'id': self.id,
            'service_type': self.SERVICE_TYPE,
            'description': self.description,
            'value': self.value,
            'service_price': self.get_price()
        }


@dataclass
class PenaltyFee(Service):
    value: float
    description: str
    penalties: int
    SERVICE_TYPE: str = 'penalty_fee'

    def get_price(self):
        return self.value * self.penalties

    def to_json(self):
        return {
            'id': self.id,
            'service_type': self.SERVICE_TYPE,
            'description': self.description,
            'value': self.value,
            'penalties': self.penalties,
            'service_price': self.get_price()
        }


@dataclass
class ExtraService(Service):
    value: float
    description: str
    SERVICE_TYPE: str = 'extra_service'

    def get_price(self):
        return self.value

    def to_json(self):
        return {
            'id': self.id,
            'service_type': self.SERVICE_TYPE,
            'description': self.description,
            'value': self.value,
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

    def get_final_bill(self, services: List[Service]):
        return self.get_base_bill(services) * self.get_multiplier()


class HolidaySeasonStrategy(BillingStrategy):
    __MULTIPLIER = 1.2

    def get_multiplier(self):
        return self.__MULTIPLIER

    def get_final_bill(self, services: List[Service]):
        return super().get_base_bill(services) * self.get_multiplier()


class JuneSeasonStrategy(BillingStrategy):
    __MULTIPLIER = 1.1

    def get_multiplier(self):
        return self.__MULTIPLIER

    def get_final_bill(self, services: List[Service]):
        return super().get_base_bill(services) * self.get_multiplier()


class JuneHighSeasonStrategy(BillingStrategy):
    __MULTIPLIER = 1.5

    def get_multiplier(self):
        return self.__MULTIPLIER

    def get_final_bill(self, services: List[Service]):
        return super().get_base_bill(services) * self.get_multiplier()


class LowSeasonStrategy(BillingStrategy):
    __MULTIPLIER = 0.8

    def get_multiplier(self):
        return self.__MULTIPLIER

    def get_final_bill(self, services: List[Service]):
        return super().get_base_bill(services) * self.get_multiplier()


@dataclass
class Contract:
    id: str
    guest: Guest
    card_number: str
    checkin_date: datetime
    days_contracted: int
    billing_strategy: BillingStrategy = BillingStrategy()
    services: List[Service] = field(default_factory=list)
    is_open: bool = True

    def to_json(self):
        return {
            'id': self.id,
            'guest': self.guest.to_json(),
            'card_number': self.card_number,
            'checkin_date': self.checkin_date,
            'days_contracted': self.days_contracted,
            'is_open': self.is_open,
            'services': list(map(lambda s: s.to_json(), self.services)),
            'services_price': self.billing_strategy.get_base_bill(self.services),
            'price_multiplier': self.billing_strategy.get_multiplier(),
            'total_price': self.billing_strategy.get_final_bill(self.services)
        }
