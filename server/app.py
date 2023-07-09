from fastapi import FastAPI

app = FastAPI(debug=True)

from server.api import api
