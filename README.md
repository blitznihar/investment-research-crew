# Investment Research Crew

[![CI (lint + test)](https://github.com/blitznihar/investment-research-crew/actions/workflows/pylint.yml/badge.svg)](https://github.com/blitznihar/investment-research-crew/actions/workflows/pylint.yml)
[![codecov](https://codecov.io/github/blitznihar/investment-research-crew/graph/badge.svg?token=CxxB9Ew6Lx)](https://codecov.io/github/blitznihar/investment-research-crew)
![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![Last Commit](https://img.shields.io/github/last-commit/blitznihar/investment-research-crew)
![License](https://img.shields.io/github/license/blitznihar/investment-research-crew?cacheSeconds=0)
![CrewAI](https://img.shields.io/badge/CrewAI-000000?style=for-the-badge&logo=ai&logoColor=white)

## Overview

**Investment Research Crew** is an AI-powered multi-agent system built with [CrewAI](https://crewai.com/) that automates investment research report generation and analysis. The system uses specialized agents for content planning, writing, and editing to produce comprehensive, well-researched investment reports.

## Features

- **Content Planning Agent**: Researches and plans content structure with SEO optimization
- **Content Writing Agent**: Generates engaging, factually accurate investment analysis articles
- **Content Editing Agent**: Reviews and refines content for quality and consistency
- **Flexible LLM Support**: Works with OpenAI, local Docker AI, or LM Studio
- **Configurable Settings**: Environment-based configuration for easy customization

## Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- API key for your preferred LLM provider (OpenAI, Docker AI, or LM Studio)

## Installation

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
```

**For Docker AI (local):**
```env
LLM_PROVIDER=docker
DOCKER_AI_API_URL=http://localhost:12434/engines/v1
DOCKER_AI_API_KEY=docker
DOCKER_AI_MODEL=openai/gpt-oss
```

**For LM Studio (local):**
```env
LMSTUDIO_API_URL=http://127.0.0.1:1234/v1
LMSTUDIO_API_KEY=lm-studio
LMSTUDIO_MODEL=openai/gpt-oss-20b
```

## Usage

### Run the Investment Research Crew

Execute the following command to start the crew:

```bash
uv run investment-research-crew
```

This will:
1. Load your configuration from `.env`
2. Initialize the Content Planning, Writing, and Editing agents
3. Execute the crew workflow on a default topic (currently "Artificial Intelligence")
4. Output the generated investment research report

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

## Project Structure

```
investment-research-crew/
├── src/investment_research_crew/
│   ├── agents/          # Agent definitions (planner, writer, editor)
│   ├── crews/           # Crew orchestration logic
│   ├── tasks/           # Task definitions for agents
│   ├── tools/           # Custom tools and utilities
│   ├── rag/             # RAG (Retrieval Augmented Generation) components
│   ├── config.py        # Configuration and settings management
│   └── main.py          # Entry point
├── tests/               # Unit tests
├── pyproject.toml       # Project metadata and dependencies
└── README.md            # This file
```

## Configuration

Settings are managed through [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) and support both environment variables and `.env` file loading.

See [src/investment_research_crew/config.py](src/investment_research_crew/config.py) for detailed configuration options.

## Dependencies

Key dependencies:
- `crewai` - Multi-agent orchestration framework
- `crewai-tools` - Pre-built tools for agents
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

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Nihar Malali** - [GitHub](https://github.com/blitznihar)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
