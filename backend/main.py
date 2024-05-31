"""Entrypoint of backend API exposing the FastAPI `app` to be served by an application server such as uvicorn."""

from pathlib import Path
import logging
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from backend.api import project, static_files
from backend.api import user, auth
from backend.logging_config import configure_logging

__authors__ = ["Weston Voglesonger"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

description = """
Welcome to the Project Edge RESTful Application Programming Interface.
"""

# Configure logging
configure_logging()

# Metadata to improve the usefulness of OpenAPI Docs /docs API Explorer
app = FastAPI(
    title="Edge Carolina API",
    version="0.0.1",
    description=description,
    openapi_tags=[
        user.openapi_tags,
        auth.openapi_tags,
        project.openapi_tags,
    ],
)

# Use GZip middleware for compressing HTML responses over the network
app.add_middleware(GZipMiddleware)

# Plugging in each of the router APIs
feature_apis = [
    user,
    auth,
    project
]

for feature_api in feature_apis:
    app.include_router(feature_api.api)

# Static file mount used for serving Angular front-end in production, as well as static assets
app.mount("/static", static_files.StaticFileMiddleware(directory=Path("./static")), name="static")

# Example route to test logging
@app.get("/test-logging")
async def test_logging():
    logger = logging.getLogger(__name__)
    logger.info("This is an info log message")
    return {"message": "Check the logs for an info message"}