# LinkedIn CRM Backend Testing Guide

This document outlines a systematic approach to testing the LinkedIn CRM backend and resolving common issues. Follow these steps sequentially to ensure proper functionality of all components.

## Phase 1: Environment Setup and Basic Verification

### Step 1: Verify Dependencies

```bash
# Check Python version (should be 3.8+)
python --version

# Install required packages
pip install -r requirements.txt

# Verify FastAPI installation
pip show fastapi
```

**Expected outcome**: All dependencies should install without errors. FastAPI should be at version 0.95.0 or higher.

**Common issues**:
- Package conflicts: Use a virtual environment
- Missing system dependencies: Install required system packages based on error messages

### Step 2: Environment Configuration

```bash
# Copy the example environment file
cp backend/.env.example backend/.env

# Edit the .env file with your configuration
# At minimum, set the database connection and SECRET_KEY
```

**Expected outcome**: Environment file should be created with all necessary configuration.

### Step 3: Database Setup

```bash
# Start PostgreSQL (if not already running)
# For Docker:
docker run --name pg-linkedin-crm -e POSTGRES_PASSWORD=password -e POSTGRES_DB=linkedin_crm -p 5432:5432 -d postgres

# Initialize the database using the provided script
cd backend
python -m app.scripts.init_db --admin
```

**Expected outcome**: Database tables should be created successfully based on SQLAlchemy models, and an admin user should be created.

**Common issues**:
- Database connection errors: Verify PostgreSQL is running and credentials are correct
- Migration errors: Check model definitions for inconsistencies

## Phase 2: Core Functionality Testing

### Step 4: Run System Checks

```bash
# Run the diagnostic script to verify system setup
cd backend
python -m app.scripts.check_system
```

**Expected outcome**: All checks should pass or provide clear instructions for fixing issues.

**Common issues**:
- Missing dependencies: Install required packages
- Configuration errors: Check your .env file
- Database connectivity: Verify database credentials and connection

### Step 5: Start the Application

```bash
# Start the application in development mode
cd backend
uvicorn app.main:app --reload
```

**Expected outcome**: The application should start without errors and be accessible at http://localhost:8000.

### Step 6: Test Health Endpoints

```bash
# Test the root endpoint
curl http://localhost:8000/

# Test the API status endpoint
curl http://localhost:8000/api/status

# Test the database health check
curl http://localhost:8000/api/v1/health/db
```

**Expected outcome**: All health endpoints should return 200 OK responses.

**Common issues**:
- Server not starting: Check for port conflicts or permission issues
- Database health check failing: Verify database connection settings

## Phase 3: Authentication Testing

### Step 7: Test Login and Token Generation

```bash
# Login with admin credentials
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=admin123" \
  > token_response.json

# Extract token for later use
export TOKEN=$(cat token_response.json | jq -r '.access_token')
```

**Expected outcome**: A valid JWT token should be returned.

**Common issues**:
- Authentication failing: Verify credential values
- Token format issues: Check token generation code

## Phase 4: Data Model Testing

### Step 8: Test User Endpoints

```bash
# Get current user
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/users/me

# List all users
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/users/
```

**Expected outcome**: The API should return user information.

**Common issues**:
- Authentication issues: Verify token settings in config.py
- Permission issues: Check role-based access control

### Step 9: Create Basic Lead Data

```bash
# Create a test lead
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test Lead",
    "email": "test@example.com",
    "job_title": "CTO",
    "company": "Test Company",
    "linkedin_url": "https://linkedin.com/in/testlead",
    "status": "new",
    "source": "manual"
  }' \
  http://localhost:8000/api/v1/leads/
```

**Expected outcome**: A new lead should be created and returned with an ID.

**Common issues**:
- Validation errors: Check schema definitions
- Database constraints: Verify model foreign key relationships

## Phase 5: Advanced Functionality Testing

### Step 10: Test Lead Scoring

```bash
# Create a lead scoring rule
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "C-Level Executive",
    "description": "Higher score for C-level executives",
    "field": "job_title",
    "operator": "contains",
    "value": ["CEO", "CTO", "CIO", "CFO", "COO"],
    "score_value": 20,
    "is_active": true
  }' \
  http://localhost:8000/api/v1/scoring/rules/

# Apply scoring to leads
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "lead_ids": [1]
  }' \
  http://localhost:8000/api/v1/scoring/apply/
```

**Expected outcome**: Lead scoring rule should be created and applied successfully.

**Common issues**:
- Missing implementation: Verify that lead scoring logic is implemented
- Scoring calculation errors: Check scoring logic algorithm

### Step 11: Test LinkedIn Integration

