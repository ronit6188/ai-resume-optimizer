import os
import sys
from pathlib import Path

# Add the backend folder to the Python path so imports work
BASE_DIR = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(BASE_DIR))

from alembic.config import Config
from alembic import command

def main() -> None:
    alembic_cfg_path = BASE_DIR / "alembic.ini"
    if not alembic_cfg_path.is_file():
        raise FileNotFoundError(f"Missing alembic.ini at {alembic_cfg_path}")
    config = Config(str(alembic_cfg_path))
    # Ensure Alembic knows the absolute script location (backend/alembic)
    config.set_main_option('script_location', str(BASE_DIR / 'alembic'))
    command.upgrade(config, "head")
    print("✅ Migration completed successfully")

if __name__ == "__main__":
    main()
