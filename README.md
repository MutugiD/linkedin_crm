# LinkedIn CRM Automation

A comprehensive LinkedIn automation solution that includes cookie-less scraping, lead scoring, automated outreach, and a custom CRM interface.

## Features

- **Cookie-less LinkedIn Scraping:** Extract LinkedIn profile, company, and content data without requiring cookies or logins
- **Lead Scoring:** Score prospects against your ICP based on industry fit, tool usage, revenue alignment, and role relevance
- **Automated Outreach:** Manage connection requests, message sequences, and follow-ups automatically
- **Pipeline Management:** Track leads through customizable pipeline stages with sentiment-based updates
- **Advanced Features:** Find key players in companies, export custom LinkedIn searches, and monitor company news
- **Custom CRM Interface:** Manage your entire sales process through a modern, intuitive interface

## Project Structure

```
linkedin_crm/
├── backend/         # Python FastAPI backend
├── frontend/        # React.js frontend
├── docker/          # Docker configuration
├── scripts/         # Utility scripts
├── docs/            # Documentation
├── planning.md      # Project planning documentation
├── prompts.md       # Development prompts and questions
└── product_features.md # Detailed product features
```

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 14+
- PostgreSQL 13+
- Docker and Docker Compose (optional, for containerized setup)

### Installation

1. Clone the repository
   ```
   git clone https://github.com/yourusername/linkedin_crm.git
   cd linkedin_crm
   ```

2. Set up the backend
   ```
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up the frontend
   ```
   cd frontend
   npm install
   ```

4. Set up the database
   ```
   # Create PostgreSQL database (using psql)
   createdb linkedin_crm

   # Run migrations
   cd backend
   alembic upgrade head
   ```

5. Start the development servers
   ```
   # Backend
   cd backend
   uvicorn app.main:app --reload

   # Frontend
   cd frontend
   npm start
   ```

### Docker Setup (Alternative)

1. Build and start the containers
   ```
   docker-compose up -d
   ```

2. Access the application at http://localhost:3000

## Development

- Backend API is available at http://localhost:8000
- API documentation is available at http://localhost:8000/docs
- Frontend development server runs at http://localhost:3000

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://reactjs.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)