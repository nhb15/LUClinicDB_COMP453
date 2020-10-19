/*
 *
 */

DROP TABLE IF EXISTS patient
DROP TABLE IF EXISTS provider
DROP TABLE IF EXISTS visit
DROP TABLE IF EXISTS message

create table patient(
  patientID           int               not null auto_increment,
  patientName         varchar(30)       not null,
  patientAddress      varchar(50)       not null,
  patientPhone        char(10)          not null,
  patientPCP          int,
  patientPassword     varchar(15),

    primary key (patientID)
    foreign key (patientPCP) references provider(providerID)
);

create table provider(
  providerID          int               not null auto_increment,
  providerName        varchar(30)       not null,
  providerLicense     varchar(10)       not null,
  providerSpecialty   varchar(30)       not null,
  providerNPI         char(10)          not null,
  providerPassword    varchar(15),

    primary key (providerID)
);

create table visit(
  visitID             int            not null auto_increment,
  providerID          int            not null,
  patientID           int            not null,
	visitDate           DATETIME,
  visitStatus         varchar(15),

    primary key (visitID)
    foreign key (providerID) references provider(providerID)
    foreign key (patientID) references patient(patientID)
) ;

create table message(
	messageID          int             not null auto_increment,
	senderID           int             not null,
	recipientID        int             not null,
	messageSubject     varchar(30),
	messageBody        varchar(1000),
	messageDate        DATETIME,

    primary key (messageID)
    /*foreign key (senderID) references p */

/* set foreign_key_checks=0; */
);

INSERT INTO visit
(providerID, patientID, visitDate, visitStatus)
values
(1, 1, '2008-11-11 13:23:44', "Completed"),
(1, 2, '2009-11-11 13:30:44', "Completed"),
(2, 1, '2010-04-12 09:45:12', "Completed"),
(1, 2, '2021-01-01 12:00:00', "Scheduled");

INSERT INTO message
(senderID, recipientID, subject, body, messageDate)
values
(1, 1, "advice", "I need advice about my diagnosis", '2008-11-11 13:23:44'),
(2, 1, "medication question", "what does my med do", '2011-12-04 01:01:01'),
(1, 1, "doc", "hello doc this is a message body", '2020-03-15 06:06:06');


/* set foreign_key_checks=1;  */
/*
alter table employee ADD foreign key (super_ssn) references employee(ssn);
alter table employee ADD foreign key (dno) references department(dnumber);
*/
