# InternAI API

FastAPI backend for the InternAI platform providing AI-powered internship matching and application assistance.

## Features

- **Profile Analysis**: Extract skills from resumes and LinkedIn profiles
- **Job Matching**: AI-powered matching between user profiles and job opportunities
- **Application Writing**: Generate personalized cover letters and application materials
- **Career Coaching**: Provide interview preparation and career guidance

## API Endpoints

### Core Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /api/info` - Detailed API information

### V1 API Endpoints

- `POST /v1/analyze` - Analyze user profile and extract skills
- `POST /v1/match` - Match user profile with job opportunities
- `POST /v1/write` - Generate application materials
- `POST /v1/coach` - Get career coaching and interview preparation

## Development

### Prerequisites

- Python 3.11+
- pip or poetry

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or using poetry
poetry install
```

### Running the Server

```bash
# Development server
python main.py

# Or using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Or using the project scripts
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Code Quality

```bash
# Run linting
ruff check . --fix

# Format code
black .

# Type checking
mypy .
```

### Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Environment Variables

Create a `.env` file with:

```env
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
```

## Models

### UserProfile
- `name`: Optional user name
- `email`: Optional email address
- `linkedin_url`: Optional LinkedIn profile URL
- `resume_url`: Optional resume file URL
- `skills`: Optional list of skills

### JobItem
- `id`: Unique job identifier
- `source`: Job source (e.g., "linkedin", "indeed")
- `title`: Job title
- `company`: Company name
- `location`: Optional job location
- `url`: Job posting URL
- `desc`: Optional job description

### MatchResult
- `job`: JobItem object
- `score`: Match score (0-100)
- `missing_skills`: List of skills the user lacks

## Example Usage

### Analyze Profile
```bash
curl -X POST "http://localhost:8000/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "skills": ["Python", "React"]
  }'
```

### Match Jobs
```bash
curl -X POST "http://localhost:8000/v1/match" \
  -H "Content-Type: application/json" \
  -d '{
    "profile": {
      "name": "John Doe",
      "skills": ["Python", "React"]
    },
    "jobs": [
      {
        "id": "1",
        "source": "linkedin",
        "title": "Software Engineer",
        "company": "TechCorp",
        "url": "https://example.com/job/1"
      }
    ]
  }'
```

## License

MIT License - see LICENSE file for details.
