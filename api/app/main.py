"""FastAPI app and AWS Lambda entry point."""

from fastapi import FastAPI
from mangum import Mangum

from app.api import router

app = FastAPI(title="Site chat API", docs_url=None, redoc_url=None, openapi_url=None)
app.include_router(router)

handler = Mangum(app, lifespan="off")
