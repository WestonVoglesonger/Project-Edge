from pathlib import Path
import logging
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import FileResponse
from backend.api import comment, discussion, project, static_files, join_request, user, auth
from backend.logging_config import configure_logging

# Configuration and Metadata
description = """
Welcome to the Project Edge RESTful Application Programming Interface.
"""

app = FastAPI(
    title="Edge Carolina API",
    version="0.0.1",
    description=description,
    openapi_tags=[
        user.openapi_tags,
        auth.openapi_tags,
        project.openapi_tags,
        discussion.openapi_tags,
        comment.openapi_tags,
        join_request.openapi_tags,
    ],
    openapi={
        "components": {
            "securitySchemes": {
                "OAuth2PasswordBearer": {
                    "type": "oauth2",
                    "flows": {
                        "password": {
                            "tokenUrl": "/api/auth/token",
                            "scopes": {
                                "read": "Read access",
                                "write": "Write access"
                            }
                        }
                    }
                }
            }
        },
        "security": [
            {
                "OAuth2PasswordBearer": ["read", "write"]
            }
        ]
    }
)

# Use GZip middleware for compressing HTML responses over the network
app.add_middleware(GZipMiddleware)

# Configure logging
configure_logging()

# Include all routers
feature_apis = [user, auth, project, discussion, comment, join_request]
for feature_api in feature_apis:
    app.include_router(feature_api.api)

# Mount static files middleware for serving Angular front-end
app.mount("/", static_files.StaticFileMiddleware(directory=Path("./static")))

# Serve the Angular index.html for all non-API routes
@app.get("/{full_path:path}", include_in_schema=False)
async def serve_spa(full_path: str):
    index_path = Path("./dist/project-edge/index.html")
    if index_path.exists():
        return FileResponse(index_path)
    return {"detail": "Not Found"}
