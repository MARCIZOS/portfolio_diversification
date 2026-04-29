import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Set yfinance cache directory to /tmp on Vercel
if os.getenv("VERCEL"):
    os.environ["YFINANCE_CACHE_DIR"] = "/tmp/.yfinance"

# Add project root to path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Initialize FastAPI app
app = FastAPI(title="ARAIA Portfolio API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check routes
@app.get("/api/health")
@app.get("/api")
def health_check():
    return {
        "status": "ok", 
        "message": "ARAIA Portfolio Backend is running",
        "environment": "vercel" if os.getenv("VERCEL") else "local"
    }

# Import and include routers inside the app to avoid circular imports
try:
    from api.routes import router as portfolio_router
    from api.auth_routes import router as auth_router
    
    app.include_router(auth_router, prefix="/api")
    app.include_router(portfolio_router, prefix="/api")
except ImportError as e:
    print(f"Router import error: {e}")

# Vercel needs 'app' to be available
handler = app

