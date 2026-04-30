# AWS Deployment Guide (App Runner / ECS)

This project is configured for a unified deployment using Docker, which is the recommended way to deploy full-stack applications on AWS.

## Deployment Strategy: Dockerized Full-Stack
The application is containerized such that:
1. **Frontend**: React is built and served as static files by the FastAPI backend.
2. **Backend**: FastAPI handles API requests under `/api` and serves the React UI under `/`.
3. **Container**: Everything runs in a single Docker container on port 8000.

## Prerequisites
1. **AWS Account**
2. **Docker Installed** (for local testing)
3. **AWS CLI** configured

## Local Testing with Docker
```bash
# Build the image
docker build -t portfolio-diversifier .

# Run the container
docker run -p 8000:8000 -e GROQ_API_KEY=your_key portfolio-diversifier
```
Access the app at `http://localhost:8000`

## Deploying to AWS App Runner (Easiest)
AWS App Runner is a fully managed service that makes it easy to deploy containerized web applications.

1. **Create an ECR Repository**:
   - Go to AWS Console -> Elastic Container Registry -> Create repository.
   - Name it `portfolio-diversifier`.

2. **Push your Image to ECR**:
   Click "View push commands" in your ECR repository and follow the steps:
   - Authenticate your Docker client.
   - Build your Docker image.
   - Tag the image.
   - Push the image to ECR.

3. **Create App Runner Service**:
   - Go to AWS Console -> App Runner -> Create service.
   - **Source**: Container registry -> Amazon ECR.
   - **Container image URI**: Select your pushed image.
   - **Deployment settings**: Automatic (whenever you push a new image).
   - **Service settings**:
     - **Port**: 8000.
     - **Environment Variables**: Add `GROQ_API_KEY`, `SECRET_KEY`, etc.
   - Review and Create.

## Deploying to AWS ECS (Fargate)
For more advanced scaling and networking:
1. Create an ECS Cluster.
2. Create a Task Definition (Container: your ECR image, Port: 8000).
3. Create a Service to run the task in your cluster.

## Important Production Notes
- **Persistence**: The current user database (`.users_db.json`) is stored inside the container. Since containers are ephemeral, your data will be lost on restart. For production, you should update `auth_service.py` to use **AWS RDS (Postgres)** or **DynamoDB**.
- **Security**: Always use environment variables for sensitive keys (`GROQ_API_KEY`, `SECRET_KEY`).
