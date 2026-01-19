# Investment Research Crew

[![CI (lint + test)](https://github.com/blitznihar/investment-research-crew/actions/workflows/pylint.yml/badge.svg)](https://github.com/blitznihar/investment-research-crew/actions/workflows/pylint.yml)
[![codecov](https://codecov.io/github/blitznihar/investment-research-crew/graph/badge.svg?token=CxxB9Ew6Lx)](https://codecov.io/github/blitznihar/investment-research-crew)
![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![Last Commit](https://img.shields.io/github/last-commit/blitznihar/investment-research-crew)
![License](https://img.shields.io/github/license/blitznihar/investment-research-crew?cacheSeconds=0)
![CrewAI](https://img.shields.io/badge/CrewAI-000000?style=for-the-badge&logo=ai&logoColor=white)

## Overview

**Investment Research Crew** is an AI-powered multi-agent system built with [CrewAI](https://crewai.com/) that automates investment research report generation and analysis. The system uses specialized agents for content planning, writing, and editing to produce comprehensive, well-researched investment reports.

This is a production-ready **FastAPI application** deployable to Docker, Kubernetes, or any container orchestration platform.

## Features

- **Content Planning Agent**: Researches and plans content structure with SEO optimization
- **Content Writing Agent**: Generates engaging, factually accurate investment analysis articles
- **Content Editing Agent**: Reviews and refines content for quality and consistency
- **RESTful API**: FastAPI-based HTTP endpoints for programmatic access
- **Flexible LLM Support**: Works with OpenAI, local Docker AI, or LM Studio
- **Container-Ready**: Docker and Docker Compose support for easy deployment
- **Kubernetes Compatible**: Deploy to any Kubernetes cluster
- **Configurable Settings**: Environment-based configuration for easy customization

## Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Docker and Docker Compose (for containerized deployment)
- API key for your preferred LLM provider (OpenAI, Docker AI, or LM Studio)

## Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/blitznihar/investment-research-crew.git
cd investment-research-crew
```

2. Install dependencies using uv:
```bash
uv sync
```

3. Configure your environment:
```bash
cp .env.example .env
```

Edit `.env` and set your preferred LLM provider credentials:

**For OpenAI:**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini

API_HOST=0.0.0.0
API_PORT=8542
API_RELOAD=true
```

**For Docker AI (local):**
```env
LLM_PROVIDER=docker
DOCKER_AI_API_URL=http://localhost:12434/engines/v1
DOCKER_AI_API_KEY=docker
DOCKER_AI_MODEL=openai/gpt-oss

API_HOST=0.0.0.0
API_PORT=8542
API_RELOAD=true
```

**For LM Studio (local):**
```env
LLM_PROVIDER=lmstudio
LMSTUDIO_API_URL=http://127.0.0.1:1234/v1
LMSTUDIO_API_KEY=lm-studio
LMSTUDIO_MODEL=openai/gpt-oss-20b

API_HOST=0.0.0.0
API_PORT=8542
API_RELOAD=true
```

### Docker Deployment

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8542`

2. Run in detached mode:
```bash
docker-compose up -d
```

3. View logs:
```bash
docker-compose logs -f investment-research-crew
```

4. Stop the service:
```bash
docker-compose down
```

### Docker Build (Manual)

Build the Docker image manually:
```bash
docker build -t investment-research-crew:latest .
```

Run the container:
```bash
docker run -p 8542:8542 \
  -e LLM_PROVIDER=docker \
  -e DOCKER_AI_API_URL=http://host.docker.internal:12434/engines/v1 \
  -e DOCKER_AI_API_KEY=docker \
  -e DOCKER_AI_MODEL=openai/ai/gpt-oss \
  investment-research-crew:latest
```

## Usage

### Running the API Server

#### Local Development
```bash
uv run investment-research-crew
```

The API will start at `http://localhost:8542` (or the port specified in your `.env` file).

#### Docker Compose
```bash
docker-compose up
```

### API Endpoints

#### Health Check
Check if the API is running and view configuration:

```bash
curl http://localhost:8542/health
```

Response:
```json
{
  "status": "ok",
  "llm_provider": "docker",
  "docker_ai_url": "http://host.docker.internal:12434/engines/v1",
  "docker_ai_model": "openai/ai/gpt-oss",
  "docker_key_present": true
}
```

#### Run Content Generation
Generate an investment research report for a specific topic:

**Using curl:**
```bash
curl -X POST http://localhost:8542/content/run \
  -H "Content-Type: application/json" \
  -d '{"topic": "Artificial Intelligence in Healthcare"}'
```

**Using Python requests:**
```python
import requests

response = requests.post(
    "http://localhost:8542/content/run",
    json={"topic": "Artificial Intelligence in Healthcare"}
)

print(response.json())
```

**Response:**
```json
{
  "topic": "Artificial Intelligence in Healthcare",
  "result": "# Investment Research Report: AI in Healthcare\n\n..."
}
```

#### Interactive API Documentation
Once the server is running, visit:
- Swagger UI: `http://localhost:8542/docs`
- ReDoc: `http://localhost:8542/redoc`

### Run Tests

Execute unit tests with coverage:

```bash
uv run pytest --cov
```

Run linting checks:

```bash
uv run ruff check .
uv run pylint src
```

## Kubernetes Deployment

### Basic Kubernetes Deployment

1. Create a Kubernetes deployment YAML (`k8s-deployment.yaml`):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: investment-research-crew
spec:
  replicas: 2
  selector:
    matchLabels:
      app: investment-research-crew
  template:
    metadata:
      labels:
        app: investment-research-crew
    spec:
      containers:
      - name: investment-research-crew
        image: investment-research-crew:latest
        ports:
        - containerPort: 8542
        env:
        - name: API_HOST
          value: "0.0.0.0"
        - name: API_PORT
          value: "8542"
        - name: LLM_PROVIDER
          value: "docker"
        - name: DOCKER_AI_API_URL
          valueFrom:
            configMapKeyRef:
              name: llm-config
              key: docker_ai_url
        - name: DOCKER_AI_API_KEY
          valueFrom:
            secretKeyRef:
              name: llm-secrets
              key: docker_ai_key
        - name: DOCKER_AI_MODEL
          value: "openai/ai/gpt-oss"
---
apiVersion: v1
kind: Service
metadata:
  name: investment-research-crew-service
spec:
  selector:
    app: investment-research-crew
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8542
  type: LoadBalancer
```

2. Apply the deployment:
```bash
kubectl apply -f k8s-deployment.yaml
```

3. Check deployment status:
```bash
kubectl get pods
kubectl get services
```

## Project Structure

```
investment-research-crew/
├── src/investment_research_crew/
│   ├── agents/          # Agent definitions (planner, writer, editor)
│   ├── crews/           # Crew orchestration logic
│   ├── tasks/           # Task definitions for agents
│   ├── tools/           # Custom tools and utilities
│   ├── rag/             # RAG (Retrieval Augmented Generation) components
│   ├── api.py           # FastAPI application and endpoints
│   ├── config.py        # Configuration and settings management
│   └── main.py          # Entry point for CLI and server startup
├── tests/               # Unit tests
├── Dockerfile           # Docker image definition
├── docker-compose.yml   # Docker Compose configuration
├── pyproject.toml       # Project metadata and dependencies
└── README.md            # This file
```

## Configuration

Settings are managed through [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) and support both environment variables and `.env` file loading.

See [src/investment_research_crew/config.py](src/investment_research_crew/config.py) for detailed configuration options.

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_PROVIDER` | LLM provider (`openai`, `docker`, `lmstudio`) | `openai` |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `OPENAI_API_URL` | OpenAI API endpoint | `https://api.openai.com/v1` |
| `OPENAI_MODEL` | OpenAI model name | `gpt-4o-mini` |
| `DOCKER_AI_API_URL` | Docker AI endpoint | `http://localhost:12434/engines/v1` |
| `DOCKER_AI_API_KEY` | Docker AI API key | `docker` |
| `DOCKER_AI_MODEL` | Docker AI model | `openai/ai/gpt-oss` |
| `API_HOST` | API server host | `0.0.0.0` |
| `API_PORT` | API server port | `8542` |
| `API_RELOAD` | Enable auto-reload (dev only) | `true` |

## Dependencies

Key dependencies:
- `crewai` - Multi-agent orchestration framework
- `crewai-tools` - Pre-built tools for agents
- `fastapi` - Modern web framework for building APIs
- `uvicorn` - ASGI server for FastAPI
- `langchain-community` - LangChain community integrations
- `litellm` - LLM abstraction layer
- `pydantic` - Data validation
- `python-dotenv` - Environment variable management

See [pyproject.toml](pyproject.toml) for the complete list.

## Development

### Setup Development Environment

```bash
uv sync
```

### Run Tests

```bash
uv run pytest
```

### Run Linting

```bash
uv run ruff check .
uv run ruff format .
uv run pylint src
```

### Local API Development

Start the API server with auto-reload:
```bash
uv run investment-research-crew
```

## Production Deployment Considerations

- **Environment Variables**: Use secrets management (Kubernetes Secrets, AWS Secrets Manager, etc.) for sensitive credentials
- **Scaling**: Configure horizontal pod autoscaling in Kubernetes based on CPU/memory metrics
- **Load Balancing**: Use Ingress controllers or cloud load balancers for production traffic
- **Monitoring**: Integrate with Prometheus, Grafana, or cloud monitoring solutions
- **Logging**: Configure structured logging and ship logs to centralized logging systems
- **Rate Limiting**: Implement API rate limiting to prevent abuse

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Nihar Malali** - [GitHub](https://github.com/blitznihar)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.