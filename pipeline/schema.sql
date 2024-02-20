-- This file should contain table definitions for the database.

DROP TABLE IF EXISTS cai_schema.transaction;
DROP TABLE IF EXISTS cai_schema.payment_type;
DROP TABLE IF EXISTS cai_schema.truck;

CREATE TABLE cai_schema.truck (
    truck_id INT GENERATED ALWAYS AS IDENTITY,
    truck_name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(250) UNIQUE NOT NULL,
    has_card_reader BOOLEAN NOT NULL,
    FSA_rating SMALLINT NOT NULL,
    PRIMARY KEY (truck_id)
);

CREATE TABLE cai_schema.payment_type (
    payment_type_id INT GENERATED ALWAYS AS IDENTITY,
    payment_type_name VARCHAR(10) UNIQUE NOT NULL,
    PRIMARY KEY (payment_type_id)
);

CREATE TABLE cai_schema.transaction (
    transaction_id INT GENERATED ALWAYS AS IDENTITY,
    total SMALLINT NOT NULL,
    at TIMESTAMPTZ NOT NULL,
    truck_id INT NOT NULL,
    payment_type_id INT NOT NULL,
    PRIMARY KEY (transaction_id),
    FOREIGN KEY (truck_id)
        REFERENCES cai_schema.truck(truck_id),
    FOREIGN KEY (payment_type_id)
        REFERENCES cai_schema.payment_type(payment_type_id)
);

INSERT INTO cai_schema.truck(truck_name, description, has_card_reader, FSA_rating)
        VALUES
    ('Burrito Madness', 'An authentic taste of Mexico.', True, 4),
    ('Kings of Kebabs', 'Locally-sourced meat cooked over a charcoal grill.', True, 2),
    ('Cupcakes by Michelle', 'Handcrafted cupcakes made with high-quality, organic ingredients.', True, 5),
    ('Hartmann''s Jellied Eels', 'A taste of history with this classic English dish.', True , 4),
    ('Yoghurt Heaven', 'All the great tastes, but only some of the calories!', True, 4),
    ('SuperSmoothie', 'Pick any fruit or vegetable, and we''ll make you a delicious, healthy, multi-vitamin shake. Live well; live wild.', False, 3);

INSERT INTO cai_schema.payment_type(payment_type_name)
        VALUES
    ('cash'),
    ('card');