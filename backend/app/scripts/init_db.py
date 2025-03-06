#!/usr/bin/env python
"""
Database initialization script for the LinkedIn CRM backend.
This script sets up the database, creates tables using Alembic migrations,
and optionally seeds the database with initial data.
"""

import sys
import os
import asyncio
import subprocess
from pathlib import Path
import argparse
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

def run_command(cmd, cwd=None):
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            shell=True,
            check=True,
            text=True,
            capture_output=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

async def check_database_connection():
    """Check if the database is accessible."""
    print_header("Checking Database Connection")

    try:
        from app.db.session import async_engine
        from sqlalchemy import text

        async with async_engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print_success("Database connection successful")
            return True
    except Exception as e:
        print_error(f"Database connection failed: {str(e)}")
        return False

async def create_migration():
    """Create a new Alembic migration if needed."""
    print_header("Creating Migration")

    # Check if there are any migration files
    versions_dir = parent_dir / "alembic" / "versions"
    if versions_dir.exists():
        migration_files = list(versions_dir.glob("*.py"))
        if migration_files:
            print_info(f"Found {len(migration_files)} existing migration files")
            return True

    # Create initial migration
    success, output = run_command(
        "alembic revision --autogenerate -m 'Initial database setup'",
        cwd=str(parent_dir)
    )

    if success:
        print_success("Created initial migration")
        return True
    else:
        print_error(f"Failed to create migration: {output}")
        return False

async def apply_migrations():
    """Apply all pending Alembic migrations."""
    print_header("Applying Migrations")

    success, output = run_command(
        "alembic upgrade head",
        cwd=str(parent_dir)
    )

    if success:
        print_success("Applied migrations successfully")
        return True
    else:
        print_error(f"Failed to apply migrations: {output}")
        return False

async def create_roles():
    """Create default roles in the database."""
    print_header("Creating Default Roles")

    try:
        from sqlalchemy.ext.asyncio import AsyncSession
        from sqlalchemy.future import select
        from app.db.session import async_engine
        from sqlalchemy.orm import sessionmaker
        from app.models.user import Role
        from datetime import datetime

        # Create session
        async_session = sessionmaker(
            async_engine, expire_on_commit=False, class_=AsyncSession
        )

        # Define default roles
        default_roles = [
            {
                "name": "admin",
                "description": "Administrator with full access to all features",
                "permissions": "*"  # Wildcard for all permissions
            },
            {
                "name": "manager",
                "description": "Manager with access to leads and campaigns",
                "permissions": "leads:read,leads:write,campaigns:read,campaigns:write,analytics:read"
            },
            {
                "name": "sales",
                "description": "Sales representative",
                "permissions": "leads:read,leads:write,campaigns:read"
            },
            {
                "name": "viewer",
                "description": "Read-only access",
                "permissions": "leads:read,campaigns:read,analytics:read"
            }
        ]

        async with async_session() as session:
            # Check and create roles
            roles_created = 0

            for role_data in default_roles:
                # Check if role exists
                role_result = await session.execute(
                    select(Role).where(Role.name == role_data["name"])
                )
                role = role_result.scalar_one_or_none()

                if not role:
                    # Create role
                    role = Role(
                        name=role_data["name"],
                        description=role_data["description"],
                        permissions=role_data["permissions"],
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow(),
                    )
                    session.add(role)
                    roles_created += 1
                    print_info(f"Created role: {role_data['name']}")

            if roles_created > 0:
                await session.commit()
                print_success(f"Created {roles_created} roles")
            else:
                print_info("All roles already exist")

            # Verify roles
            result = await session.execute(select(Role))
            roles = result.scalars().all()
            print_success(f"Total roles in database: {len(roles)}")

            return True
    except Exception as e:
        print_error(f"Failed to create roles: {str(e)}")
        traceback.print_exc()
        return False

async def create_admin_user(email, password, username, full_name):
    """Create an admin user if it doesn't exist."""
    print_header("Creating Admin User")

    try:
        from sqlalchemy.ext.asyncio import AsyncSession
        from sqlalchemy.future import select
        from app.db.session import async_engine
        from sqlalchemy.orm import sessionmaker
        from app.models.user import User, Role, user_role
        from app.core.security import get_password_hash
        from datetime import datetime

        # Create session
        async_session = sessionmaker(
            async_engine, expire_on_commit=False, class_=AsyncSession
        )

        async with async_session() as session:
            # Check if user exists
            user_result = await session.execute(
                select(User).where(User.email == email)
            )
            user = user_result.scalar_one_or_none()

            if user:
                print_info(f"User with email {email} already exists")
                return True

            # Get admin role
            role_result = await session.execute(
                select(Role).where(Role.name == "admin")
            )
            admin_role = role_result.scalar_one_or_none()

            if not admin_role:
                print_error("Admin role not found. Run create_roles first.")
                return False

            # Create user
            user = User(
                email=email,
                username=username,
                hashed_password=get_password_hash(password),
                full_name=full_name,
                is_active=True,
                is_superuser=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(user)
            await session.flush()

            # Associate user with admin role
            stmt = user_role.insert().values(user_id=user.id, role_id=admin_role.id)
            await session.execute(stmt)

            await session.commit()

            print_success(f"Created admin user: {email}")
            return True
    except Exception as e:
        print_error(f"Failed to create admin user: {str(e)}")
        traceback.print_exc()
        return False

async def init_db(seed=False, create_admin=False, admin_email="admin@example.com",
                admin_password="admin123", admin_username="admin", admin_fullname="Admin User"):
    """Initialize the database with tables and optional seed data."""
    print(f"{Colors.BOLD}{Colors.HEADER}LinkedIn CRM Database Initialization{Colors.ENDC}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Check database connection
    if not await check_database_connection():
        print_error("Cannot proceed without database connection")
        return False

    # Create and apply migrations
    if not await create_migration():
        print_warning("Migration creation failed, but will try to continue")

    if not await apply_migrations():
        print_error("Cannot proceed without applying migrations")
        return False

    if seed:
        # Create roles
        if not await create_roles():
            print_warning("Failed to create roles, but will try to continue")

        # Create admin user if requested
        if create_admin:
            if not await create_admin_user(admin_email, admin_password, admin_username, admin_fullname):
                print_warning("Failed to create admin user")

    print_header("Summary")
    print_success("Database initialization completed")
    if seed:
        print_info("Seed data was created")
    if create_admin:
        print_info(f"Admin user: {admin_email}")

    return True

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Initialize the LinkedIn CRM database")
    parser.add_argument("--no-seed", action="store_true", help="Skip seeding the database with initial data")
    parser.add_argument("--admin", action="store_true", help="Create admin user")
    parser.add_argument("--email", default="admin@example.com", help="Admin email")
    parser.add_argument("--password", default="admin123", help="Admin password")
    parser.add_argument("--username", default="admin", help="Admin username")
    parser.add_argument("--fullname", default="Admin User", help="Admin full name")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    seed = not args.no_seed
    asyncio.run(init_db(
        seed=seed,
        create_admin=args.admin,
        admin_email=args.email,
        admin_password=args.password,
        admin_username=args.username,
        admin_fullname=args.fullname
    ))