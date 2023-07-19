# Food Recommendation Application Backend

Backend server that provides REST API endpoints for a food recommendation system service.

## Setup
`pipenv` is used as the virtual environment manager. For installation see https://pypi.org/project/pipenv/.
To initialize the project run:
```
pipenv install --dev
```

## Running
`uvicorn` is used as the asynchronous AGSI web server provider. To start the server run:
```
pipenv shell
uvicorn server.app:app --reload
```

## Structure
The project follows a simple hexagonal based architecture. This book https://www.amazon.ca/Microservice-APIs-Jose-Haro-Peralta/dp/1617298417 and codebase https://github.com/abunuwas/microservice-apis/tree/master are used as strong reference/guides.
- `server/web_api` contains the actual backend server and REST API end points logic.
- `server/repository` contains the data layer logic to provide an interface and handle communication with the external database.
- `server/service` contains the "business logic" types and functionalities. It provides an interface to be called by the `web_api` and makes calls to the `repository` interface.

## Database Migration
'alembic' is used as the data migration tool. In general, after updating the database models, you can run:
```
alembic revision --autogenerate -m "your_revision_messsage"
alembic upgrade heads
```
Note that `PYTHONPATH` needs to be set to the current working directory so that all new database models can be detected

## Used Libraries
- `fastapi` - Web API framework
- `pydantic` - Data parsing and validation
- `sqlalchemy` - Relational SQL ORM
- `alembic` - Database migration tool
