# Investment Research Crew

[![CI (lint + test)](https://github.com/blitznihar/investment-research-crew/actions/workflows/pylint.yml/badge.svg)](https://github.com/blitznihar/investment-research-crew/actions/workflows/pylint.yml)
[![codecov](https://codecov.io/github/blitznihar/investment-research-crew/graph/badge.svg?token=CxxB9Ew6Lx)](https://codecov.io/github/blitznihar/investment-research-crew)
![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![Last Commit](https://img.shields.io/github/last-commit/blitznihar/investment-research-crew)
![License](https://img.shields.io/github/license/blitznihar/investment-research-crew?cacheSeconds=0)
![CrewAI](https://img.shields.io/badge/CrewAI-000000?style=for-the-badge&logo=ai&logoColor=white)

## Overview

**Investment Research Crew** is an AI-powered multi-agent system built with [CrewAI](https://crewai.com/) that automates investment research report generation and analysis. The system uses specialized agents for content planning, writing, and editing to produce comprehensive, well-researched investment reports.

This is a production-ready **FastAPI application** with built-in resilience testing capabilities using RabbitMQ message queuing, deployable to Docker, Kubernetes, or any container orchestration platform.

## Features

- **Content Planning Agent**: Researches and plans content structure with SEO optimization
- **Content Writing Agent**: Generates engaging, factually accurate investment analysis articles
- **Content Editing Agent**: Reviews and refines content for quality and consistency
- **Test Crew**: Resilience testing framework using RabbitMQ for message-driven testing
- **RESTful API**: FastAPI-based HTTP endpoints for programmatic access
- **RabbitMQ Integration**: Message queue support for async task processing and testing
- **Flexible LLM Support**: Works with OpenAI, local Docker AI, or LM Studio
- **Container-Ready**: Docker and Docker Compose support for easy deployment
- **Kubernetes Compatible**: Deploy to any Kubernetes cluster
- **Configurable Settings**: Environment-based configuration for easy customization

## Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Docker and Docker Compose (for containerized deployment)
- RabbitMQ (for resilience testing and async operations)
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

# RabbitMQ Configuration
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_VHOST=/
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

# RabbitMQ Configuration
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_VHOST=/
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

# RabbitMQ Configuration
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_VHOST=/
```

### Docker Deployment

1. Build and run with Docker Compose (includes RabbitMQ):
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8542`
RabbitMQ management console will be available at `http://localhost:15672` (credentials: guest/guest)

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

Run the container with RabbitMQ:
```bash
docker run -p 8542:8542 \
  -e LLM_PROVIDER=docker \
  -e DOCKER_AI_API_URL=http://host.docker.internal:12434/engines/v1 \
  -e DOCKER_AI_API_KEY=docker \
  -e DOCKER_AI_MODEL=openai/ai/gpt-oss \
  -e RABBITMQ_HOST=host.docker.internal \
  -e RABBITMQ_PORT=5672 \
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
  "docker_key_present": true,
  "rabbitmq_connected": true
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

## Resilience Testing with TestCrew and RabbitMQ

The **TestCrew** module provides comprehensive resilience testing capabilities using RabbitMQ for message-driven async testing. This allows you to validate system behavior under various failure scenarios and load conditions.

### TestCrew Features

- **Async Message Processing**: Uses RabbitMQ queues for reliable message delivery
- **Failure Simulation**: Test system behavior under various failure modes
- **Load Testing**: Simulate high-volume message processing
- **Task Retry Logic**: Validate exponential backoff and retry mechanisms
- **Monitoring**: Real-time metrics and performance monitoring
- **Resilience Validation**: Ensure system recovers gracefully from failures

### Setup RabbitMQ

#### Using Docker Compose
RabbitMQ is automatically included in the docker-compose setup:

```bash
docker-compose up
```

#### Manual RabbitMQ Setup
```bash
# Run RabbitMQ container
docker run -d --name rabbitmq \
  -p 5672:5672 \
  -p 15672:15672 \
  rabbitmq:3-management

# Access management console at http://localhost:15672
# Default credentials: guest/guest
```

### Running Resilience Tests via API

#### Test Basic Content Generation with Message Queue

**Using curl:**
```bash
curl -X POST http://localhost:8542/test/run-content-test \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Quantum Computing Investments",
    "num_messages": 5,
    "test_timeout_seconds": 60
  }'
```

**Using Python requests:**
```python
import requests

response = requests.post(
    "http://localhost:8542/test/run-content-test",
    json={
        "topic": "Quantum Computing Investments",
        "num_messages": 5,
        "test_timeout_seconds": 60
    }
)

result = response.json()
print(f"Test Status: {result['status']}")
print(f"Messages Processed: {result['messages_processed']}")
print(f"Success Rate: {result['success_rate']}%")
```

**Response:**
```json
{
  "status": "completed",
  "topic": "Quantum Computing Investments",
  "total_messages": 5,
  "messages_processed": 5,
  "messages_failed": 0,
  "success_rate": 100.0,
  "average_processing_time_ms": 2345.67,
  "duration_seconds": 15.42,
  "queue_name": "test_content_queue_12345",
  "test_results": [
    {
      "message_id": "msg_1",
      "status": "success",
      "processing_time_ms": 2100.5
    }
  ]
}
```

#### Test Failure Resilience (Simulate Failures)

Test how the system handles and recovers from failures:

**Using curl:**
```bash
curl -X POST http://localhost:8542/test/resilience-test \
  -H "Content-Type: application/json" \
  -d '{
    "test_name": "failure_recovery_test",
    "num_messages": 10,
    "failure_rate": 0.3,
    "retry_attempts": 3,
    "test_timeout_seconds": 120
  }'
```

**Using Python requests:**
```python
import requests

response = requests.post(
    "http://localhost:8542/test/resilience-test",
    json={
        "test_name": "failure_recovery_test",
        "num_messages": 10,
        "failure_rate": 0.3,  # 30% of messages will fail initially
        "retry_attempts": 3,
        "test_timeout_seconds": 120
    }
)

result = response.json()
print(f"Test Name: {result['test_name']}")
print(f"Recovery Rate: {result['recovery_rate']}%")
print(f"Failed Messages Recovered: {result['recovered_count']}")
```

**Response:**
```json
{
  "test_name": "failure_recovery_test",
  "total_messages": 10,
  "initial_failures": 3,
  "recovered_count": 3,
  "permanent_failures": 0,
  "recovery_rate": 100.0,
  "retry_attempts_used": 2.5,
  "duration_seconds": 45.23,
  "status": "passed"
}
```

#### Load Testing with Multiple Concurrent Workers

**Using curl:**
```bash
curl -X POST http://localhost:8542/test/load-test \
  -H "Content-Type: application/json" \
  -d '{
    "num_messages": 100,
    "num_workers": 5,
    "test_timeout_seconds": 300
  }'
```

**Using Python requests:**
```python
import requests

response = requests.post(
    "http://localhost:8542/test/load-test",
    json={
        "num_messages": 100,
        "num_workers": 5,
        "test_timeout_seconds": 300
    }
)

result = response.json()
print(f"Throughput: {result['messages_per_second']:.2f} msgs/sec")
print(f"P95 Latency: {result['percentile_95_ms']:.2f} ms")
print(f"All Passed: {result['all_passed']}")
```

**Response:**
```json
{
  "test_type": "load_test",
  "total_messages": 100,
  "workers": 5,
  "messages_processed": 100,
  "messages_failed": 0,
  "success_rate": 100.0,
  "duration_seconds": 23.5,
  "messages_per_second": 4.26,
  "min_latency_ms": 1200.5,
  "max_latency_ms": 3450.8,
  "average_latency_ms": 2100.3,
  "percentile_50_ms": 2050.0,
  "percentile_95_ms": 3200.0,
  "percentile_99_ms": 3400.0,
  "all_passed": true
}
```

#### Get Test Results and Metrics

Retrieve historical test results and performance metrics:

**Using curl:**
```bash
curl http://localhost:8542/test/results
```

**Using curl with filtering:**
```bash
curl "http://localhost:8542/test/results?test_name=failure_recovery_test&limit=10"
```

**Response:**
```json
{
  "total_tests": 15,
  "results": [
    {
      "test_id": "test_12345",
      "test_name": "failure_recovery_test",
      "status": "passed",
      "timestamp": "2026-01-19T14:32:10Z",
      "success_rate": 100.0,
      "duration_seconds": 45.23
    }
  ]
}
```

### TestCrew Configuration

Configure TestCrew behavior via environment variables:

```env
# TestCrew Settings
TEST_RABBITMQ_QUEUE_PREFIX=test_crew_
TEST_MESSAGE_TTL_SECONDS=3600
TEST_TASK_TIMEOUT_SECONDS=600
TEST_MAX_RETRIES=3
TEST_RETRY_BACKOFF_SECONDS=5
TEST_RESULTS_PERSISTENCE=true
```

### Project Structure

```
investment-research-crew/
├── src/investment_research_crew/
│   ├── agents/          # Agent definitions (planner, writer, editor)
│   ├── crews/
│   │   ├── content_crew.py    # Content generation crew
│   │   └── test_crew.py       # Resilience testing crew
│   ├── tasks/           # Task definitions for agents
│   ├── tools/           # Custom tools and utilities
│   ├── rag/             # RAG (Retrieval Augmented Generation) components
│   ├── api.py           # FastAPI application and endpoints
│   ├── config.py        # Configuration and settings management
│   └── main.py          # Entry point for CLI and server startup
├── tests/               # Unit tests
├── Dockerfile           # Docker image definition
├── docker-compose.yml   # Docker Compose configuration (includes RabbitMQ)
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
| `RABBITMQ_HOST` | RabbitMQ host | `localhost` |
| `RABBITMQ_PORT` | RabbitMQ port | `5672` |
| `RABBITMQ_USER` | RabbitMQ username | `guest` |
| `RABBITMQ_PASSWORD` | RabbitMQ password | `guest` |
| `RABBITMQ_VHOST` | RabbitMQ virtual host | `/` |
| `TEST_RABBITMQ_QUEUE_PREFIX` | Prefix for test queues | `test_crew_` |
| `TEST_MESSAGE_TTL_SECONDS` | Message time-to-live | `3600` |
| `TEST_TASK_TIMEOUT_SECONDS` | Task timeout | `600` |
| `TEST_MAX_RETRIES` | Maximum retry attempts | `3` |

## Dependencies

Key dependencies:
- `crewai` - Multi-agent orchestration framework
- `crewai-tools` - Pre-built tools for agents
- `fastapi` - Modern web framework for building APIs
- `uvicorn` - ASGI server for FastAPI
- `pika` - RabbitMQ Python client
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

### RabbitMQ Management

Access the RabbitMQ management console:
```
URL: http://localhost:15672
Username: guest
Password: guest
```

Monitor queue depths, message rates, and consumer connections.

## Production Deployment Considerations

- **Environment Variables**: Use secrets management (Kubernetes Secrets, AWS Secrets Manager, etc.) for sensitive credentials
- **RabbitMQ Persistence**: Enable RabbitMQ persistence for message durability in production
- **Scaling**: Configure horizontal pod autoscaling in Kubernetes based on CPU/memory metrics
- **Load Balancing**: Use Ingress controllers or cloud load balancers for production traffic
- **Monitoring**: Integrate with Prometheus, Grafana, or cloud monitoring solutions for RabbitMQ and API metrics
- **Logging**: Configure structured logging and ship logs to centralized logging systems
- **Rate Limiting**: Implement API rate limiting to prevent abuse
- **RabbitMQ Clustering**: Deploy RabbitMQ in a clustered configuration for high availability
- **Message Replication**: Configure message replication for disaster recovery

## Kubernetes Deployment

### Basic Kubernetes Deployment with RabbitMQ

1. Create a Kubernetes deployment YAML (`k8s-deployment.yaml`):

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: llm-config
data:
  docker_ai_url: "http://docker-ai:12434/engines/v1"
---
apiVersion: v1
kind: Secret
metadata:
  name: llm-secrets
type: Opaque
stringData:
  docker_ai_key: "docker"
---
apiVersion: v1
kind: Service
metadata:
  name: rabbitmq-service
spec:
  ports:
  - port: 5672
    name: amqp
  - port: 15672
    name: management
  selector:
    app: rabbitmq
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: rabbitmq
spec:
  serviceName: rabbitmq-service
  replicas: 1
  selector:
    matchLabels:
      app: rabbitmq
  template:
    metadata:
      labels:
        app: rabbitmq
    spec:
      containers:
      - name: rabbitmq
        image: rabbitmq:3-management
        ports:
        - containerPort: 5672
          name: amqp
        - containerPort: 15672
          name: management
---
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
        - name: RABBITMQ_HOST
          value: "rabbitmq-service"
        - name: RABBITMQ_PORT
          value: "5672"
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

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Nihar Malali** - [GitHub](https://github.com/blitznihar)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.