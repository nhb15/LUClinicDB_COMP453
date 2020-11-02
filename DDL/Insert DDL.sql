INSERT INTO login
(email, password, loginType)
values
("kate@luc.edu", "pass", "prv"),
("trevor@luc.edu", "pass", "prv"),
("jasper@patient.com","pass","pat");

INSERT INTO provider
(providerName, providerLicense, providerSpecialty, providerNPI, providerEmail)
values
("Kate", "MD", "Internal Medicine", '50562', "kate@luc.edu"),
("Trevor", "DO", "Pediatrics", '50626', "trevor@luc.edu"),
("Molly", "RN", "Internal Medicine", '1648974940', "molly@luc.edu"),
("Chris", "NP", "Pediatrics", "2458904332", "chris@luc.edu");

INSERT INTO patient
(patientName, patientAddress, patientPhone, patientPCP, patientEmail)
values
("Jasper", "102 Patient Address", '8912345670', 1, "jasper@patient.com"),
("Yuri", "899 Harvey Way", '7773334421', 1, "yuri@patient.com"),
("Holly", "732 Cricket Street", '4418097265', 1, "haleigh@patient.com"),
("Jacob", "133 Jake Lane", '3456789010', 2, "jacob@patient.com"),
("Alexis", "321 Street Court", '234567891', 2, "alexis@patient.com"),
("Olivia", "591 Millenial Court", '7714658970', 2, "olivia@patient.com");

/* should consider adding visit reason and adding separate table for availble appointment slots*/
INSERT INTO visit
(providerID, patientID, visitDate, visitStatus)
values
(1, 1, '2008-11-11 13:23:44', "Completed"),
(3, 1, '2021-01-01 12:00:00', "Scheduled"),
(1, 2, '2009-11-11 13:30:44', "Completed"),
(1, 2, '2021-04-12 09:45:12', "Scheduled"),
(1, 3, '2009-11-11 13:30:44', "Completed"),
(3, 3, '2021-04-12 09:45:12', "Scheduled"),
(2, 4, '2009-11-11 13:30:44', "Completed"),
(2, 4, '2021-04-12 09:45:12', "Scheduled"),
(2, 6, '2009-11-11 13:30:44', "Completed"),
(4, 6, '2021-04-12 09:45:12', "Scheduled");

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
(1, "CPT120", '2011-06-12', '2011-07-12', "Negative"),
(2, "CPT120", '2011-06-12', '2011-07-12', "Negative"),
(2, "CPT120", '2011-06-12', '2011-07-12', "Positive"),
(4, "CPT120", '2011-06-12', '2011-07-12', "Negative"),
(5, "CPT120", '2011-06-12', '2011-07-12', "Positive"),
(5, "CPT120", '2011-06-12', '2011-07-12', "Positive"),
(6, "CPT120", '2011-06-12', '2011-07-12', "Negative"),
(6, "CPT120", '2011-06-12', '2011-07-12', "Positive"),
(6, "CPT240", '2019-08-01', '2019-09-01', "Negative");

INSERT INTO lab_test
(cpt, labName, labType)
values
("CPT120", "TestLab120", 'B'),
("CPT240", "TestLab240", 'U');

set foreign_key_checks=1;

alter table patient ADD foreign key (patientPCP) references provider(providerID);
alter table visit ADD foreign key (providerID) references provider(providerID);
alter table visit ADD foreign key (patientID) references patient(patientID);
alter table message ADD foreign key (patientID) references patient(patientID);
alter table message ADD foreign key (providerID) references provider(providerID);
alter table lab_order ADD foreign key (cpt) references lab_test(cpt);
alter table health_issues ADD foreign key (icd_10_cm) references diagnosis(icd_10_cm);
alter table health_issues ADD foreign key (patientID) references patient(patientID);
alter table prescription ADD foreign key (rxID) references rx_substance(rxID);
alter table prescription ADD foreign key (patientID) references patient(patientID);
alter table allergy ADD foreign key (rxID) references rx_substance(rxID);
alter table allergy ADD foreign key (patientID) references patient(patientID);
