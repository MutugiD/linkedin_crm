#!/usr/bin/env python
"""
Diagnostic script for the LinkedIn CRM backend.
This script checks the system configuration, database connection,
and basic application functionality.
"""

import sys
import os
import asyncio
import importlib.util
from pathlib import Path
import inspect
import traceback
from datetime import datetime

# Add the parent directory to sys.path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent.parent
sys.path.insert(0, str(parent_dir))

# ANSI colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== {text} ==={Colors.ENDC}")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.ENDC}")

async def check_environment():
    print_header("Environment Check")

    # Check for .env file
    env_file = parent_dir / ".env"
    if env_file.exists():
        print_success("Found .env file")
    else:
        print_warning("No .env file found. Create one with required environment variables")

    # Check Python version
    python_version = sys.version.split()[0]
    major, minor, _ = python_version.split(".")
    if int(major) >= 3 and int(minor) >= 8:
        print_success(f"Python version: {python_version}")
    else:
        print_error(f"Python version {python_version} is too old. Upgrade to Python 3.8+")

    # Check required packages
    try:
        import fastapi
        print_success(f"FastAPI installed: {fastapi.__version__}")
    except ImportError:
        print_error("FastAPI not installed")

    try:
        import sqlalchemy
        print_success(f"SQLAlchemy installed: {sqlalchemy.__version__}")
    except ImportError:
        print_error("SQLAlchemy not installed")

    try:
        import alembic
        print_success(f"Alembic installed: {alembic.__version__}")
    except ImportError:
        print_error("Alembic not installed")

    try:
        import pydantic
        print_success(f"Pydantic installed: {pydantic.__version__}")
    except ImportError:
        print_error("Pydantic not installed")

    try:
        from app.core import config
        print_success("Config module found")
        try:
            settings = config.settings
            print_info(f"APP_ENV: {settings.APP_ENV}")
            print_info(f"POSTGRES_SERVER: {settings.POSTGRES_SERVER}")
            # Don't print password
            print_info(f"POSTGRES_DB: {settings.POSTGRES_DB}")
        except:
            print_error("Failed to import settings from config")
    except:
        print_error("Failed to import config module")

async def check_database():
    print_header("Database Check")

    try:
        from app.db.session import async_engine, get_db
        from sqlalchemy.ext.asyncio import AsyncSession
        from sqlalchemy.future import select
        from sqlalchemy import text

        print_success("Database modules imported successfully")

        # Test database connection
        try:
            async with async_engine.connect() as conn:
                result = await conn.execute(text("SELECT 1"))
                print_success("Database connection successful")

                # Check for existing tables
                result = await conn.execute(text(
                    "SELECT table_name FROM information_schema.tables "
                    "WHERE table_schema = 'public'"
                ))
                tables = [row[0] for row in result]
                if tables:
                    print_success(f"Found {len(tables)} tables in database: {', '.join(tables[:5])}" +
                                 ("..." if len(tables) > 5 else ""))
                else:
                    print_warning("No tables found in database. Run migrations.")
        except Exception as e:
            print_error(f"Database connection failed: {str(e)}")
    except Exception as e:
        print_error(f"Failed to import database modules: {str(e)}")

async def check_models():
    print_header("Model Check")

    models_dir = parent_dir / "app" / "models"
    if not models_dir.exists():
        print_error(f"Models directory not found: {models_dir}")
        return

    model_files = [f for f in models_dir.glob("*.py") if f.is_file() and f.name != "__init__.py"]
    print_info(f"Found {len(model_files)} model files")

    for model_file in model_files:
        module_name = f"app.models.{model_file.stem}"
        try:
            module = importlib.import_module(module_name)
            classes = [name for name, obj in inspect.getmembers(module, inspect.isclass)
                      if obj.__module__ == module_name]
            print_success(f"{model_file.name}: Found {len(classes)} classes")
        except Exception as e:
            print_error(f"Failed to import {model_file.name}: {str(e)}")

async def check_schemas():
    print_header("Schema Check")

    schemas_dir = parent_dir / "app" / "schemas"
    if not schemas_dir.exists():
        print_error(f"Schemas directory not found: {schemas_dir}")
        return

    schema_files = [f for f in schemas_dir.glob("*.py") if f.is_file() and f.name != "__init__.py"]
    print_info(f"Found {len(schema_files)} schema files")

    for schema_file in schema_files:
        module_name = f"app.schemas.{schema_file.stem}"
        try:
            module = importlib.import_module(module_name)
            classes = [name for name, obj in inspect.getmembers(module, inspect.isclass)
                      if obj.__module__ == module_name]
            print_success(f"{schema_file.name}: Found {len(classes)} classes")
        except Exception as e:
            print_error(f"Failed to import {schema_file.name}: {str(e)}")

async def check_api_endpoints():
    print_header("API Endpoints Check")

    try:
        from app.main import app
        from fastapi import APIRouter

        routes = []

        # Extract routes from app
        for route in app.routes:
            routes.append({
                "path": route.path,
                "methods": getattr(route, "methods", None),
                "name": route.name
            })

        print_success(f"Found {len(routes)} total routes in FastAPI app")

        # Group routes by prefix for better readability
        route_groups = {}
        for route in routes:
            parts = route["path"].split("/")
            if len(parts) > 2:
                prefix = f"/{parts[1]}"
                route_groups.setdefault(prefix, []).append(route)

        for prefix, group_routes in route_groups.items():
            print_info(f"{prefix}: {len(group_routes)} routes")

    except Exception as e:
        print_error(f"Failed to check API endpoints: {str(e)}")
        traceback.print_exc()

async def check_alembic():
    print_header("Alembic Migration Check")

    alembic_dir = parent_dir / "alembic"
    if not alembic_dir.exists():
        print_error("Alembic directory not found")
        return

    # Check alembic.ini
    alembic_ini = parent_dir / "alembic.ini"
    if alembic_ini.exists():
        print_success("Found alembic.ini")
    else:
        print_error("alembic.ini not found")

    # Check versions directory
    versions_dir = alembic_dir / "versions"
    if versions_dir.exists():
        version_files = list(versions_dir.glob("*.py"))
        print_success(f"Found {len(version_files)} migration versions")
    else:
        print_warning("No alembic versions directory found. Migrations may not be set up.")

    # Try to import alembic environment
    try:
        sys.path.insert(0, str(alembic_dir))
        import env
        print_success("Successfully imported alembic environment")
    except Exception as e:
        print_error(f"Failed to import alembic environment: {str(e)}")

async def run_checks():
    print(f"{Colors.BOLD}{Colors.HEADER}LinkedIn CRM Backend System Check{Colors.ENDC}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"System: {sys.platform}")
    print(f"Python: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Script location: {__file__}")

    try:
        await check_environment()
        await check_database()
        await check_models()
        await check_schemas()
        await check_api_endpoints()
        await check_alembic()

        print_header("Summary")
        print(f"{Colors.BOLD}Check completed.{Colors.ENDC}")
        print("Please review any warnings or errors above.")
        print("For detailed troubleshooting, refer to testing.md")
    except Exception as e:
        print_error(f"Check failed with an unexpected error: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_checks())