# Chat with Ollama

A lightweight REST API to chat with a locally running LLM using [Ollama](https://ollama.com), built with FastAPI and fully containerized with Docker.

---

## What is this?

This project provides a simple HTTP API to interact with a large language model running entirely on your machine — no external API keys, no cloud calls, no usage costs. Everything runs locally inside Docker containers.

---

## Use Cases

- **Private AI assistant** — run an LLM locally without sending data to any third-party service
- **Prototyping** — quickly build and test LLM-powered features against a local model
- **Offline usage** — works without an internet connection once the model is pulled
- **Learning** — understand how to integrate Ollama into a Python backend

---

## Architecture

```
User Request
     │
     ▼
FastAPI (/chat or /stream)
     │
     ▼
httpx async client → POST http://ollama:11434/api/generate
     │
     ▼
Ollama container (phi3 model)
     │
     ▼
Response streamed or returned to user
```

- `/chat` — waits for full generation, returns complete response as JSON
- `/stream` — streams plain text tokens back to the client in real-time as they are generated

The `ollama-init` service automatically pulls the `phi3` model on first startup.

---

## Tech Stack

| Layer | Technology |
|---|---|
| API framework | FastAPI |
| HTTP client | httpx (async) |
| LLM runtime | Ollama |
| Model | phi3 (swappable via `OLLAMA_MODEL` env var) |
| Containerization | Docker + Docker Compose |
| Data validation | Pydantic v2 |

---

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop) installed and running
- [Docker Compose](https://docs.docker.com/compose/) (included with Docker Desktop)

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/chat-with-ollama.git
cd chat-with-ollama
```

### 2. Create a `.env` file

```bash
cp .env.example .env
```

Default `.env` values:

```env
API_PORT=8000
OLLAMA_HOST=http://ollama:11434
```

### 3. Build and start

```bash
make build
make start
```

On first run, `ollama-init` automatically pulls the `phi3` model (~2.2 GB). Subsequent starts skip the download as the model is cached in a Docker volume.

### 4. Verify it's running

```bash
curl http://localhost:8000/health
# {"status":"healthy"}
```

---

## API Endpoints

### `GET /health`
Returns service health status.

**Response:**
```json
{"status": "healthy"}
```

---

### `POST /chat`
Sends a prompt and returns the full response once generation is complete.

**Request:**
```json
{"query": "What is the capital of France?"}
```

**Response:**
```json
{
  "query": "What is the capital of France?",
  "answer": "The capital of France is Paris."
}
```

---

### `POST /stream`
Streams plain text tokens in real-time as the model generates them.

**Request:**
```json
{"query": "Tell me a joke"}
```

**Response:** plain text, tokens arriving incrementally
```
Why don't scientists trust atoms?
Because they make up everything!
```

**Test with curl:**
```bash
curl -X POST http://localhost:8000/stream \
  -H "Content-Type: application/json" \
  -d '{"query": "tell me about space"}' \
  --no-buffer
```

> Note: Swagger UI (`/docs`) and Postman will display the full response after generation completes — they do not show tokens arriving one by one. Use `curl` or a frontend with `fetch` + `ReadableStream` to observe real-time streaming.

---

## Makefile Commands

| Command | Description |
|---|---|
| `make build` | Build the Docker image |
| `make start` | Start all services |
| `make stop` | Stop all services |
| `make remove` | Stop and remove containers and volumes |
| `make rebuild` | Stop, rebuild, and restart |
| `make test` | Run tests inside the container |

---

## Project Structure

```
chat-with-ollama/
├── application/
│   ├── app.py               # FastAPI app, route handlers
│   └── models/
│       └── schemas.py       # Pydantic request/response schemas
├── compose/
│   └── Dockerfile           # Container definition
├── docker-compose.yml       # Service orchestration
├── main.py                  # Uvicorn entry point
├── Makefile                 # Common dev commands
├── requirements.txt         # Python dependencies
└── .env.example             # Environment variable template
```

---

## Swapping the Model

To use a different Ollama model (e.g. `qwen2.5-coder:7b` for code tasks):

1. Update `docker-compose.yml` to pull the new model:
```yaml
entrypoint: ["ollama", "pull", "qwen2.5-coder:7b"]
```

2. Set the model via environment variable in `.env`:
```env
OLLAMA_MODEL=qwen2.5-coder:7b
```

Popular alternatives:

| Model | Size | Good for |
|---|---|---|
| `phi3` | ~2.3 GB | General chat (default) |
| `qwen2.5-coder:7b` | ~4.7 GB | Code review, code generation |
| `deepseek-coder:6.7b` | ~3.8 GB | Bug detection, security review |
| `codellama:7b` | ~3.8 GB | General code tasks |

---

## Interactive API Docs

Once running, visit [http://localhost:8000/docs](http://localhost:8000/docs) for the Swagger UI.
