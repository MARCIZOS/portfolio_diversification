# Vercel Deployment Guide

## Project Structure Overview
This is a full-stack application with:
- **Backend**: FastAPI (Python) deployed as serverless functions
- **Frontend**: React + Vite deployed as static site
- **API Routes**: All backend endpoints accessible via `/api/*`

## Prerequisites
1. **Vercel Account**: Sign up at https://vercel.com
2. **GitHub Repository**: Push your code to GitHub (Vercel integrates with GitHub)
3. **Environment Variables**: Set up any required `.env` variables

## Deployment Steps

### 1. Push Code to GitHub
```bash
git add .
git commit -m "Setup Vercel deployment configuration"
git push origin main
```

### 2. Connect to Vercel
1. Go to https://vercel.com/new
2. Select "Import Git Repository"
3. Authorize and select your GitHub repository
4. Choose **"Other"** as the framework (or skip framework detection)

### 3. Configure Build Settings
When prompted for build settings:

- **Build Command**: `cd frontend && npm install && npm run build`
- **Output Directory**: `frontend/dist`
- **Install Command**: (Leave default)

The `vercel.json` file will handle the rest of the configuration.

### 4. Environment Variables
Set environment variables in Vercel project settings:
- Go to **Settings > Environment Variables**
- Add any required variables from your `.env` file (e.g., `OPENAI_API_KEY`, database URLs)

### 5. Deploy
Click "Deploy" and wait for the build to complete.

## Important Notes

### API Endpoints
- In **production** (Vercel): All API calls use relative `/api/*` paths (same domain)
- In **development** (local): API calls go to `http://localhost:8000`

The frontend automatically detects the environment and routes accordingly.

### Python Limitations on Vercel
Vercel's Python support has some considerations:
- **Cold starts**: Serverless functions may have startup delay on first request
- **Memory limits**: Keep response sizes reasonable
- **Execution time**: Functions have execution time limits
- **Dependencies**: Only use packages available on Vercel's Python runtime

If you experience issues:
1. Check Vercel deployment logs for errors
2. Ensure all Python dependencies are in `requirements.txt`
3. Consider using alternative backends (Railway, Render) for persistent services

### Local Development
```bash
# Terminal 1: Start backend
cd portfolio_diversification-main
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start frontend
cd portfolio_diversification-main/frontend
npm run dev
```

Access frontend at `http://localhost:5174` (or displayed port)

## File Changes Made for Deployment

1. **`requirements.txt`**: Python dependencies
2. **`vercel.json`**: Vercel configuration with rewrite rules
3. **`api/index.py`**: Serverless handler for FastAPI
4. **`frontend/vite.config.js`**: Added dev proxy for `/api/*`
5. **`frontend/src/services/api.js`**: Smart API URL detection
6. **`.vercelignore`**: Files to exclude from deployment

## Troubleshooting

### Build Fails
- Check that all dependencies are in `requirements.txt`
- Verify frontend build works locally: `npm run build`
- Check Vercel logs for specific error messages

### API Returns 404
- Ensure `vercel.json` is in the root directory
- Check that API routes are correctly defined in `main.py` and routers

### CORS Issues
- CORS is already configured to allow all origins in `main.py`
- In production, you may want to restrict to your domain

### Environment Variables Not Loading
- Verify variables are set in Vercel project settings
- Ensure `python-dotenv` is in `requirements.txt` (already included)

## Next Steps

After successful deployment:
1. Test all API endpoints from the deployed frontend
2. Monitor Vercel analytics and logs
3. Set up domain (optional) in Vercel settings
4. Consider enabling auto-deployments on main branch commits

## Support
For Vercel-specific issues: https://vercel.com/docs
For FastAPI questions: https://fastapi.tiangolo.com
