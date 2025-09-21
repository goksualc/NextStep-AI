# InternAI

> AI-powered internship matching and application assistance platform

InternAI is a comprehensive monorepo that leverages artificial intelligence to revolutionize the internship application process. The platform combines intelligent matching algorithms, automated application writing, and personalized career coaching to help students and professionals find their ideal internship opportunities.

## 🚀 Product Vision

InternAI aims to democratize access to quality internship opportunities by:

- **Smart Matching**: AI-powered algorithms that connect candidates with relevant internship opportunities based on skills, experience, and career goals
- **Application Automation**: Intelligent writing assistants that generate personalized cover letters and application materials
- **Career Coaching**: Personalized guidance and recommendations to accelerate professional development
- **Comprehensive Analysis**: Deep analysis of CVs/resumes to extract structured profiles and identify optimization opportunities

## 🏗️ Architecture

InternAI follows a modern microservices architecture with the following components:

### Frontend (`apps/web`)
- **Framework**: Next.js 15 with App Router
- **Styling**: Tailwind CSS
- **Language**: TypeScript with strict mode
- **Features**: Dashboard, job matching, application tracking, career coaching

### Backend (`apps/api`)
- **Framework**: FastAPI (Python 3.11+)
- **Features**: RESTful API, health monitoring, agent orchestration
- **Dependencies**: Pydantic, Uvicorn, HTTPx

### AI Agents (`agents/`)
- **CV Analyzer**: Extracts structured information from resumes/CVs
- **Job Scout**: Discovers internship opportunities from various sources
- **Matcher**: AI-powered matching between profiles and opportunities
- **App Writer**: Generates personalized application materials
- **Coach**: Provides career guidance and recommendations

### Shared Packages (`packages/`)
- **Prompts**: YAML-based prompt templates for AI agents
- **Embeddings**: Unified interface for text vectorization

### Infrastructure (`infra/`)
- **Coral**: Distributed computing and agent orchestration

## 🛠️ Technology Stack

### Frontend
- Next.js 15
- React 18
- TypeScript
- Tailwind CSS
- App Router

### Backend
- FastAPI
- Python 3.11+
- Pydantic
- Uvicorn
- HTTPx

### AI/ML
- OpenAI/Mistral APIs
- Sentence Transformers (local embeddings)
- NumPy
- PyYAML

### Development
- ESLint + Prettier
- Black + Ruff
- MyPy (type checking)
- Makefile for automation

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd internai
   ```

2. **Run initial setup**
   ```bash
   make setup
   ```

3. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your API keys and configuration
   ```

4. **Start development servers**
   ```bash
   # Start both web and API servers
   make dev

   # Or start individually
   make dev-web    # Next.js on http://localhost:3000
   make dev-api    # FastAPI on http://localhost:8000
   ```

### Environment Configuration

Copy `env.example` to `.env` and configure:

```bash
# Required API Keys
MISTRAL_API_KEY=your_mistral_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Coral Configuration
CORAL_SERVER_URL=http://localhost:8080
CORAL_API_KEY=your_coral_api_key_here

# Application URLs
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📁 Project Structure

```
internai/
├── apps/
│   ├── web/                    # Next.js frontend application
│   │   ├── src/app/           # App Router pages
│   │   ├── package.json       # Dependencies and scripts
│   │   └── next.config.js     # Next.js configuration
│   └── api/                   # FastAPI backend application
│       ├── main.py           # FastAPI application entry point
│       ├── requirements.txt  # Python dependencies
│       └── pyproject.toml    # Project configuration
├── agents/                    # AI agent implementations
│   ├── cv_analyzer/          # CV/resume analysis
│   ├── job_scout/            # Job opportunity discovery
│   ├── matcher/              # Profile-job matching
│   ├── app_writer/           # Application material generation
│   └── coach/                # Career coaching and advice
├── packages/                  # Shared libraries
│   ├── prompts/              # YAML prompt templates
│   └── embeddings/           # Text embedding utilities
├── infra/                     # Infrastructure configuration
│   └── coral/                # Coral orchestration setup
├── Makefile                  # Development automation
├── env.example               # Environment variable template
└── README.md                 # This file
```

## 🔧 Development Commands

### Setup and Installation
```bash
make setup              # Initial project setup
make install-deps       # Install all dependencies
make install-web-deps   # Install frontend dependencies only
make install-api-deps   # Install backend dependencies only
```

### Development
```bash
make dev                # Start both web and API servers
make dev-web           # Start Next.js development server
make dev-api           # Start FastAPI development server
```

### Code Quality
```bash
make lint              # Run linting for all projects
make format            # Format code for all projects
make type-check        # Run type checking
```

### Testing
```bash
make test              # Run tests for all projects
make test-agents       # Test AI agents specifically
```

### Utilities
```bash
make clean             # Clean build artifacts
make build             # Build for production
make health            # Check service health
make docs              # Generate API documentation
```

## 🌐 API Documentation

Once the API server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Key Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /api/info` - Detailed API information

## 🤖 AI Agents Overview

### CV Analyzer
Extracts structured information from CVs/resumes including:
- Personal information (name, contact details)
- Education history
- Work experience
- Skills and competencies
- Languages and certifications

### Job Scout
Discovers internship opportunities from:
- LinkedIn job postings
- Company career pages
- Job boards and aggregators
- University career services

### Matcher
AI-powered matching algorithm that considers:
- Technical skill alignment
- Experience level compatibility
- Location preferences
- Cultural fit assessment
- Career progression opportunities

### App Writer
Generates personalized application materials:
- Cover letters tailored to specific roles
- Email templates for applications
- Follow-up messages
- Thank you notes

### Coach
Provides personalized career guidance:
- Skill development recommendations
- Interview preparation tips
- Networking strategies
- Career planning advice
- Portfolio optimization

## 🔒 Security & Privacy

- Environment variables for sensitive configuration
- CORS middleware for API security
- Input validation with Pydantic
- TypeScript strict mode for frontend safety
- Comprehensive .gitignore for sensitive files

## 🚀 Deployment

### Production Build
```bash
make build              # Build frontend for production
```

### Docker Support
```bash
make docker-build       # Build Docker images
make docker-run         # Run with Docker Compose
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting (`make test && make lint`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines

- Follow TypeScript strict mode for frontend code
- Use Black and Ruff for Python formatting and linting
- Write comprehensive docstrings for Python functions
- Add type hints for all Python functions
- Test all new features before submitting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Check the API documentation at http://localhost:8000/docs
- Review the health status with `make health`
- Check logs for detailed error information

## 🔮 Roadmap

- [ ] Database integration (PostgreSQL)
- [ ] User authentication and authorization
- [ ] Real-time notifications
- [ ] Advanced analytics dashboard
- [ ] Mobile application
- [ ] Enterprise features
- [ ] Multi-language support

---

**Built with ❤️ by the InternAI team**
