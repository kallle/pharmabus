DROP TABLE IF EXISTS drivers;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS pharmacies;
DROP TABLE IF EXISTS meds;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS order_contains;
DROP TABLE IF EXISTS pharmacy_stores;
DROP TABLE IF EXISTS users;


CREATE TABLE drivers (
       id               integer primary key,
       Name             text,
       range            integer,
       addr_plz         integer,
       addr_street      text,
       addr_street_nr   integer,
       koo              text,
       cooler_dim_x     integer,
       cooler_dim_y     integer,
       cooler_dim_z     integer,
       storage_dim_x    integer,
       storage_dim_y    integer,
       storage_dim_z    integer
);

CREATE TABLE patients (
       id               integer primary key,
       Name             text,
       addr_plz         integer,
       addr_street      text,
       addr_street_nr   integer,
       koo              text
);


CREATE TABLE pharmacies (
       id               integer primary key,
       Name             text,
       addr_plz         integer,
       addr_street      text,
       addr_street_nr   integer,
       koo              text
);


CREATE TABLE meds (
       id           integer primary key,
       pzn          text,
       product_name text,
       ingredient   text,
       quantity     text,
       dimension_x  integer,
       dimension_y  integer,
       dimension_z  integer,
       requries_cooling integer
);


CREATE TABLE orders (
       id           integer primary key,
       status       text,
       given_by     patient,
       driven_by    integer,
       FOREIGN KEY (given_by)
       REFERENCES patients(id),
       FOREIGN KEY (driven_by)
       REFERENCES drivers (id)
);


CREATE TABLE order_contains (
       order_id             integer,
       med_id               integer,
       served_by            integer,
       amount               integer,
       recipe_with_customer integer,
       PRIMARY KEY (order_id, med_id),
       FOREIGN KEY (order_id)
       REFERENCES orders (id),
       FOREIGN KEY (med_id)
       REFERENCES meds (id),
       FOREIGN KEY (served_by)
       REFERENCES pharmacies (id)
);


CREATE TABLE pharmacy_stores (
       pharmacy_id  integer,
       med_id       integer,
       amount       integer,
       PRIMARY KEY (pharmacy_id, med_id),
       FOREIGN KEY (pharmacy_id)
       REFERENCES pharmacies(id),
       FOREIGN KEY (med_id)
       REFERENCES meds (id)
);


CREATE TABLE Users (
       id          integer primary key,
       username    text,
       pwd         text,
       salt        text,
       driver_id   integer,
       pharmacy_id integer,
       patient_id  integer
);

