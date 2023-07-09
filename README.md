# Food Recommendation Application Backend

Backend server that provides REST API endpoints for a food recommendation system service.

## Setup
`pipenv` is used as the virtual environment manager. For installation see https://pypi.org/project/pipenv/.
To install run:
```
pipenv install --dev
```

## Running
`uvicorn` is used as the asynchronous AGSI web server provider. To start the server run:
```
pipenv shell
uvicorn server.app:app --reload     
```
