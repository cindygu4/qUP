# qUP
qUP is a web application where students can keep track of and be notified of all their office hours. Instructors can 
create office hours and open up queues that their students can join. Additionally, it allows students to rate the help 
given during a specific instructors' office hours, providing valuable feedback to 
the instructor. 

## Project Info
This project has 3 apps:
* `users`
* `students`
* `teachers`

Each of these apps can be found inside the `apps` folder. 

Additionally, this project is connected to a PostgresQL database. 

Users App
----
The users app handles all of the login and registration for both students and teachers.


#### Static Folder
* `styles.css`
  * Contains the CSS styling stuff for the login and register pages, including the background image and the custom buttons 

#### Templates Folder
* `index.html`
  * Contains the landing page with the login or sign up buttons
* `layout.html`
  * Contains the layout of the login and registration pages
* `login.html`
  * Handles the login for both students and instructors
* `register.html`
  * Handles the registration for both students and instructors
  
#### Python Files
* `forms.py`
  * Contains the student and instructor registration form
* `models.py`
  * Contains the `User`, `Teacher`, and `Student` models
* `urls.py`
  * Contains the urls for the login, registration, logout, and landing page
* `views.py`
  * Handles the login, registration, and logging out for students and instructors

Students App
----
The students app contains all the files needed for the student side.

#### Static Folder
* `feedback.js`
* `notifications.js`
* `styles.css`

Teachers App
----
The teachers app contains all the files needed for the teacher side

#### Static Folder
* `classes.js`
* `styles.css`