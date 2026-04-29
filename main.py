"""Local entrypoint for the FastAPI application."""

import os
import uvicorn
from api.index import app

if __name__ == "__main__":
    # In development, we run the app directly
    uvicorn.run(app, host="0.0.0.0", port=8000)
