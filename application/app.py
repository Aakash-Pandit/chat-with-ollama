import logging
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

import requests

from application.models.schemas import (
    HealthResponse,
    ChatRequest,
    ChatResponse,
)

logging.getLogger("onnxruntime").setLevel(logging.ERROR)

app = FastAPI(
    title="Research AI Agent API",
    description="API for Research AI Agent powered by LangGraph, Cohere, FAISS, and Tavily",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": "Chat With Ollama",
        "docs": "/docs",
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
    )


def ollama_request(prompt: str, stream: bool = False):
    ollama_url = os.getenv("OLLAMA_HOST", "http://ollama:11434")
    return requests.post(
        f"{ollama_url}/api/generate",
        json={"model": "phi3", "prompt": prompt, "stream": stream},
        stream=stream,
    )


def stream_llm(prompt: str):
    response = ollama_request(prompt, stream=True)
    for line in response.iter_lines():
        if line:
            yield line.decode() + "\n"


@app.post("/stream")
def stream(request: ChatRequest):
    return StreamingResponse(stream_llm(request.query), media_type="text/plain")


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = ollama_request(request.query)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return ChatResponse(query=request.query, answer=response.json()["response"])
