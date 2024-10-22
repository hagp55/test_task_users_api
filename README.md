# Users API

Users API is a simple user management API built using FastAPI.
It provides basic CRUD (Create, Read, Update, Delete) operations for users.

## Tech Stack
- Python
- FastAPI
- Pytest
- Postgresql
- Docker
- Docker-Compose

## Features
- CRUD operations for users (Create, Read, Update, Delete).
- Info endpoint
  - Function that counts the number of users registered in the last 7 days.
  - Function that returns the top 5 users with the longest names.
  - Function that determines what proportion of users have an email address registered in a particular domain
- Simple and straightforward project structure.

## Installation
### Clone the project
```bash
   git clone https://github.com/hagp55/test_task_users_api
```
### Go to the project directory
```bash
  cd my-project
```
### Config .env variables
Use the `.env.example` as reference to create your configuration file `.env`

### Use Poetry to install project dependencies:

```bash
poetry install
```

### Run in Docker
```bash
docker compose up

```
### Running Tests
To run tests, run the following command
```bash
poetry run pytest -v
```
## API Endpoints

#### list routes of UsersAPI, and what are their expected request.
| Route                               | Description
|-------------------------------------|-------------------------------------------
| `GET` /api/v1/users/statistics/     | get user statistics, optional <domain>
| `GET` /api/v1/users/                | get all users, optional <page, size>
| `POST` /api/v1/users/               | create user
| `GET` /api/v1/users/{user_id}/      | get a specific user
| `PUT` /api/v1/users/{user_id}/      | update a specific user
| `DELETE` /api/v1/users/{user_id}/   | delete a specific user


## Testing the API with Swagger UI

Fast API comes with Swagger UI. This tool is automatically generated based on your API's route definitions and Pydantic models.

### Accessing Swagger UI

Once the API is running, Swagger UI can be accessed on the following URL:

```bash
http://127.0.0.1:8000/docs
```

You can use swagger UI to:

1. **Browse Endpoints**
2. **Send Requests**
3. **View Responses**
4. **Test Validations**

## To Test with SwaggerUI, you can do the following for each endpoint explained above

1. Open your web browser and navigate to the /docs path as mentioned above.

2. Explore the available endpoints and select the one you want to test.

3. Click on the "Try it out" button to open an interactive form where you can input data.

4. Fill in the required parameters and request body (if applicable) according to the API documentation given above.

5. Click the "Execute" button to send the request to the API.

6. The response will be displayed below, showing the status code and response data.

7. You can also view example request and response payloads, which can be helpful for understanding the expected data format.
