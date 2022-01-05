# coding: utf-8

from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar, List
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


@dataclass
class Guest:
    name: str 
    social_number: str
    birthdate: str
    address: Address


@dataclass
class Service:
    id: str

    def get_price(self):
        return 0.0


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

    __PRESIDENTIAL_PRICE: ClassVar[float] = 1200.0
    __LUXURY_SIMPLE_PRICE: ClassVar[float] = 520.0
    __LUXURY_DOUBLE_PRICE: ClassVar[float] = 570.0
    __LUXURY_TRIPLE_PRICE: ClassVar[float] = 620.0
    __EXECUTIVE_SIMPLE_PRICE: ClassVar[float] = 360.0
    __EXECUTIVE_DOUBLE_PRICE: ClassVar[float] = 385.0
    __EXECUTIVE_TRIPLE_PRICE: ClassVar[float] = 440.0

    def get_price(self):
        total_value = 0.0

        if self.rental_type == RoomRentalType.PRESIDENTIAL:
            total_value += self.days * RoomRental.__PRESIDENTIAL_PRICE
        elif self.rental_type == RoomRentalType.LUXURY_SIMPLE:
            total_value += self.days * RoomRental.__LUXURY_SIMPLE_PRICE
        elif self.rental_type == RoomRentalType.LUXURY_DOUBLE:
            total_value += self.days * RoomRental.__LUXURY_DOUBLE_PRICE
        elif self.rental_type == RoomRentalType.LUXURY_TRIPLE:
            total_value += self.days * RoomRental.__LUXURY_TRIPLE_PRICE
        elif self.rental_type == RoomRentalType.EXECUTIVE_SIMPLE:
            total_value += self.days * RoomRental.__EXECUTIVE_SIMPLE_PRICE
        elif self.rental_type == RoomRentalType.EXECUTIVE_DOUBLE:
            total_value += self.days * RoomRental.__EXECUTIVE_DOUBLE_PRICE
        elif self.rental_type == RoomRentalType.EXECUTIVE_TRIPLE:
            total_value += self.days * RoomRental.__EXECUTIVE_TRIPLE_PRICE

        return total_value


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

    __LUXURY_PRICE: ClassVar[float] = 100.0
    __EXECUTIVE_PRICE: ClassVar[float] = 60.0
    __FULL_GAS_FEE: ClassVar[float] = 60.0
    __INSURANCE_FEE: ClassVar[float] = 60.0

    def get_price(self):
        total_value = 0.0

        if self.rental_type == CarRentalType.LUXURY:
            total_value += self.days * CarRental.__LUXURY_PRICE
        elif self.rental_type == CarRentalType.EXECUTIVE:
            total_value += self.days * CarRental.__EXECUTIVE_PRICE

        if self.full_gas:
            total_value += CarRental.__FULL_GAS_FEE

        if self.car_insurance:
            total_value += CarRental.__INSURANCE_FEE

        return total_value


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


@dataclass
class Meal(Service):
    value: float
    description: str    
    SERVICE_TYPE: str = 'meal'

    def get_price(self):
        return self.value


@dataclass
class ExtraService(Service):
    value: float
    description: str
    SERVICE_TYPE: str = 'extra_service'

    def get_price(self):
        return self.value


class BillingStrategy:
    def get_bill(self, services: List[Service]):
        bill_value = 0.0
        for service in services:
            bill_value += service.get_price()

        return bill_value


class HolidaySeasonStrategy(BillingStrategy):
    def get_bill(self, services: List[Service]):
        return super().get_bill(services) * 1.2


class JuneSeasonStrategy(BillingStrategy):
    def get_bill(self, services: List[Service]):
        return super().get_bill(services) * 1.1


class JuneHighSeasonStrategy(BillingStrategy):
    def get_bill(self, services: List[Service]):
        return super().get_bill(services) * 1.5


class LowSeasonStrategy(BillingStrategy):
    def get_bill(self, services: List[Service]):
        return super().get_bill(services) * 0.8


@dataclass
class Contract(Service):
    id: str
    guest: Guest
    card_number: str
    checkin_date: datetime
    days_contracted: int
    services: List[Service] = field(default_factory=list)
    is_open: bool = True
    billing_strategy: BillingStrategy = BillingStrategy()
