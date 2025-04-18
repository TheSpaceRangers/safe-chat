from dotenv import load_dotenv

from fastapi import FastAPI

from routes.v1 import api_v1
from storage import load_optional_rules

load_dotenv()

load_optional_rules()

api = FastAPI()

api.include_router(api_v1)