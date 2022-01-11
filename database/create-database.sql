create database riviera;

use riviera;

create table `guest`(
    `id` int(64) auto_increment,
    `name` varchar(128),
    `social_number` varchar(64),
    `birth_date` date,
    `phone_number` varchar(32),
    `address_street` varchar(128),
    `address_street_number` int(64),
    `address_additional_info` varchar(128),
    `address_neighborhood` varchar(64),
    `address_zipcode` varchar(32),
    `address_city` varchar(64),
    `address_state` varchar(64),
    `address_country` varchar(64),

    primary key (`id`)
);

create table `contract`(
    `id` int(64) auto_increment,
    `guest_id` int(64),
    `checkin_time` datetime,
    `contracted_days` int(32),
    `credit_card_number` varchar(64), -- Stored as plain text because this is a toy example. Don't do this!
    `is_open` boolean,
    `billing_strategy_id` int(64), -- foreign key added later
    `review_id` int(64), -- foreign key added later

    primary key (`id`),
    foreign key (`guest_id`) references `guest`(`id`)
);

create table `contract_billing_strategy`(
    `id` int(64) auto_increment,
    `name` varchar(64),
    `multiplier` decimal(10, 2),

    primary key (`id`)
);

alter table `contract`
    add constraint foreign key (`billing_strategy_id`) references `contract_billing_strategy`(`id`);

create table `review`(
    `id` int(64) auto_increment,
    `rating` int(32),
    `comment` varchar(512),

    primary key (`id`)
);

alter table `contract`
    add constraint foreign key (`review_id`) references `review`(`id`);

create table `product`(
    `id` int(64) auto_increment,
    `name` varchar(64),
    `price` decimal(10,2),
    `quantity` int(32),

    primary key (`id`)
);

create table `service`(
    `id` int(64) auto_increment,
    `contract_id` int(64),

    primary key (`id`),
    foreign key (`contract_id`) references `contract`(`id`)
);

create table `room_rental`(
    `service_id` int(64),
    `product_id` int(64),
    `contracted_days` int(32),
    `has_additional_bed` boolean,

    primary key (`service_id`),
    foreign key (`service_id`) references `service`(`id`) on delete cascade,
    foreign key (`product_id`) references `product`(`id`)
);

create table `car_rental`(
    `service_id` int(64),
    `product_id` int(64),
    `contracted_days` int(32),
    `car_plate` varchar(64),
    `has_full_gas` boolean,
    `has_insurance` boolean,

    primary key (`service_id`),
    foreign key (`service_id`) references `service`(`id`) on delete cascade,
    foreign key (`product_id`) references `product`(`id`)
);

create table `babysitter`(
    `service_id` int(64),
    `product_id` int(64),
    `normal_hours` int(32),
    `extra_hours` int(32),

    primary key (`service_id`),
    foreign key (`service_id`) references `service`(`id`) on delete cascade,
    foreign key (`product_id`) references `product`(`id`)
);

create table `meal`(
    `service_id` int(64),
    `unit_price` decimal(10, 2),
    `description` varchar(512),

    primary key (`service_id`),
    foreign key (`service_id`) references `service`(`id`) on delete cascade
);

create table `extra_service`(
    `service_id` int(64),
    `unit_price` decimal(10, 2),
    `description` varchar(512),

    primary key (`service_id`),
    foreign key (`service_id`) references `service`(`id`) on delete cascade
);

create table `penalty_fee`(
    `service_id` int(64),
    `unit_price` decimal(10, 2),
    `description` varchar(512),
    `penalties` int(32),

    primary key (`service_id`),
    foreign key (`service_id`) references `service`(`id`) on delete cascade
);
