INSERT INTO patient
(patientName, patientAddress, patientPhone, patientPCP, patientEmail)
values
("Bob", "102 Learning Lane", '1234567890', 1, "Bob@luc.edu"),
("Jane", "321 SQL Court", '234567890', 2, "Jane@luc.edu"),
("Jacob", "133 Jake Lane", '3456789010', 2, "Jacob@luc.edu"),
("John Doe", "666 SQL Lane", '0567891234', 2, "JohnDoe@luc.edu"),
("Patient Name", "102 Patient Address", '8912345670', 1, "PatientName@luc.edu"),
("Alexis", "321 street Court", '234567891', 2, "Alexis@luc.edu");

INSERT INTO provider
(providerName, providerLicense, providerSpecialty, providerNPI, providerEmail)
values
("Kate", "Doctor", "Fam Med", '50562', "Kate@luc.edu"),
("Trevor", "Doctor", "Peds", '50626', "Trevor@luc.edu");

INSERT INTO login
(email, password, loginType)
values
("Trevor@luc.edu", "pass", "prv"),
("patient@luc.edu","pass","pat");

INSERT INTO visit
(providerID, patientID, visitDate, visitStatus)
values
(1, 1, '2008-11-11 13:23:44', "Completed"),
(1, 2, '2009-11-11 13:30:44', "Completed"),
(2, 1, '2010-04-12 09:45:12', "Completed"),
(1, 2, '2021-01-01 12:00:00', "Scheduled");

INSERT INTO message
(patientID, providerID, messageSubject, messageBody, messageDate, senderPT)
values
(1, 1, "advice", "I need advice about my diagnosis", '2008-11-11 13:23:44', 1),
(2, 1, "medication question", "what does my med do", '2011-12-04 01:01:01', 1),
(1, 1, "doc", "hello doc this is a message body", '2020-03-15 06:06:06', 1);

INSERT INTO lab_order
(patientID, cpt, orderDate, completeDate, results)
values
(1, "CPT120", '2011-06-12', '2011-07-12', "Positive"),
(2, "CPT240", '2019-08-01', '2019-09-01', "Negative");

INSERT INTO lab_test
(cpt, labName, labType)
values
("CPT120", "TestLab120", 'B'),
("CPT240", "TestLab240", 'U');
