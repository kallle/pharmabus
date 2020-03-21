DROP TABLE IF EXISTS Drivers CASCADE;
DROP TABLE IF EXISTS Patients CASCADE;

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


CREATE TABLE order_content (
       order_id             integer primary key,
       med_id               integer primary key,
       served_by            integer,
       amount               integer,
       recipe_with_customer integer,
       FOREIGN KEY (order_id)
       REFERENCES orders (id),
       FOREIGN KEY (med_id)
       REFERENCES meds (id),
       FOREIGN KEY (served_by)
       REFERENCES pharmacies (id)
);


CREATE TABLE pharmacy_stores (
       pharmacy     integer primary key,
       med          integer primary key,
       amount       integer,
       FOREIGN KEY (pharmacy)
       REFERENCES pharmacies(id),
       FOREIGN KEY (med)
       REFERENCES meds(id)
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

