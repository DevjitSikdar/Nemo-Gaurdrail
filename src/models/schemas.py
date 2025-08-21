from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = {}

class ChatResponse(BaseModel):
    response: str
    is_safe: bool
    applied_rules: List[str] = []
    warnings: List[str] = []
    citations_required: bool = False
    processing_time: float
    timestamp: datetime

class GuardrailResult(BaseModel):
    is_allowed: bool
    reason: Optional[str] = None
    confidence_score: float
    rule_triggered: Optional[str] = None