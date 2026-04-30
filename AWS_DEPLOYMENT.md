# AWS Deployment Guide (S3 + CloudFront + EC2)

This guide explains how to deploy the portfolio diversifier project using a split architecture:
- **Frontend**: Hosted on **AWS S3** and distributed via **CloudFront**.
- **Backend**: Hosted on an **AWS EC2** instance.

## 1. Backend Deployment (EC2)

### Prerequisites
- An EC2 instance (Ubuntu 22.04 recommended).
- Security Group allowing inbound traffic on port 80 (HTTP), 443 (HTTPS), and 8000 (API).

### Steps
1. **Connect to your EC2**:
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```
2. **Install Dependencies**:
   ```bash
   sudo apt update && sudo apt install -y python3-pip python3-venv git
   ```
3. **Clone and Setup**:
   ```bash
   git clone https://github.com/your-repo/portfolio_diversify.git
   cd portfolio_diversify
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. **Environment Variables**:
   Create a `.env` file with your keys and the allowed origins:
   ```env
   GROQ_API_KEY=your_key
   ALLOWED_ORIGINS=https://your-cloudfront-domain.com
   ```
5. **Run with Gunicorn/Uvicorn**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000 --daemon
   ```

## 2. Frontend Deployment (S3 + CloudFront)

### Steps
1. **Configure API URL**:
   In your local `frontend/` directory, create/update `.env.production`:
   ```env
   VITE_API_URL=https://your-ec2-domain-or-ip/api
   ```
2. **Build the Frontend**:
   ```bash
   cd frontend
   npm install
   npm run build
   ```
3. **Upload to S3**:
   - Create an S3 bucket (e.g., `portfolio-frontend-static`).
   - Enable **Static Website Hosting**.
   - Upload all files from `frontend/dist/` to the root of the bucket.
4. **Configure CloudFront**:
   - Create a CloudFront Distribution.
   - **Origin**: Your S3 bucket website endpoint.
   - **Viewer Protocol Policy**: Redirect HTTP to HTTPS.
   - **Default Root Object**: `index.html`.
   - **Error Pages**: Add a custom error response for 403/404 to return `/index.html` with status 200 (for SPA routing).

## 3. Architecture Benefits
- **Cost**: S3 + CloudFront is extremely cheap for static hosting.
- **Performance**: CloudFront caches your frontend at edge locations globally.
- **Scalability**: Your EC2 only handles API logic and RAG processing.

## Important Notes
- **SSL**: Use AWS Certificate Manager (ACM) to get a free SSL certificate for your CloudFront distribution.
- **CORS**: Ensure `ALLOWED_ORIGINS` in your EC2 `.env` matches your CloudFront domain to prevent browser blocks.
