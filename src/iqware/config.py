import os
from pathlib import Path

import dotenv

# ===========================
#      API CONFIGURATION
# ===========================

dotenv.load_dotenv()

MAIN_DIR = Path(__file__).resolve().parent

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM") or "HS256"
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

DATABASE_URL = os.getenv("DATABASE_URL") or f"sqlite:///{MAIN_DIR}/db.sqlite3"

CORS_DOMAINS = ["localhost"]


if not JWT_SECRET_KEY:
    raise RuntimeError("The JWT Secret key was not set.")
