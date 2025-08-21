import re
from typing import Dict, Any, Tuple
from .base import BaseGuardrail

class ToxicityFilterGuardrail(BaseGuardrail):
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.input_threshold = config.get('toxicity', {}).get('input_threshold', 0.7)
        self.output_threshold = config.get('toxicity', {}).get('output_threshold', 0.6)
        
        self.toxic_patterns = [
            r'\b(hate|stupid|idiot|moron)\b',
            r'\b(kill|die|death)\b.*\b(you|yourself)\b',
            r'\b(f\*\*k|sh\*t|damn)\b.*\b(you|off)\b'
        ]
    
    async def check_input(self, text: str) -> Tuple[bool, str, float]:
        toxicity_score = self._calculate_toxicity(text)
        
        if toxicity_score > self.input_threshold:
            return False, f"Input contains toxic content (score: {toxicity_score:.2f})", toxicity_score
        
        return True, "", toxicity_score
    
    async def check_output(self, text: str) -> Tuple[bool, str, float]:
        toxicity_score = self._calculate_toxicity(text)
        
        if toxicity_score > self.output_threshold:
            return False, f"Output contains toxic content (score: {toxicity_score:.2f})", toxicity_score
        
        return True, "", toxicity_score
    
    def _calculate_toxicity(self, text: str) -> float:
        text_lower = text.lower()
        matches = 0
        
        for pattern in self.toxic_patterns:
            if re.search(pattern, text_lower):
                matches += 1
        
        return min(matches * 0.3, 1.0)