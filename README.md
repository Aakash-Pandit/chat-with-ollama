# Chat with Ollama

A lightweight REST API that lets you chat with a locally running LLM (phi3) using [Ollama](https://ollama.com), wrapped in a FastAPI service and fully containerized with Docker.

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

## How Ollama Works

[Ollama](https://ollama.com) is a tool that runs open-source LLMs locally. It:

1. Downloads and manages model weights on your machine
2. Exposes a local HTTP API at `http://localhost:11434`
3. Handles inference — you send a prompt, it returns a response

Models are stored in a Docker volume and only downloaded once.

---

## How We Use Ollama in This Project

```
User Request
     │
     ▼
FastAPI (/chat or /stream)
     │
     ▼
ollama_request() → POST http://ollama:11434/api/generate
     │
     ▼
Ollama container (phi3 model)
     │
     ▼
Response returned to user
```

- `/chat` — returns the full response once generation is complete
- `/stream` — streams tokens back to the client in real-time as they are generated

The `ollama-init` service automatically pulls the `phi3` model on first startup so you don't have to do it manually.

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

The default `.env` should contain:

```env
OLLAMA_HOST=http://ollama:11434
```

### 3. Build the project

```bash
make build
```

### 4. Start the project

```bash
make start
```

On first run, the `ollama-init` service will automatically pull the `phi3` model (~2.2 GB). Subsequent starts skip the download as the model is cached in a Docker volume.

### 5. Verify it's running

```bash
curl http://localhost:8000/health
# {"status":"healthy"}
```

---

## API Endpoints

### `POST /chat`
Returns the full response after generation completes.

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
Streams tokens in real-time as the model generates them.

**Request:**
```json
{"query": "Tell me a joke"}
```

**Response:** newline-delimited JSON chunks
```json
{"model":"phi3","response":"Why","done":false}
{"model":"phi3","response":" don't","done":false}
...
{"model":"phi3","response":"","done":true}
```

---

## Makefile Commands

| Command | Description |
|---------|-------------|
| `make build` | Build the Docker image |
| `make start` | Start all services |
| `make stop` | Stop all services |
| `make remove` | Stop and remove containers and volumes |
| `make rebuild` | Stop, rebuild, and restart |

---

## Interactive API Docs

Once running, visit [http://localhost:8000/docs](http://localhost:8000/docs) for the Swagger UI.
