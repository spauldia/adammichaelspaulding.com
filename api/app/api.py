"""HTTP routes for the chat API."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.dependencies import get_chat_orchestrator
from app.models import ChatRequest, ChatResponse, HealthResponse
from app.orchestrators.chat_orchestrator import ChatOrchestrator

UNKNOWN_CLIENT_IP = "unknown"

router = APIRouter()


@router.get("/health")
def health() -> HealthResponse:
    return HealthResponse()


@router.post("/chat")
def chat(
    body: ChatRequest,
    request: Request,
    orchestrator: Annotated[ChatOrchestrator, Depends(get_chat_orchestrator)],
) -> ChatResponse:
    client_ip = request.client.host if request.client else UNKNOWN_CLIENT_IP
    return orchestrator.answer(body, client_ip)
