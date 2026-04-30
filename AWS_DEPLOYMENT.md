# AWS Deployment Guide (App Runner / ECS)

This project is now configured for a unified deployment using Docker, which is ideal for AWS App Runner or AWS ECS.

## Deployment Strategy: Dockerized Full-Stack
The application is containerized such that:
1. **Frontend**: React is built and served as static files by FastAPI.
2. **Backend**: FastAPI handles API requests under `/api` and serves the UI under `/`.
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

## Deploying to AWS App Runner (Recommended)
AWS App Runner is the easiest way to deploy this container.

1. **Push to ECR (Elastic Container Registry)**:
   ```bash
   # Create a repository
   aws ecr create-repository --repository-name portfolio-diversifier

   # Login to ECR
   aws ecr get-login-password --region your-region | docker login --username AWS --password-stdin your-account-id.dkr.ecr.your-region.amazonaws.com

   # Tag and Push
   docker tag portfolio-diversifier:latest your-account-id.dkr.ecr.your-region.amazonaws.com/portfolio-diversifier:latest
   docker push your-account-id.dkr.ecr.your-region.amazonaws.com/portfolio-diversifier:latest
   ```

2. **Create App Runner Service**:
   - Go to AWS Console -> App Runner -> Create service.
   - Source: Container registry (ECR).
   - Select your image.
   - **Service settings**: Port 8000.
   - **Environment Variables**: Add `GROQ_API_KEY`, `SECRET_KEY`, etc.

## Deploying to AWS ECS (Fargate)
For more control, use ECS with Fargate:
1. Create a Cluster.
2. Create a Task Definition (using the ECR image, port 8000).
3. Create a Service to run the task.

## Important Notes
- **Storage**: The current user database (`.users_db.json`) is stored inside the container's ephemeral storage. For production, you should connect to a persistent database like **AWS RDS (Postgres)** or **DynamoDB**.
- **Security**: Ensure your `SECRET_KEY` is kept private and provided via environment variables.
