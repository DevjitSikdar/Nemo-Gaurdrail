import re
from typing import Dict, Any, Tuple, List
from .base import BaseGuardrail

class TopicRestrictionGuardrail(BaseGuardrail):
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.blocked_topics = config.get('blocked_topics', [])
        self.political_keywords = [
            'election', 'voting', 'democrat', 'republican', 
            'biden', 'trump', 'congress', 'senate', 'political party'
        ]
        self.illegal_keywords = [
            'drugs', 'weapons', 'hacking', 'piracy', 'fraud'
        ]
    
    async def check_input(self, text: str) -> Tuple[bool, str, float]:
        text_lower = text.lower()
        
        if self._contains_political_content(text_lower):
            return False, "Political discussions are not allowed", 0.9
        
        if self._contains_illegal_content(text_lower):
            return False, "Discussions about illegal activities are not allowed", 0.95
            
        return True, "", 0.0
    
    async def check_output(self, text: str) -> Tuple[bool, str, float]:
        return await self.check_input(text)
    
    def _contains_political_content(self, text: str) -> bool:
        return any(keyword in text for keyword in self.political_keywords)
    
    def _contains_illegal_content(self, text: str) -> bool:
        return any(keyword in text for keyword in self.illegal_keywords)