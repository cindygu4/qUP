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
  * Contains the JavaScript needed for students to click on the stars to give a rating and for students to submit the 
  feedback form 
* `notifications.js`
  * Contains the JavaScript needed for infinite scrolling of a student's notifications
* `styles.css`
  * Contains all of the CSS needed for the buttons, navbar and body color, etc. 
  
#### Templates Folder
* `classes.html`
  * Contains page for showing students all of the classes they are in
* `give_feedback.html`
  * Allows students to give feedback to the instructor using a form to rate them from 1-5 and also provide them with 
  any additional comments
* `index.html`
  * Contains the student dashboard
  * When there are ongoing office hours, they will show up on the left hand side of the screen (if on a large/medium 
  screen)
  * When office hours are done and the student attended that office hours, those office hours will show up in the 
  list on the right (for medium/larger screens)
    * If the student received help from the instructor during those office hours, a give feedback button will show up, 
    allowing students to be redirected to a form that they can fill out
    * Only shows the office hours attended in the past 7 days 
* `join_class.html`
  * Allows students to input a 7-character code given to them by their instructor and join that class
* `layout.html`
  * Contains the navbar and the layout that other HTML pages follow
* `notifications.html`
  * Displays all the notifications that a student received, uses JavaScript to achieve infinite scrolling
* `opened_queue.html`
  * Contains the page that a student sees when an instructor opens a queue
  * Students can join the queue by filling out a form with additional information
    * Once a student fills out the form and clicks "Join Queue," they will see a disabled button and will not be allowed 
    to join the queue again until they are removed from the queue or helped by the instructor
  * Students can also see how many other people are in the queue
* `upcoming_oh.html`
  * Displays all of a student's upcoming office hours
  
#### Python Files
* `forms.py`
  * Contains the forms needed for a student to join a class and to join an opened queue
* `models.py`
  * Contains the `Notification`, `OfficeHoursLine`, and `Feedback` models
    * `OfficeHoursLine` helps to handle the queue for a given office hours
* `urls.py`
  * Contains all of the URLs a student needs to navigate around the website
* `views.py`
  * Handles all of the student's requests
  * Includes APIs for loading notifications and POSTing a feedback form

Teachers App
----
The teachers app contains all the files needed for the teacher side

#### Static Folder
* `classes.js`
  * Allows instructors to edit the names of their classes without having to reload the page
* `styles.css`
  * Contains all of the CSS styling needed for the buttons, navbar color, body color, etc.
  
#### Templates Folder
* `add_class.html`
  * Allows instructor to create a new class
* `add_queue.html`
  * Allows instructor to fill out a form to create new office hours
* `classes.html`
  * Allows instructor to view all of their classes
  * Shows their classes' class codes
  * Allows them to edit the names of the classes without reloading the page (`classes.js`) 
* `classroom.html`
  * Allows instructor to view all of their office hours
  * Instructors can create new office hours, open/join an office hours, view feedback from past office hours, and delete
  office hours from this page
* `edit_queue.html`
  * Allows instructor to edit their office hours, fills the form with the existing office hours' information
* `feedback.html`
  * Instructors can view their avg rating for an office hours and all of the comments that students have made regarding 
  their help during office hours
  * Instructors can also see the number of students who responded
  * All feedback ratings and comments are anonymous
* `index.html`
  * Contains the instructor dashboard
  * When there are ongoing office hours, they will show up on the left hand side of the screen (if on a large/medium 
  screen)
  * When office hours have ended, those office hours will show up in the list on the right (for medium/larger screens), 
  with buttons allowing instructors to view feedback for those office hours
    * Only shows the office hours from the past 7 days
* `layout.html`
  * Contains the instructor navbar and any additional layout needed for other pages
* `opened_oh.html`
  * Contains the page that an instructor sees when a queue is opened
  * Shows how many students in the queue
  * Only shows the "Finished Helping" button for the first student in the queue
  * Allows instructors to end office hours early with a button
* `upcoming_ohs.html`
  * Shows the instructor all of their upcoming office hours

#### Python Files
* `forms.py`
  * Contains the forms needed for instructors to create classes and office hours
  * Includes date validation function used when creating office hours 
* `models.py`
  * Contains the `Classroom` and `Queue` models
* `urls.py`
  * Contains all of the URLs need for an instructor to navigate around the web app
* `views.py`
  * Handles all of the instructor's requests
  * Includes API for renaming a class

Requirements
---
* `psycopg2-binary`
* `django-crispy-forms`

Additional Info
---
* Time Zone for this project is `America/New_York`