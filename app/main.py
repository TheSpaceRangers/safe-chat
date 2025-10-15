from dotenv import load_dotenv

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from routes.v1 import api_v1
from storage import load_optional_rules

load_dotenv()

load_optional_rules()

api = FastAPI()

# CORS restreint: ajustez au domaine dhebergement si besoin
api.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["POST", "GET", "DELETE"],
    allow_headers=["content-type"],
)

@api.middleware("http")
async def security_headers_and_min_logs(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response

api.include_router(api_v1)