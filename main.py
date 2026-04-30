import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.routes import router as portfolio_router
from api.auth_routes import router as auth_router

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

# Include API routers
app.include_router(auth_router, prefix="/api")
app.include_router(portfolio_router, prefix="/api")

# Health check routes
@app.get("/api/health")
@app.get("/api")
def health_check():
    return {
        "status": "ok", 
        "message": "ARAIA Portfolio Backend is running",
        "environment": "production" if os.getenv("DOCKER_ENV") else "development"
    }

# Static file serving (Serve React frontend)
# This assumes the frontend build is in the 'static' directory
if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
