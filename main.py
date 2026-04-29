"""FastAPI application entrypoint."""

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from api.routes import router as portfolio_router
from api.auth_routes import router as auth_router

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="ARAIA Portfolio Input API")


@app.get("/")
def root():
    """Health check for the root path."""
    return {"status": "ok", "message": "ARAIA Portfolio API is running. Access frontend at /index.html if not automatically redirected."}


@app.get("/api")
@app.get("/api/health")
def api_root() -> dict[str, str]:
    """Simple health response for the API base path."""
    return {"status": "ok", "message": "ARAIA Portfolio Input API is running"}

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(portfolio_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
