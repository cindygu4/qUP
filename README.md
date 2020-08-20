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
  * When office hours have been ended and the student attended that office hours, those office hours will show up in the 
  list on the right (for medium/larger screens)
    * If the student received help from the instructor during those office hours, a give feedback button will show up, 
    allowing students to be redirected to a form that they can fill out 
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
* `styles.css`