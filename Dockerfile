# Front-end Build Steps
FROM node:18 as build
WORKDIR /workspace/frontend
COPY ./frontend/package.json ./frontend/angular.json /workspace/frontend/
RUN npm install && npm install -g @angular/cli
ENV SHELL=/bin/bash
RUN ng analytics disable
COPY ./frontend/src /workspace/frontend/src
COPY ./frontend/*.json /workspace/frontend/
RUN ng build --output-path /workspace/static

# Back-end Build Steps
FROM python:3.11-slim-buster
WORKDIR /app
COPY ./backend/requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY ./backend/ /app/
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "1380"]
EXPOSE 1380