set FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS patient;
DROP TABLE IF EXISTS provider;
DROP TABLE IF EXISTS login;
DROP TABLE IF EXISTS visit;
DROP TABLE IF EXISTS message;
DROP TABLE IF EXISTS lab_test;
DROP TABLE IF EXISTS lab_order;
DROP TABLE IF EXISTS diagnosis;
DROP TABLE IF EXISTS health_issues;
DROP TABLE IF EXISTS rx_substance;
DROP TABLE IF EXISTS prescription;
DROP TABLE IF EXISTS allergy;

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

);

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

create table lab_test (
  cpt       varchar(15)   not null,
  labName       varchar(15)   not null,
  labType       char(1),

  primary key (cpt)
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

create table diagnosis (
  icd_10_cm          varchar(7)      not null,
  diagnosisName      varchar(50)     not null,

  primary key (icd_10_cm)
);

create table health_issues (
  icd_10_cm     varchar(7)    not null,
  patientID     int           not null,

  primary key (icd_10_cm, patientID)
);

create table rx_substance (
  rxID        varchar(10)     not null,
  rxName      varchar(50)     not null,

  primary key (rxID)
);

create table prescription (
  rxID        varchar(10)     not null,
  patientID     int           not null,
  dosage      varchar (5)     not null,

  primary key (rxID, patientID)
);

create table allergy (
  rxID        varchar(10)     not null,
  patientID     int           not null,
  reaction      varchar(25)   not null,

  primary key (rxID, patientID)
);
