# LUClinic

Repo for the group project for LUC class COMP 453 - Database Programming.

Members of the project group are:

- Nate Boldt
- Valerie Boudas
- Anshul Shanker

---

# Business Requirements

**What is the title of this application?**

LU Clinic Patient & Provider Portal

**What is the organization/business for whom this application is being developed?**

Loyola University Clinic

**What is the mission of this organization?**

To provide quality medical care to all patients.

**What is the purpose of this application?**

LUClinic is a portal for both patients and providers to view/change their appointments, display details regarding their health records, and also serves as a messaging system between the patient and the provider.

**Why will this application support the mission of the organization?**

Accurate and complete medical records are important for care of the patient.

**Provide an ER diagram of the database, both before and after any structural changes.  See point #3 under Technical Requirements.**

See ERD located in Documentation folder.

**Walk through how this application is used, both as a user and as an adminstrator.**

(See PowerPoint presentation.)

**During your demonstration, be sure to point out the technical specifications below. But make sure that the technical features make sense in the context of your application.  For example, if you are demonstrating an aggregate function, you might say, "This is a query that tells us how many orders each customer has placed.  This is useful if we are trying to analyze repeat business.**

**You will probably find it easier to take screen shots of your data entry, validation and queries, and paste them into PPT slides.  In this way, your presentation will be smoother, you won't rely upon scrolling through results or navigating through your application during your presentation.  In addition, you won't have any unpleasant surprises if your server goes down or any other unanticipated issues arise.**

---

# Technical Requirements
**Some of the technical specifications/components of the project:**

- **Include at least one structural change to the database using DDL.  (Create, Alter, Drop). Clearly, your application will be written on one version of the design.  So you may satisfy this requirement by discussing what changes in the business requirements might precipitate a change in the design, and how would you implement that?  An example would be:  the design is based on the reality that every employee is assigned to exactly one department.  But the company has changed its management structure to a more project-based structure, and now, employees can be assigned to multiple departments.  This necessitates a change in the cardinaly of department:employee from 1:n to m:n.  This now requires a new relationship entity.  Other examples might include changing the format of a zip code from XXXXX to XXXXX-xxxx.**

   * Currently, patients cannot reschedule appointments themselves. (The 'Reschedule' button does nothing.)  If patients were given the ability to reschedule on their own, they would need to know what days/times are available for scheduling. To accomplish this, another table (appointment_times) would need to be added with information about provider schedules and available appointment slots.  This table would have a 1:1 relationship with both the provider and visit tables (each available slot could only have one scheduled visit with one provider). ProviderID would be added as a FK in the appointment_times table and the visit table would need an additional FK referencing the PK of the appointment_times tuple that it references. (Valerie)

- **Provide the DDL as well as the INSERT SQL for creating the tables and initially populating the database.  You may do this in any text editor and then paste into the SQL window of PHMyAdmin, or you may use the DDL from the terminal or from within a Python program, as demonstrated in class.**

  * Both the Create and Insert DDL SQL files are located in DDL folder. (Nate & Valerie)

- **Include at least one insertion of a new record that will occur during the execution of the application.  This will most likely be as the result of a transaction or some component that should be added to the database.  For instance, in our labs, we added a department, and we also added an employee-project assignment.  Both of these required the insertion of a new record in the database.  In regular SQL, this would use the INSERT statement.  However, you should use Flask-SQLAlchemy for this purpose.**

  * See addPatient (Nate)

- **Include at least one update of a record--changing an existing record, not adding a new one.  Use SQLAlchemy.**

  * See modifyPatient (Nate).

- **Include at least one delete of a record.  Use SQLAlchemy.**

  * See cancel_visit in LuClinic.py, lines 304-310 (Valerie).

- **Include at least one simple SELECT SQL statement.  Use regular SQL for this.  This will require a database connection using one of packages that were showed in Lab-4-connect.**

  * See My Patients (Nate).

- **Include one query using Flask-SQLAlchemy filter or filter_by.**

    * See appointments in LuClnic.py, lines 283-293 (Valerie). This function lists both scheduled and completed appointments for the logged in patient.

- **Inlcude at least one SELECT using an aggregate function.  Use regular SQL for this.**
  * Within the myPatients route, we select a count of the patients for the logged in provider. (Nate)
`cur.execute("SELECT DISTINCT COUNT(patientID) FROM patient WHERE patientPCP = '%d'" % providerID)`

