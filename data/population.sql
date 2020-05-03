INSERT INTO Users (id, email, pwd, surname, familyname, plz, street, streetno, longitude, latitude) VALUES
(1, 'overlord@example.de', 'pbkdf2:sha256:150000$szP3j8W9$8f72ef81ecd16045b7749338b9865f908f403ded92aa0ff0f970fa6d9740d485', 'Simon', 'Koch', '40722', 'Secret', 42, 1234.4, 4432.1),
(2, 'doctor@example.de'  , 'pbkdf2:sha256:150000$szP3j8W9$8f72ef81ecd16045b7749338b9865f908f403ded92aa0ff0f970fa6d9740d485', 'Simon', 'Koch', '40722', 'Secret', 42, 1234.4, 4432.1),
(3, 'pharmacy@example.de', 'pbkdf2:sha256:150000$szP3j8W9$8f72ef81ecd16045b7749338b9865f908f403ded92aa0ff0f970fa6d9740d485', 'Simon', 'Koch', '40722', 'Secret', 42, 1234.4, 4432.1),
(4, 'patient@example.de' , 'pbkdf2:sha256:150000$szP3j8W9$8f72ef81ecd16045b7749338b9865f908f403ded92aa0ff0f970fa6d9740d485', 'Simon', 'Koch', '40722', 'Secret', 42, 1234.4, 4432.1),
(5, 'driver@example.de'  , 'pbkdf2:sha256:150000$szP3j8W9$8f72ef81ecd16045b7749338b9865f908f403ded92aa0ff0f970fa6d9740d485', 'Simon', 'Koch', '40722', 'Secret', 42, 1234.4, 4432.1);

INSERT INTO Overlords(user_id)
VALUES (1);

INSERT INTO Pharmacies(user_id, name)
VALUES (3, 'Convinient Drug Store');

INSERT INTO Doctors(user_id)
VALUES (2);

INSERT INTO Patients(user_id)
VALUES (4);

INSERT INTO Drivers(user_id, max_range)
VALUES (5, 42);
