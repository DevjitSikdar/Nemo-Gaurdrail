import re
from typing import Dict, Any, Tuple, List
from .base import BaseGuardrail

class CitationEnforcerGuardrail(BaseGuardrail):
    """Enforces citations for factual claims"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.citation_required = config.get('citation_required', True)
        
        # Patterns that likely need citations
        self.factual_patterns = [
            r'\b\d{4}\b.*\b(year|data|study|research)\b',  # Years with data/study
            r'\b(according to|studies show|research indicates)\b',
            r'\b\d+(\.\d+)?%\b',  # Percentages
            r'\b(statistics|survey|poll)\b.*\b(show|indicate|reveal)\b'
        ]
    
    async def check_input(self, text: str) -> Tuple[bool, str, float]:
        # Citations not required for input
        return True, "", 0.0
    
    async def check_output(self, text: str) -> Tuple[bool, str, float]:
        if not self.citation_required:
            return True, "", 0.0
        
        needs_citation = self._needs_citation(text)
        has_citation = self._has_citation(text)
        
        if needs_citation and not has_citation:
            return False, "Response contains factual claims that require citations", 0.8
        
        return True, "", 0.0
    
    def _needs_citation(self, text: str) -> bool:
        """Check if text contains claims that need citations"""
        return any(re.search(pattern, text.lower()) for pattern in self.factual_patterns)
    
    def _has_citation(self, text: str) -> bool:
        """Check if text contains citations"""
        citation_patterns = [
            r'\[.*\]',  # [Source]
            r'\(.*\d{4}.*\)',  # (Author 2023)
            r'source:',  # Source: ...
            r'according to.*:'  # According to X:
        ]
        return any(re.search(pattern, text.lower()) for pattern in citation_patterns)