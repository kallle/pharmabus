DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Patients;
DROP TABLE IF EXISTS Pharmacies;
DROP TABLE IF EXISTS Doctors;
DROP TABLE IF EXISTS Patients;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Prescriptions;
DROP TABLE IF EXISTS Order_Status;
DROP TABLE IF EXISTS Prescription_Status;
DROP TABLE IF EXISTS Routes;
DROP TABLE IF EXISTS Stops;
DROP TABLE IF EXISTS Stop_Types;


CREATE TABLE Users (
       id          integer primary key,
       pwd         text,
       surname     text,
       familyname  text,
       plz         text,
       street      text,
       streetno    integer,
       longitude   double,
       latitude    double
);


CREATE TABLE Patients (
       user_id        integer,
       FOREIGN KEY (user_id)
       REFERENCES Users(id)
);


CREATE TABLE Doctors (
       user_id        integer,
       FOREIGN KEY (user_id)
       REFERENCES Users(id)
);


CREATE TABLE Pharamacies (
       name           text,
       user_id        integer,
       FOREIGN KEY (user_id)
       REFERENCES Users(id)
);


CREATE TABLE Order_Status (
       name         text PRIMARY KEY,
);


INSERT INTO Order_Status (name)
VALUES ('at_patient'),
       ('at_doctor'),
       ('at_pharmacy'),
       ('at_driver'),
       ('delivered');


CREATE TABLE Prescription_Status (
       name         text PRIMARY KEY,
);


INSERT INTO Prescription_Status (name)
VALUES ('at_patient'),
       ('at_doctor');


CREATE TABLE Prescriptions (
       id                  integer PRIMARY KEY,
       status              text,
       scan                blob,
       FOREIGN KEY (status)
       REFERENCES Prescription_Status(name)
);


CREATE TABLE Routes (
       id           integer PRIMARY KEY
);


CREATE TABLE Stop_Types (
       name            text
);

INSERT INTO Stop_Types (name)
VALUES ('pick_up_recipe'),
       ('pick_up_med'),
       ('drop_off');


CREATE TABLE Stops (
       step_no     integer,
       belogs_to   integer,
       part_of     integer,
       stop_type   text,
       FOREIGN KEY (belongs_to)
       REFERENCES Routes(id),
       FOREIGN KEY (part_of)
       REFERENCES Orders(id)
       FOREIGN KEY (stop_type)
       REFERENCES Stop_Types (name)
);


CREATE TABLE Orders (
       id           integer PRIMARY KEY,
       title        text,
       status       text,
       presription  integer,
       patient      integer,
       doctor       integer,
       pharmacy     integer,
       FOREIGN KEY (status)
       REFERENCES Order_Status(name),
       FOREIGN KEY (prescription)
       REFERENCES Presciptions(id),
       FOREIGN KEY  (patient)
       REFERENCES Patients(id),
       FOREIGN KEY  (doctor)
       REFERENCES Doctors(id),
       FOREIGN KEY  (pharmacy)
       REFERENCES Pharmacies(id)
);

CREATE TABLE Drivers (
       user_id        integer,
       current_route  integer,
       FOREIGN KEY (user_id)
       REFERENCES Users(id),
       FOREIGN KEY (current_route)
       REFERENCES Routes(id)
);
