INSERT INTO drivers VALUES
(1, 'Karl der Grosse'    ,  100, 38100, 'Marstall' , 42, 52.26548, 	10.52356, 10, 20, 10, 10, 20, 30),
(2, 'Mellaroy Archer' ,  20, 14057, 'Kurfuerstendamm'    , 123, 	52.50023,  	13.31, 10, 20, 30, 10, 20, 30),
(3, 'Ray Gillette'   ,  50, 14476, 'Tristanstr.'     , 11, 52.45701,  	13.10295, 10, 20, 30, 10, 20, 30),
(4, 'Roby Bubble'   ,  75, 81377, 'Eichendorffstr.'     , 42, 48.1148493, 11.5486665, 10, 20, 30, 10, 20, 30),
(5, 'Simone Kuechenmeister'   ,  10, 38118, 'Luisenstr.'     , 7, 52.2558,  10.509346, 10, 20, 30, 10, 20, 30),
(6, 'Goliat Gross'   ,  30, 80331, 'Waldstr.'     , 18, 48.1148483, 11.4786645, 10, 15, 20, 10, 20, 30);


INSERT INTO pharmacies VALUES
(1, 'Hagenmarkt Apotheke', 38100, 'Hagenmarkt', 19, 52.267770, 10.524170),
(2, 'Arkaden-Apotheke', 38100, 'Ritterbrunnen', 1, 52.265090, 10.528030),
(3, 'Sofien-Apotheke' 38118, 'Sophienstraße', 28, 52.258260, 10.506750),
(4, 'APONEO öffentliche Apotheke' 10365 , 'Frankfurter Allee', 241, 52.512040, 13.496970),
(5, 'Meraner Apotheke' 10825, 'Meraner Str.', 16, 52.4866223, 13.3386726),
(6, 'Suarez Apotheke' 14057, 'Suarezstraße', 64, 52.5074305, 13.2950865),
(7, 'MediosApotheke Oranienburger Tor' 10117, 'Friedrichstraße', 113a, 52.5260999, 13.3876281),
(8, 'Rats Apotheke Gauting' 82131, 'Bahnhofstraße', 2, 48.0669554, 11.3798203),
(9, 'Marys pharmacy Grosshadern' 81377, 'Heiglhofstraße', 4A, 48.1148493, 11.4786665),
(10, 'Rosen Apotheke' 80331, 'Rosenstraße', 6, 48.1364717, 11.5738671);


INSERT INTO meds VALUES
(1, 3867219, 'ACC 200 Brausetabletten', 'Acetylcystein', 'Hexal', '50 Stk', 10, 5 , 5, 0, 0),
(2, 3920801, 'ACC 100 Brausetabletten', 'Acetylcystein', 'Hexal', '100 Stk', 10, 5 , 5, 0, 0),
(3, 7112908, 'ACE HEMMER 12,5 mg', 'Captopril', 'ratiopharm', '100 Stk', 10, 7 , 3, 0, 1),
(4, 7112920, 'ACE HEMMER 25 mg', 'Captopril', 'ratiopharm', 10, 7 , 3, 0, 1),
(5, 9091300, 'ACICLOVIR 200 mg', 'Aciclovir', 'ratiopharm', '25 Stk', 5, 5, 5, 0, 1),
(6, 870439, 'ACICLOVIR 50 mg', 'Aciclovir', '1A Pharma', '2 g', 5, 5, 5, 0, 1),
(7, 6977954, 'ACICLOVIR 50 mg', 'Aciclovir', 'HEUMANN PHARMA', '2 g', 5, 5, 5, 0, 0),
(8, 3628124, 'ASPIRIN 500 mg', 'Acetylsalicylsaere', 'Abis-Pharma', '20 Stk', 10, 5, 1, 0, 0),
(9, 6977954, 'ASPIRIN 500 mg', 'Acetylsalicylsaere', 'Bayer', '8 Stk', 5, 4, 2, 0, 0),
(10, 10203632, 'ASPIRIN 500 mg', 'Acetylsalicylsaere', 'Bayer', '80 Stk', 5, 4, 5, 0, 0),
(11, 2949599, 'Tamiflu 45 mg', 'Oseltamivir phosphat', 'Roche Pharma', '10 Stk', 3, 7, 1, 0, 1),
(12, 2948625, 'Tamiflu 30 mg', 'Oseltamivir phosphat', 'Roche Pharma', '10 Stk', 3, 7, 1, 0, 1),
(13, 890287, 'Tamiflu 75 mg', 'Oseltamivir phosphat', 'Roche Pharma', '10 Stk', 3, 7, 1, 0, 1),
(14, 11528543, 'Dolormin Ibuprofensaft 40 mg/ml', 'Ibuprofen', 'Johnson & Johnson', '100 ml', 5, 12, 4, 0, 0),
(15, 7770675, 'DOC Ibuprofen Scherzgel 5 %', 'Ibuprofen', 'Hermes Arzneimittel', '150 g', 5, 12, 3, 0, 0),
(16, 13506652, 'Ibuprofen 400 mg', 'Ibuprofen', 'Fair-Med Healthcare', '20 Stk', 6, 3, 2, 0, 0),
(17, 6876785, 'Ibuprofen 600 mg', 'Ibuprofen', 'ALIUD Pharma', '20 Stk', 6, 3, 2, 0, 1),
(18, 4478201, 'Paracetamol Suppositorien 1000 mg', 'Paracetamol', '1A Pharma', '10 Stk', 6, 3, 2, 0, 0),
(19, 1234473, 'Paracetamol 500 mg', 'Paracetamol', 'AbZ-Pharma', '10 Stk', 6, 3, 2, 0, 0)
(20, 7524686, 'L-Thyrox 75 ug', 'Levothyroxin natrium', 'Hexal', '98 Stk', 6, 3, 2, 0, 1),
(21, 2532735, 'L-Thyrox 75 ug', 'Levothyroxin natrium', 'Sanofi-Aventis Deutschland', '50 Stk', 6, 3, 1, 0, 1),
(22, 11100905, 'Erbitux 5 mg/ml', 'Paracetamol', 'EurimPharm Arzneimittel', '100 ml', 3, 3, 8, 1, 1),
(23, 9929393, 'Heparin 25.000 I.E.', 'Heparin Natrium', 'B. Braun Melsungen', '10 x 5 ml', 10, 20, 3, 1, 1),
(24, 8875844, 'RESOCHIN Tabletten 250 mg', 'Chloroquin phosphat', 'ACA Müller/ADAG Pharma', '100 Stk', 5, 3, 2, 0, 1),
(25, 3276398, 'KALETRA 200 mg/50 mg', 'Ritonavir Lopinavir', 'HAEMATO PHARM', '120 Stk', 6, 3, 2, 0, 0);

INSERT INTO pharmacy_stores VALUES
(1, 1, 1),
(1, 2, 2),
(1, 3, 3),
(2, 1, 4),
(2, 5, 5),
(2, 6, 5);

