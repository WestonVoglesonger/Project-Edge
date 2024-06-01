# Front-end Build Steps
FROM node:18 as build

# Set environment variable to increase memory limit
ENV NODE_OPTIONS=--max-old-space-size=4096

# Set working directory
WORKDIR /workspace/frontend

# Copy package files
COPY ./frontend/package.json ./frontend/angular.json ./

# Install dependencies and Angular CLI
RUN npm install -g @angular/cli && npm install

# Disable Angular analytics
RUN ng analytics disable

# Copy source files
COPY ./frontend/src ./src
COPY ./frontend/*.json ./

# Build the Angular project
RUN ng build --optimization --output-path ../static

# Back-end Build Steps
FROM python:3.11-slim-buster

# Set working directory
WORKDIR /workspace/backend

# Ensure the requirements.txt file is copied to the correct location
COPY ./backend/requirements.txt /workspace/backend/requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r /workspace/backend/requirements.txt

# Copy the rest of the backend code
COPY ./backend/ /workspace/backend

# Copy the built static files from the frontend build stage
COPY --from=build /workspace/static /workspace/static

# Set PYTHONPATH environment variable
ENV PYTHONPATH=/workspace/backend

# Set the entrypoint for the backend service
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "1380"]

# Expose the port for the backend service
EXPOSE 1380