```bash
# Configure LinkedIn settings
curl -X PUT \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "linkedin_settings": {
      "username": "test@example.com",
      "password": "test_password",
      "max_actions_per_day": 25
    }
  }' \
  http://localhost:8000/api/v1/settings/system/

# Test a profile scrape
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "job_type": "Profile",
    "target_url": "https://linkedin.com/in/testprofile",
    "priority": 1
  }' \
  http://localhost:8000/api/v1/scraping/jobs/
```

**Expected outcome**: A scrape job should be created and queued.

**Common issues**:
- LinkedIn authentication issues: Check credential handling
- Rate limiting or blocking: Implement proper delays and proxy rotation

## Phase 6: Performance and Error Testing

### Step 12: Test Error Handling

```bash
# Test with invalid data
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "",
    "email": "not-an-email"
  }' \
  http://localhost:8000/api/v1/leads/

# Test with non-existent resource
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/leads/9999
```

**Expected outcome**: Proper error responses with appropriate status codes.

**Common issues**:
- Missing error handling: Add comprehensive exception handlers
- Unclear error messages: Improve error response structure

### Step 13: Load Testing (Basic)

```bash
# Install artillery if needed
npm install -g artillery

# Create a basic test file (test.yml)
# Run a basic load test
artillery quick --count 10 -n 20 http://localhost:8000/api/status
```

**Expected outcome**: The application should handle the load without errors.

## Phase 7: Bug Fixing and Iteration

### Step 14: Common Issues and Fixes

#### Issue 1: Database Connection Errors

If you encounter database connection errors:

1. Use the database diagnostic command:
```bash
python -m app.scripts.check_system
```

2. Verify PostgreSQL is running:
```bash
pg_isready -h localhost -p 5432
```

3. Check connection string in .env file:
```
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=linkedin_crm
```

4. Test direct connection:
```bash
psql -h localhost -U postgres -d linkedin_crm
```

#### Issue 2: Authentication Problems

If token authentication is failing:

1. Run the init_db script to create an admin user:
```bash
python -m app.scripts.init_db --admin --email admin@example.com --password admin123
```

2. Check JWT secret key configuration in .env
3. Verify token expiration settings
4. Inspect token payload structure

```bash
# Decode JWT token to inspect
echo $TOKEN | cut -d "." -f2 | base64 -d 2>/dev/null | jq .
```

#### Issue 3: Model Relationships

If you encounter foreign key or relationship errors:

1. Review model definitions for correct relationships
2. Check for circular imports
3. Verify cascading delete behavior

#### Issue 4: API Validation Errors

For Pydantic validation issues:

1. Check schema definitions for correct types
2. Add more descriptive validators
3. Use proper field constraints

### Step 15: Continuous Integration

Set up a basic CI pipeline for automated testing:

```bash
# Create a test script
cat > backend/run_tests.sh << 'EOF'
#!/bin/bash
set -e

echo "Running backend tests..."
cd backend
pytest -v

echo "Checking code formatting..."
black --check .

echo "Running linters..."
flake8 .

echo "All tests passed!"
EOF

chmod +x backend/run_tests.sh
```

**Expected outcome**: A basic test script that can be integrated into CI/CD.

## Utility Scripts Reference

The LinkedIn CRM backend comes with several utility scripts to help with development, testing, and troubleshooting:

### System Check Script

The `app.scripts.check_system` module provides comprehensive diagnostics of your setup:

```bash
python -m app.scripts.check_system
```

This will check:
- Environment configuration
- Database connectivity
- Model and schema integrity
- API endpoint availability
- Alembic migration setup

### Database Initialization Script

The `app.scripts.init_db` module initializes and seeds the database:

```bash
# Basic initialization
python -m app.scripts.init_db

# Initialize with admin user
python -m app.scripts.init_db --admin

# Initialize with custom admin user
python -m app.scripts.init_db --admin --email admin@yourdomain.com --password securepassword
```

Options:
- `--no-seed`: Skip seeding the database with initial data
- `--admin`: Create admin user
- `--email`: Admin email address
- `--password`: Admin password
- `--username`: Admin username
- `--fullname`: Admin full name

## Final Verification

After completing all steps and fixing identified issues:

1. Restart the application from scratch
2. Verify that all endpoints work as expected
3. Test the full lead management workflow from creation to scoring
4. Verify that LinkedIn integration functions properly
5. Check that authentication and permissions work correctly

## Troubleshooting Checklist

- [ ] Verify all environment variables are set correctly in .env
- [ ] Run the system check script to diagnose issues
- [ ] Check database connection and migrations
- [ ] Ensure proper authentication configuration
- [ ] Validate model relationships and constraints
- [ ] Test API endpoints with valid and invalid data
- [ ] Verify error handling and responses
- [ ] Check performance under basic load

## Next Steps

After basic functionality is verified, consider:

1. Adding comprehensive test coverage
2. Setting up continuous integration
3. Implementing monitoring and logging
4. Performance optimization
5. Security hardening