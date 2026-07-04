# Flask Todo App 

A Flask-based Todo application with user authentication using JWT stored in cookies, SQLAlchemy for persistence, and basic CRUD functionality for todos.


## Features

User registration and login

JWT authentication using Flask-JWT-Extended

JWT stored securely in HTTP cookies

User-specific todo lists

Create, update, and delete todos

SQLite database using SQLAlchemy ORM

Server-side rendered templates (Jinja2)

## Creating a user
Before accessing the todo application, all users must log in.
If you don't have a user, you can just click register.

<p align="center">
  <img src="assets/login.png" height="50%" width="50%">
  <img src="assets/register.png" height="25%" width="25%">
</p>

After logging in, you will be met with a blank page containing only a header.

<p align="center">
  <img src="assets/home.png" width="500">
</p>

---

## Accessing the todos

If you click the button "Create todo" you will get to the todo creation page, which will pop up in your homepage until you delete them.

<p align="center">
  <img src="assets/create_todo.png" width="380">
  <img src="assets/todos.png" width="380">
</p>

## Tech Stack

Python 

Flask

Flask-SQLAlchemy

Flask-JWT-Extended

SQLite

Jinja2 templates

Docker 

## Running with Docker

### Clone the repository:

```bash
git clone https://github.com/jonasolivernicolaysen/todo_API.git
cd todo_API
```
### Build and start the application
```bash
docker compose up --build
```

Open your browser and navigate to http://localhost:5000



