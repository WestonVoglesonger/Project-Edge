# Front-end Build Steps
FROM node:18 as build

# Set environment variable to increase memory limit
ENV NODE_OPTIONS=--max-old-space-size=4096

COPY ./frontend/package.json /workspace/frontend/package.json
COPY ./frontend/angular.json /workspace/frontend/angular.json
WORKDIR /workspace/frontend
RUN npm install -g @angular/cli && npm install
ENV SHELL=/bin/bash
RUN ng analytics disable
COPY ./frontend/src /workspace/frontend/src
COPY ./frontend/*.json /workspace/frontend
RUN ng build --optimization --output-path ../static

# Back-end Build Steps
FROM python:3.11-slim-buster
WORKDIR /app

# Ensure the requirements.txt file is copied to the correct location
COPY ./backend/requirements.txt /workspace/backend/requirements.txt

# Install PostgreSQL development package
RUN apt-get update && \
    apt-get install -y libpq-dev

RUN pip install --upgrade pip && \
    pip install -r /workspace/backend/requirements.txt

# Copy the rest of the backend code
COPY ./backend/ /app

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "1380"]

EXPOSE 1380