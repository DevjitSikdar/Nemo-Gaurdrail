from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

import os
from fastapi import FastAPI, HTTPException
from src.api.chatgroq_client import ChatGroqClient
from src.guardrails.manager import GuardrailsManager
from src.models.schemas import ChatRequest, ChatResponse

from contextlib import asynccontextmanager
from datetime import datetime
import asyncio
import platform

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    yield
    # Shutdown logic

app = FastAPI(lifespan=lifespan)

# Initialize ChatGroqClient and GuardrailsManager
chat_client = ChatGroqClient()
guardrails = GuardrailsManager(config_path="config/config.yml")

app.mount("/static", StaticFiles(directory="src/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("src/static/index.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/health")
async def health_check():
    api_status = await chat_client.health_check()
    return {"api_status": api_status}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Check input against guardrails
    safe_input, rules, warnings = await guardrails.check_input(request.message)

    if not safe_input:
        return ChatResponse(
            response="Your input was blocked by guardrails.",
            is_safe=False,
            applied_rules=rules,
            warnings=warnings,
            processing_time=0.0,
            timestamp=datetime.now()
        )

    # Generate response from ChatGroq
    response_text = await chat_client.generate_response(request.message)

    # Check output against guardrails
    safe_output, modified_output, rules, warnings = await guardrails.check_output(response_text)

    if not safe_output:
        return ChatResponse(
            response=modified_output,
            is_safe=False,
            applied_rules=rules,
            warnings=warnings,
            processing_time=0.0,
            timestamp=datetime.now()
        )

    return ChatResponse(
        response=modified_output,
        is_safe=True,
        applied_rules=rules,
        warnings=warnings,
        processing_time=0.0,
        timestamp=datetime.now()
    )