- **Include at least one SELECT using a compound condition using regular SQL, and also the equivalent of a compound condition select using Flask-SQLAlchemy.**
      
    * SQL : /admin route LuClinic.py Line 389 (Anshul)
      Patient ID's of all the patients that have both messaged and visited.
      ```
      SELECT DISTINCT patientID FROM message INTERSECT SELECT DISTINCT patientID FROM visit
      ```
    * Flask-SQLAlchemy :  /admin route LuClinic.py Line 398 (Anshul)
      Patients that have both Atorvastatin and Omeprazole prescribed
      ```
      ator = dbAlchemy.session.query(Prescription.patientID).filter(Prescription.medID==4)
      omep = dbAlchemy.session.query(Prescription.patientID).filter(Prescription.medID==7)
      medCombinations = ator.intersect(omep).all()
      ```

- **Include at least one JOIN query using SQL, and also one using Flask-SQLAlchemy.**

  * See profile in LuClinic.py, lines 154-155 (uses SQL). This part of the function lists different parts of the patient's health record on their home page. And appointments (uses SQLAlchemy) in LUClinic.py, line 289 (Valerie). This function lists both scheduled and completed appointments for the logged in patient (also uses filter).

- **Include at least one subquery.  Regular SQL.  Excellence points if you also use Flask-SQLAlchemy.**

    * Flask-SQLAlchemy : /admin route LuClinic.py Line 411(Anshul)
      List of all Patients that have been prescribed 'mg' dosage
      ```
       subquery = dbAlchemy.session.query(Prescription.patientID).filter(Prescription.dosage.like('%mg%')).subquery()
       mgDose = dbAlchemy.session.query(Patient).filter(Patient.patientID.in_(subquery)).all()
      ```      
    
    * SQL : (Anshul)
      ```sql
      SELECT * FROM Patients WHERE patientID IN (SELECT patientID FROM Prescription WHERE dosage like '%mg%')
      ```

- **Use a form to collect user data, as shown in our CRUD labs.**

    * /registerProvider and /registerPatient routes LuClinic.py Line 79 and 104 (Anshul)

- **Populate a field on a form or table from the database.  This would most likely be for your update, and you can model this directly off of our examples in class.**

    * See Modify Patient (Nate).

- **Check for empty data fields. You can use the built-in validations for this.**

    * Modify Patient and Add Patient (Nate).

- **Implement referential intergrity.  Demonstrate what happens when it is violated. Or, if you constructed your program so that it can't be violated, demonstrate how it references a primary key and prevents a violation of referential intergrity.  For example, if employee has a foreign key deptNo that references the primary key deptNo in the relation Department.  If you populate a drop-down box with existing department numbers, this will prevent the user from entering an invalid department number, thereby enforcing referential integrity.  We did something similar in Lab-4-c.  If you just have a text box, the user can enter a department number that doesn't exist, and you can demonstrate that this will cause a referential integrity error.  Either method is fine, but be clear on what you are trying to achieve and demonstrate.**

  * All tables have foreign keys to prevent violations except for the Login table, which allows patients to register asynchronously from a Patient record being created for them. There are no other tables with the same attributes that aren't foreign keys. If something is updated in one table that has a foreign key link in another, it updates both tables. The system is specifically set up to avoid patient email integrity violations by not allowing anyone to edit the patient email. (Valerie) (Nate)

- **Use an appropriate structure for your project package.  Any of the structures that we used in class is fine.  I would recommend using the structure that we used for Lab-4-c, as that is a good starting point for the project.**

  * (Nate and Anshul). The LuClinic file holds all the routes, exclusively. 

---

# Goals for E.C.

- **Using additional flask or flask-sqlalchemy features that we did not cover in class.**

  * Using Flask-Session (Anshul). WebApp uses session to log-in users and mantain their login status. When they logout or close the browser the session keys are cleared.

- **Using additonal WTForms components that we did not cover in class. (Examples:  importing other html form components that we did not demonstrate in class; check boxes, radio buttons, etc. multiple drop-down boxes)**

- **A correlated subquery.**

- **A Flask-SQLAlchemy subquery.**

    * Flask-SQLAlchemy : /admin route LuClinic.py Line 411(Anshul)
      List of all Patients that have been prescribed 'mg' dosage
      ```
       subquery = dbAlchemy.session.query(Prescription.patientID).filter(Prescription.dosage.like('%mg%')).subquery()
       mgDose = dbAlchemy.session.query(Patient).filter(Patient.patientID.in_(subquery)).all()
      ```

- **An especially complex query.**

- **An especially complex ERD.**

- **Additions to your html that add to the functionality, navigability or appeal of your website.  This includes bootstrap that we didn't use in class.**

- **Javascript, JQuery, other client-side programming**
    
    
# Known Broken Links

- ** Not an exhaustive list yet, but to start: **

  *Appointments when logged in as a provider
  
  *Rescheduling an appointment when viewing a specific appointment as a patient
