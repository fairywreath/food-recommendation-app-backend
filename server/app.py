from dotenv import load_dotenv

from fastapi import FastAPI


load_dotenv(override=True)

app = FastAPI(debug=True)


from server.web_api import api
