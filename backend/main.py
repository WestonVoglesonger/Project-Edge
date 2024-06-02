from pathlib import Path
import logging
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware
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
app.mount("/", static_files.StaticFileMiddleware(directory=Path("./static")))

# Serve the Angular index.html for all non-API routes
@app.get("/{full_path:path}", include_in_schema=False)
async def serve_spa(full_path: str):
    index_path = Path("./dist/project-edge/index.html")
    if index_path.exists():
        return FileResponse(index_path)
    return {"detail": "Not Found"}

# Example route to test logging
@app.get("/test-logging")
async def test_logging():
    logger = logging.getLogger(__name__)
    logger.info("This is an info log message")
    return {"message": "Check the logs for an info message"}
