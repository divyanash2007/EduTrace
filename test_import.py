import sys
import os

# Emulate what alembic/env.py does
current_dir = os.getcwd()
sys.path.append(current_dir)

try:
    from app.core import config
    print("Successfully imported app.core.config")
    print(f"DB_URL: {config.DB_URL}")
except ImportError as e:
    print(f"ImportError: {e}")
    print(f"sys.path: {sys.path}")
except Exception as e:
    print(f"Error: {e}")
