/*
 *
 */

 set FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS visit;
DROP TABLE IF EXISTS message;
DROP TABLE IF EXISTS lab_order;
DROP TABLE IF EXISTS lab_test;
DROP TABLE IF EXISTS login;
DROP TABLE IF EXISTS patient;
DROP TABLE IF EXISTS provider;


create table patient(
  patientID           int               not null auto_increment,
  patientName         varchar(30)       not null,
  patientAddress      varchar(50)       not null,
  patientPhone        char(10)          not null,
  patientPCP          int,
  patientEmail	      varchar(255),

    primary key (patientID)

);

create table provider(
  providerID          int               not null auto_increment,
  providerName        varchar(30)       not null,
  providerLicense     varchar(10)       not null,
  providerSpecialty   varchar(30)       not null,
  providerNPI         char(10)          not null,
  providerEmail       varchar(255),

    primary key (providerID)
);

create table login(
  email       varchar(255)    not null,
  password      varchar(30)     not null,
  loginType     char(3)       not null,

    primary key(email)
);

create table visit(
  visitID             int            not null auto_increment,
  providerID          int            not null,
  patientID           int            not null,
  visitDate           DATETIME,
  visitStatus         varchar(15),

    primary key (visitID)

) ;

create table message(
  messageID          int             not null auto_increment,
  patientID          int             not null,
  providerID         int             not null,
  messageSubject     varchar(30),
  messageBody        varchar(1000),
  messageDate        DATETIME,
  senderPT     BOOLEAN,

    primary key (messageID)

);

create table lab_order (
  orderID       int       not null auto_increment,
  patientID     int       not null,
  cpt         varchar(15)   not null,
  orderDate     DATE,
  completeDate    DATE,
  results       varchar(50),

  primary key (orderID)
);

create table lab_test (
  cpt       varchar(15)   not null,
  labName       varchar(15)   not null,
  labType       char(1),

  primary key (cpt)
);

set foreign_key_checks=1;

alter table patient ADD foreign key (patientPCP) references provider(providerID);
alter table visit ADD foreign key (providerID) references provider(providerID);
alter table visit ADD foreign key (patientID) references patient(patientID);
alter table message ADD foreign key (patientID) references patient(patientID);
alter table message ADD foreign key (providerID) references provider(providerID);
alter table lab_order ADD foreign key (cpt) references lab_test(cpt)
