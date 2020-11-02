# LUClinic

Repo for the group project for class COMP 453

LUClinic is a portal for both patients and doctors to view their appointments, display details regarding their medication and also a messaging system between the paitient and the doctor.

Members of the project group are:

- Anshul Shanker
- Nate Boldt
- Valerie Boudas

LAB 4 C LINK: https://docs.google.com/document/d/1E3MqRDxqg0adEL1X2GCCbNieWF-a_31V9HadYXwtaZw/edit?usp=sharing

---

# Business Requirements

What is the title of this application?

**LU Clinic Patient & Provider Portal**

What is the organization/business for whom this application is being developed?

**Loyola University Clinic**

What is the mission of this organization?

What is the purpose of this application?

Why will this application support the mission of the organization?

Provide an ER diagram of the database, both before and after any structural changes.  See point #3 under Technical Requirements.

Walk through how this application is used, both as a user and as an adminstrator.

---

During your demonstration, be sure to point out the technical specifications below. But make sure that the technical features make sense in the context of your application.  For example, if you are demonstrating an aggregate function, you might say, "This is a query that tells us how many orders each customer has placed.  This is useful if we are trying to analyze repeat business."

You will probably find it easier to take screen shots of your data entry, validation and queries, and paste them into PPT slides.  In this way, your presentation will be smoother, you won't rely upon scrolling through results or navigating through your application during your presentation.  In addition, you won't have any unpleasant surprises if your server goes down or any other unanticipated issues arise.

# Technical Requirements
Some of the technical specifications/components of the project:

- Include at least one structural change to the database using DDL.  (Create, Alter, Drop). Clearly, your application will be written on one version of the design.  So you may satisfy this requirement by discussing what changes in the business requirements might precipitate a change in the design, and how would you implement that?  An example would be:  the design is based on the reality that every employee is assigned to exactly one department.  But the company has changed its management structure to a more project-based structure, and now, employees can be assigned to multiple departments.  This necessitates a change in the cardinaly of department:employee from 1:n to m:n.  This now requires a new relationship entity.  Other examples might include changing the format of a zip code from XXXXX to XXXXX-xxxx.  

- Provide the DDL as well as the INSERT SQL for creating the tables and initially populating the database.  You may do this in any text editor and then paste into the SQL window of PHMyAdmin, or you may use the DDL from the terminal or from within a Python program, as demonstrated in class.

- Include at least one insertion of a new record that will occur during the execution of the application.  This will most likely be as the result of a transaction or some component that should be added to the database.  For instance, in our labs, we added a department, and we also added an employee-project assignment.  Both of these required the insertion of a new record in the database.  In regular SQL, this would use the INSERT statement.  However, you should use Flask-SQLAlchemy for this purpose.

- Include at least one update of a record--changing an existing record, not adding a new one.  Use SQLAlchemy.

- Include at least one delete of a record.  Use SQLAlchemy.

- Include at least one simple SELECT SQL statement.  Use regular SQL for this.  This will require a database connection using one of packages that were showed in Lab-4-connect.

- Include one query using Flask-SQLAlchemy filter or filter_by.

- Inlcude at least one SELECT using an aggregate function.  Use regualr SQL for this.
  **Within the myPatients route, we select a count of the patients for the logged in provider.**
  `cur.execute("SELECT DISTINCT COUNT(patientID) FROM patient WHERE patientPCP = '%d'" % providerID)`

- Include at least one SELECT using a compound condition using regular SQL, and also the equivalent of a compound condition select using Flask-SQLAlchemy.

- Include at least one JOIN query using SQL, and also one using Flask-SQLAlchemy.

- Include at least one subquery.  Regular SQL.  Excellence points if you also use Flask-SQLAlchemy.

- Use a form to collect user data, as shown in our CRUD labs.

- Populate a field on a form or table from the database.  This would most likely be for your update, and you can model this directly off of our examples in class.

- Check for empty data fields. You can use the built-in validations for this.

- Implement referential intergrity.  Demonstrate what happens when it is violated. Or, if you constructed your program so that it can't be violated, demonstrate how it references a primary key and prevents a vioaltion of referential intergrity.  For example, if employee has a foreign key deptNo that references the primary key deptNo in the relation Department.  If you populate a drop-down box with existing department numbers, this will prevent the user from entering an invalid department number, thereby enforcing referential integrity.  We did something similar in Lab-4-c.  If you just have a text box, the user can enter a department number that doesn't exist, and you can demonstrate that this will cause a referential integrity error.  Either method is fine, but be clear on what you are trying to achieve and demonstrate.

- Use an appropriate structure for your project package.  Any of the structures that we used in class is fine.  I would recommend using the structure that we used for Lab-4-c, as that is a good starting point for the project.

---

# Goals for E.C.

- Using additional flask or flask-sqlalchemy features that we did not cover in class.

- Using additonal WTForms components that we did not cover in class. (Examples:  importing other html form components that we did not demonstrate in class; check boxes, radio buttons, etc. multiple drop-down boxes)

- A correlated subquery.

- A Flask-SQLAlchemy subquery.

- An especially complex query.

- An especially complex ERD.

- Additions to your html that add to the functionality, navigability or appeal of your website.  This includes bootstrap that we didn't use in class.

- Javascript, JQuery, other client-side programming
