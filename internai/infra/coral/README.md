# Coral Infrastructure

This directory contains configuration and documentation for running Coral distributed computing platform with InternAI.

## Overview

Coral is a distributed computing platform that enables:
- Agent registration and discovery
- Distributed agent execution
- Usage tracking and billing
- Load balancing and scaling

## Local Development Setup

### Option 1: Docker (Recommended)

Run Coral locally using the official Docker image:

```bash
# Pull the latest Coral image
docker pull coral-platform/coral:latest

# Run Coral server with default configuration
docker run -d \
  --name coral-server \
  -p 8080:8080 \
  -e CORAL_API_KEY=your_api_key_here \
  coral-platform/coral:latest

# Verify Coral is running
curl http://localhost:8080/health
```

### Option 2: Docker Compose

For a more complete setup with dependencies:

```bash
# Create docker-compose.yml (see below)
docker-compose up -d

# Check status
docker-compose ps
```

### Option 3: From Source

```bash
# Clone Coral repository
git clone https://github.com/coral-platform/coral.git
cd coral

# Install dependencies
pip install -r requirements.txt

# Run development server
python main.py --host 0.0.0.0 --port 8080
```

## Configuration

### Environment Variables

Create a `.env` file in your project root:

```bash
# Coral Configuration
CORAL_SERVER_URL=http://localhost:8080
CORAL_API_KEY=your_coral_api_key_here

# Optional: Advanced configuration
CORAL_TIMEOUT=30
CORAL_RETRY_ATTEMPTS=3
CORAL_RATE_LIMIT=100
```

### Docker Compose Example

```yaml
version: '3.8'
services:
  coral:
    image: coral-platform/coral:latest
    ports:
      - "8080:8080"
    environment:
      - CORAL_API_KEY=${CORAL_API_KEY}
      - CORAL_DATABASE_URL=postgresql://coral:coral@postgres:5432/coral
      - CORAL_REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
    volumes:
      - coral_data:/var/lib/coral

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=coral
      - POSTGRES_USER=coral
      - POSTGRES_PASSWORD=coral
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/var/lib/redis

volumes:
  coral_data:
  postgres_data:
  redis_data:
```

## Managed Coral Service

For production deployments, use the managed Coral service:

### Registration

1. Sign up at [coral-platform.com](https://coral-platform.com)
2. Create a new project
3. Generate an API key
4. Update your environment variables

### Configuration

```bash
# Production Coral configuration
CORAL_SERVER_URL=https://api.coral-platform.com
CORAL_API_KEY=your_production_api_key_here
```

## Agent Registration

InternAI automatically registers agents with Coral on startup:

```python
# Agents are registered automatically when the API starts
# Check registered agents:
curl http://localhost:8000/v1/agents
```

### Manual Agent Registration

You can also register agents manually:

```python
from app.coral_client import CoralClient

client = CoralClient()
result = client.register_agent(
    name="custom_agent",
    description="Custom agent description",
    schema={"input": {}, "output": {}},
    endpoint="/v1/custom",
    pricing={"per_request": 0.01}
)
```

## Monitoring

### Health Checks

```bash
# Check Coral server health
curl http://localhost:8080/health

# Check agent status
curl http://localhost:8000/v1/agents
```

### Logs

```bash
# Docker logs
docker logs coral-server

# Docker Compose logs
docker-compose logs coral
```

## Troubleshooting

### Common Issues

1. **Connection Refused**
   - Ensure Coral server is running
   - Check port configuration (default: 8080)
   - Verify firewall settings

2. **Authentication Failed**
   - Verify CORAL_API_KEY is set correctly
   - Check API key permissions

3. **Agent Registration Failed**
   - Ensure agent schemas are valid JSON
   - Check endpoint URLs are accessible
   - Verify agent names are unique

### Debug Mode

Enable debug logging:

```bash
# Set debug environment variable
export CORAL_DEBUG=true

# Or in .env file
CORAL_DEBUG=true
```

## Security

### API Key Management

- Store API keys in environment variables
- Never commit API keys to version control
- Rotate API keys regularly
- Use different keys for development and production

### Network Security

- Use HTTPS in production
- Configure proper CORS settings
- Implement rate limiting
- Monitor API usage

## Performance

### Optimization Tips

- Use connection pooling
- Implement caching for frequently accessed data
- Monitor memory usage
- Scale horizontally when needed

### Monitoring

- Set up alerts for high error rates
- Monitor response times
- Track resource usage
- Implement health checks

## Support

- Documentation: [docs.coral-platform.com](https://docs.coral-platform.com)
- Community: [community.coral-platform.com](https://community.coral-platform.com)
- Issues: [github.com/coral-platform/coral/issues](https://github.com/coral-platform/coral/issues)
