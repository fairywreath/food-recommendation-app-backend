from fastapi import FastAPI

app = FastAPI(debug=True)

from server.web_api import api
