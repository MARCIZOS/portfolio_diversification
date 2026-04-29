import os
import sys

# Set yfinance cache directory to /tmp on Vercel
if os.getenv("VERCEL"):
    os.environ["YFINANCE_CACHE_DIR"] = "/tmp/.yfinance"

# Add project root to path so we can import from main and other modules
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Import the FastAPI app from main.py
try:
    from main import app
except ImportError as e:
    # Fallback for different Vercel directory structures
    print(f"Import error: {e}. Trying alternative path...")
    sys.path.append(os.path.join(root_dir, "api"))
    from main import app

# Vercel needs the app object to be available at the module level
# This is already handled by the import above

