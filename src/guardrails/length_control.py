from typing import Dict, Any, Tuple
from .base import BaseGuardrail

class LengthControlGuardrail(BaseGuardrail):
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        limits = config.get('limits', {})
        self.max_input_length = 100
        self.max_output_length = limits.get('max_response_length', 500)
    
    async def check_input(self, text: str) -> Tuple[bool, str, float]:
        if len(text) > self.max_input_length:
            return False, f"Input too long ({len(text)} > {self.max_input_length})", 1.0
        return True, "", 0.0
    
    async def check_output(self, text: str) -> Tuple[bool, str, float]:
        if len(text) > self.max_output_length:
            truncated = text[:self.max_output_length] + "..."
            return True, f"Response truncated to {self.max_output_length} characters", 0.5
        return True, "", 0.0