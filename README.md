<b>Task Management API</b><br><br>
This Project provides endpoints for managing tasks, assigning them to users, and retrieving task details. It includes
functionalities for listing tasks, creating tasks (admin only), updating tasks details(by admin only), assigning tasks
to users, and fetching tasks assigned to a specific user.

<b>Tech Stack:</b>

1. Python
2. Django Rest Framework (DRF)
3. Sqlite

<b>API Endpoints</b>

1. List All Tasks <br>
   Retrieves all tasks ordered by weightage in descending order and then by creation date.
   GET http://127.0.0.1:8000/tasks/list <br>
   [
   {
   "id": 3,
   "name": "Report dashboard Bug",
   "description": "You have to make report dashboard for easy data visibility.",
   "created_at": "2025-03-25T11:11:42.038806Z",
   "updated_at": "2025-03-25T11:11:42.038827Z",
   "task_type": "feature",
   "status": "pending",
   "created_by": 1
   }, <br>
   {
   "id": 2,
   "name": "Newsfeed Bug",
   "description": "Newsfeed is not visible when applying filters for a corporate.",
   "created_at": "2025-03-25T07:39:25.328721Z",
   "updated_at": "2025-03-25T08:38:33.462524Z",
   "task_type": "bug",
   "status": "pending",
   "created_by": 1
   }
   ]

2. Create a New Task (Admin Only) <br>
   POST  http://127.0.0.1:8000/tasks/create/ <br>
   Only users with an admin role (role = 0) can create tasks.

   Request Body: <br> {
   "user_id":1,
   "name":"Report dashboard Bug",
   "task_type":"feature",
   "description":"You have to make report dashboard for easy data visibility."
   } <br><br>
   Response:<br>
   {
   "id": 3,
   "name": "Report dashboard Bug",
   "description": "You have to make report dashboard for easy data visibility.",
   "created_at": "2025-03-25T11:11:42.038806Z",
   "updated_at": "2025-03-25T11:11:42.038827Z",
   "task_type": "feature",
   "status": "pending",
   "created_by": 1
   }

3. Get Users (Only users with role=1 will be fetched)<br>
   GET http://127.0.0.1:8000/users/list <br>
   Retrieves users who are not admins<br>
   Response: <br>
   [
   {
   "id": 2,
   "role_name": "normal_user",
   "name": "John Hill",
   "email": "john@yopmail.com",
   "username": "john_12",
   "mobile": "9876543210",
   "created_at": "2025-03-25T07:14:14.006287Z",
   "updated_at": "2025-03-25T07:14:14.006317Z"
   }, <br>
   {
   "id": 3,
   "role_name": "normal_user",
   "name": "James Bond",
   "email": "james@yopmail.com",
   "username": "james_13",
   "mobile": "8765432109",
   "created_at": "2025-03-25T07:14:14.017940Z",
   "updated_at": "2025-03-25T07:14:14.017958Z"
   },

4. Get Tasks Assigned to a User (tasks will be sorted by weightage) <br>
   GET http://127.0.0.1:8000/tasks/user/2 <br>
   Retrieves all tasks assigned to a user, sorted by weightage in descending order.<br>
   Response: <br>
   [
   {
   "task_id": 2,
   "name": "Newsfeed Bug",
   "description": "Newsfeed is not visible when applying filters for a corporate.",
   "task_type": "bug",
   "weightage": 5,
   "deadline": "2025-04-21"
   }, <br>
   {
   "task_id": 1,
   "name": "Dropdown menu",
   "description": "You have to build the backend for Dropdown menu for a corporate.",
   "task_type": "feature",
   "weightage": 1,
   "deadline": "2025-03-28"
   }
   ]
   <br>
5. Assign Tasks to Users (Task can be assigned to multiple users or a single user can be assigned multiple tasks) <br>
   POST http://127.0.0.1:8000/tasks/assign/<br>
   In list format, these are ids of user_id and task_id <br>
   Request Body: <br>
   {"task_ids":[1,2],
   "user_ids":[2],
   "weightage":{"2": 5},
   "deadline":{"1":"2025-03-28","2":"2025-04-21"}
   }
   Response: <br>
   {
   "message": "Successfully assigned 2 task(s) to 1 user(s)."
   }
   <br><br>

<b>Steps to Run the Project</b>

1. Extract the ZIP File
2. Navigate to the extracted folder:
3. Set Up a Virtual Environment and activate venv:
   python -m venv venv
   venv\Scripts\activate  or source venv/bin/activate
4. Install Dependencies
   pip install -r requirements.txt
5. If you found error of "No module storages"
   pip install django-storages
6. Set Up the Database
   python manage.py migrate
7. Create a Superuser (Optional for Admin Access)
   python manage.py createsuperuser
8. Run the Development Server
   python manage.py runserver
   The application will be available at:  http://127.0.0.1:8000/
9. Test the API Endpoints
   Use Postman, cURL, or any REST client to test the API endpoints.

<b>Future Enhancements</b>

1. Admin Can Add Attachments: While creating or updating tasks, admins can attach files (e.g., PDFs, images).

2. Users Can Submit Tasks: Users will have the ability to mark tasks as "Submitted" and attach evidence (e.g., reports).

3. Task Completion Workflow: Admins will be able to review submitted tasks and mark them as "Approved" or "Rejected."

4. Task Comments & Feedback: Users and admins can comment on tasks, providing feedback or clarifications.

5. Email Notifications: Notify users when a new task is assigned or when an update is made.

6. Task Assignment History: Keep a log of all task assignments and updates for tracking.
