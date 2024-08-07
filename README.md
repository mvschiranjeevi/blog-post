# Flask Blog Post API

## Overview

This is a RESTful API built using Python Flask for managing blog posts. It includes features for creating, retrieving, updating, and deleting blog posts. The API also implements JWT-based authentication to secure these operations. SQLAlchemy is used for in-memory database management.

## Features

- **JWT Authentication**: Users can sign up, sign in, and authenticate their requests.
- **CRUD Operations for Blog Posts**:
  - Create a new blog post
  - Retrieve a list of all blog posts
  - Retrieve a single blog post by its ID
  - Update an existing blog post
  - Delete a blog post

## Technologies Used

- **Python Flask**: Web framework for building the API.
- **SQLAlchemy**: ORM for database management.
- **JWT**: Authentication mechanism.
- **pylint**: Linting libraryfor better readabilty.
- **unittest**: API testing library Unit testing.
- **Swagger**: Tool for API Documentation.

## Project Structure

```bash
├── instance/
├── src/
│ ├── ...
│ ├── config # Config files for the application
│ ├── constants # HTTP constant codes for the application
│ ├── docs # Swagger file docs
│ ├── init.py # entry file
│ ├── auth.py # Auth end points
│ ├── posts.py # blog post end points
│ └── database.py # database structure
├── test/
│ ├── ...
│ ├── init.py # entry file
│ ├── test_auth.py # unit cases for auth end points
│ └── test_posts.py # unit test cases for blog post end points
├── requirements.txt # Requirements file
└── ...
```

## Setup and Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/mvschiranjeevi/blog-post
   cd blog-post
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install the dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables for mac**:
   Create a `.flaskenv` file and add the following variables:
   ```flaskenv
   export FLASK_APP=src
   export FLASK_RUN_PORT=8000
   export FLASK_ENV=development
   export FLASK_DEBUG=1
   export SQLALCHEMY_DB_URI = sqlite:///posts.db
   export JWT_SECRET_KEY = your_secret_key
   ```
   Create a `.env` file and add the following variables:
   ```env
   export SECRET_KEY=your_secret_key
   ```

## Running the Application

To run the application, use the following command:

```bash
flask run
```

## Testing the Application

```bash
python -m unittest discover -s tests
```

This `README.md` provides an overview of your Flask project, setup instructions, details about the API endpoints, and how to run tests.
