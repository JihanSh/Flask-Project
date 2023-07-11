# Flask-Project


# Task Management API

This is a Flask-based API for managing tasks. It uses SQLAlchemy and psycopg2 to interact with a PostgreSQL database. You can use Postman to test the API endpoints.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Jihansh/task-management-api.git
Navigate to the project directory:
bash
Copy code
cd task-management-api
(Optional) Create a virtual environment:
bash
Copy code
python3 -m venv venv
Activate the virtual environment:
macOS/Linux:
bash
Copy code
source venv/bin/activate
Windows (PowerShell):
bash
Copy code
venv\Scripts\Activate
Install the required packages:
bash
Copy code
pip install Flask SQLAlchemy psycopg2
Database Setup
Install PostgreSQL on your machine if you haven't already. You can download it from the official website: https://www.postgresql.org/download/

Create a PostgreSQL database for the application.

Update the database configuration in the app.py file:

python
Copy code
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/database_name'
Replace username, password, and database_name with your own database credentials.

Create a table called "tasks" in the database with the following columns:
id (serial primary key)
title (text)
description (text)
completed (boolean)
API Endpoints
GET /tasks: Retrieve all tasks from the database and return them as JSON.
POST /tasks: Create a new task and store it in the database.
GET /tasks/{task_id}: Retrieve a specific task and return its details as JSON.
PUT /tasks/{task_id}: Update the details of a specific task.
DELETE /tasks/{task_id}: Delete a specific task.
Usage
Start the Flask development server:
bash
Copy code
python app.py
Open Postman or any similar tool to test the API endpoints.

Send appropriate requests (GET, POST, PUT, DELETE) to the corresponding endpoints (e.g., http://localhost:5000/tasks) and verify the responses.

Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
