INSERT INTO login
(email, password, loginType)
values
("kate@luc.edu", "pass", "prv"),
("trevor@luc.edu", "pass", "prv"),
("molly@luc.edu", "pass", "prv"),
("chris@luc.edu", "pass", "prv"),
("jasper@patient.com","pass","pat"),
("yuri@patient.com", "pass", "pat"),
("holly@patient.com", "pass", "pat"),
("steve@patient.com", "pass", "pat"),
("alexis@patient.com", "pass", "pat"),
("olivia@patient.com", "pass", "pat");

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
("Holly", "732 Cricket Street", '4418097265', 1, "holly@patient.com"),
("Steve", "133 Boogie Lane", '3456789010', 1, "steve@patient.com"),
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
(2, 6, '2019-11-12 14:20:22', "Completed"),
(4, 6, '2021-04-12 09:45:12', "Scheduled");

INSERT INTO message
(patientID, providerID, messageSubject, messageBody, messageDate, senderPT)
values
(1, 1, "advice", "I need advice about my diagnosis.", '2008-11-11 13:23:44', 1),
(1, 1, "medication question", "what does my med do?", '2011-12-04 01:01:01', 1),
(1, 1, "lab results", "are my lab results in?", '2011-12-04 01:01:01', 1),
(3, 1, "moving out of state", "can i get a copy of my medical records?", '2011-12-04 01:01:01', 1),
(4, 2, "feeling tired", "do i need to make an appointment?", '2011-12-04 01:01:01', 1),
(4, 2, "is this normal", "my nose runs when i eat.", '2011-12-04 01:01:01', 1),
(5, 2, "billing question", "what is this charge on my bill", '2011-12-04 01:01:01', 1),
(5, 2, "medical certification", "i need this form signed for my job", '2011-12-04 01:01:01', 1),
(6, 2, "vaccines", "i refuse to vaccinate my child", '2017-12-04 01:01:01', 1),
(6, 2, "covid", "how can i stop my child from getting covid", '2020-09-15 06:06:06', 1);

/* B = blood, U = urine, S = saliva, F = fecal */
INSERT INTO lab_test
(cpt, labName, labType)
values
("10165", "Basic Metabolic Panel", 'B'),
("10231", "Comprehensive Metabolic Panel", 'B'),
("14852", "Lipid Panel with Reflex to Direct LDL", 'B'),
("07020", "Thyroid Panel", 'B'),
("10256", "Hepatic Function Panel", 'B'),
("06399", "Complete Blood Count (includes Differential and Platelets)", 'B'),
("08847", "Prothrombin Time with INR", 'B'),
("17306", "Vitamin D, 25-Hydroxy, Total, Immunoassay", "B"),
("19897", "Cortisol, LC/MS, Saliva", 'S'),
("05463", "Urinalysis, Complete", 'U');

INSERT INTO lab_order
(patientID, cpt, orderDate, completeDate, results)
values
(1, "10165", '2018-06-12', '2018-07-12', "Normal"),
(1, "14852", '2020-04-19', NULL, NULL),
(2, "07020", '2011-03-10', '2011-03-13', "Abnormal"),
(2, "05463", '2019-01-31', '2011-02-02', "Normal"),
(4, "17306", '2020-09-22', NULL, NULL),
(5, "07020", '2016-11-15', '2016-11-22', "Normal"),
(5, "19897", '2011-08-28', NULL, NULL),
(6, "10165", '2020-10-09', NULL, NULL),
(6, "10256", '2014-06-17', '2014-07-02', "Abnormal"),
(6, "06399", '2019-07-24', '2019-08-01', "Abnormal");

INSERT INTO diagnosis
(icd_10_cm, diagnosisName)
values
("E11.9", "Type 2 Diabetes Mellitus Without Complications"),
("I11.9", "Hypertensive Heart Disease Without Heart Failure"),
("J45.909", "Unspecified Asthma, Uncomplicated"),
("G47.00", "Insomnia, Unspecified"),
("E03.9", "Hypothyroidism, Unspecified"),
("D50.9", "Iron Deficiency Anemia, Unspecified"),
("B17.10", "Acute Hepatitis C Without Hepatic Coma"),
("N20.0", "Calculus Of Kidney"),
("G43.909", "Migraine, Unspecified, Not Intractable, Without Status Migrainosus"),
("I49.9", "Cardiac Arrhythmia, Unspecified");

INSERT INTO health_issues
(icd_10_cm, patientID)
values
("G47.00", 1),
("E03.9", 1),
("N20.0", 2),
("I11.9", 3),
("I49.9", 4),
("G43.909", 4),
("J45.909", 4),
("E11.9", 4),
("E03.9", 5),
("D50.9", 5);

INSERT INTO medication
(medName)
values
("Atorvastatin"),
("Lisinopril"),
("Albuterol"),
("Levothyroxine"),
("Amlodipine"),
("Gabapentin"),
("Omeprazole"),
("Metformin"),
("Losartan"),
("Hydrocodone/Acetaminophen");

INSERT INTO prescription
(patientID, medID, dosage)
values
(1, 4, "125 mcg"),
(1, 7, "1 mg"),
(2, 1, "300 mcg"),
(2, 6, "25 mg"),
(3, 3, "90 mg"),
(4, 4, "75 mcg"),
(4, 8, "900 mg"),
(4, 3, "75 mcg"),
(4, 10, "100 mg"),
(5, 2, "70 mcg"),
(6, 9, "450 mcg");

INSERT INTO allergen
(allergenName, allergenType)
values
("cat dander", "animal"),
("ragweed", "environmental"),
("dust mites", "animal"),
("mold", "environmental"),
("peanuts", "food"),
("shellfish", "food"),
("insect sting", "animal"),
("maple pollen", "environmental"),
("latex", "material"),
("eggs", "food");

INSERT INTO allergy
(patientID, medID, allergenID, reaction)
values
(2, NULL, 3, "rash"),
(3, 2, NULL, "shortness of breath"),
(4, NULL, 5, "swollen tongue"),
(4, NULL, 1, "rash"),
(4, NULL, 9, "itchy eyes"),
(4, 10, NULL, "chest tightness"),
(4, NULL, 10, "rash"),
(5, 6, NULL, "swollen face"),
(5, 9, NULL, "rash"),
(6, NULL, 8, "itchy eyes");

alter table patient ADD foreign key (patientPCP) references provider(providerID);
alter table patient ADD foreign key (patientEmail) references login(email);
alter table provider ADD foreign key (providerEmail) references login(email);
alter table visit ADD foreign key (providerID) references provider(providerID);
alter table visit ADD foreign key (patientID) references patient(patientID);
alter table message ADD foreign key (patientID) references patient(patientID);
alter table message ADD foreign key (providerID) references provider(providerID);
alter table lab_order ADD foreign key (patientID) references patient(patientID);
alter table lab_order ADD foreign key (cpt) references lab_test(cpt);
alter table health_issues ADD foreign key (icd_10_cm) references diagnosis(icd_10_cm);
alter table health_issues ADD foreign key (patientID) references patient(patientID);
alter table prescription ADD foreign key (patientID) references patient(patientID);
alter table prescription ADD foreign key (medID) references medication(medID);
alter table allergy ADD foreign key (patientID) references patient(patientID);
alter table allergy ADD foreign key (medID) references medication(medID);
alter table allergy ADD foreign key (allergenID) references allergen(allergenID);

set foreign_key_checks=1;
