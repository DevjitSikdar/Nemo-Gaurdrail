import asyncio
import logging
from typing import List, Dict, Any, Tuple
import yaml
from .topic_filter import TopicRestrictionGuardrail
from .toxicity_filter import ToxicityFilterGuardrail
from .length_control import LengthControlGuardrail
from .citation_enforcer import CitationEnforcerGuardrail

logger = logging.getLogger(__name__)

class GuardrailsManager:
    """Manages and orchestrates all guardrails"""
    
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.input_guardrails = []
        self.output_guardrails = []
        self._initialize_guardrails()
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    
    def _initialize_guardrails(self):
        """Initialize all guardrails based on config"""
        guardrail_classes = {
            'topic_filter': TopicRestrictionGuardrail,
            'toxicity_filter': ToxicityFilterGuardrail,
            'length_control': LengthControlGuardrail,
            'citation_enforcer': CitationEnforcerGuardrail
        }
        
        # Initialize input guardrails
        for guardrail_name in ['topic_filter', 'toxicity_filter', 'length_control']:
            guardrail_class = guardrail_classes[guardrail_name]
            self.input_guardrails.append(guardrail_class(self.config))
        
        # Initialize output guardrails
        for guardrail_name in ['toxicity_filter', 'citation_enforcer', 'length_control']:
            guardrail_class = guardrail_classes[guardrail_name]
            self.output_guardrails.append(guardrail_class(self.config))
    
    async def check_input(self, text: str) -> Tuple[bool, List[str], List[str]]:
        """
        Run all input guardrails
        Returns: (is_safe, applied_rules, warnings)
        """
        applied_rules = []
        warnings = []
        
        for guardrail in self.input_guardrails:
            try:
                is_safe, reason, confidence = await guardrail.check_input(text)
                
                if not is_safe:
                    applied_rules.append(f"{guardrail.name}: {reason}")
                    return False, applied_rules, warnings
                
                if reason:  # Warning but not blocking
                    warnings.append(f"{guardrail.name}: {reason}")
                
            except Exception as e:
                logger.error(f"Error in {guardrail.name}: {str(e)}")
                warnings.append(f"{guardrail.name}: Processing error")
        
        return True, applied_rules, warnings
    
    async def check_output(self, text: str) -> Tuple[bool, str, List[str], List[str]]:
        """
        Run all output guardrails
        Returns: (is_safe, modified_text, applied_rules, warnings)
        """
        modified_text = text
        applied_rules = []
        warnings = []
        
        for guardrail in self.output_guardrails:
            try:
                is_safe, reason, confidence = await guardrail.check_output(modified_text)
                
                if not is_safe:
                    if "truncated" in reason.lower():
                        # Handle truncation
                        modified_text = modified_text[:self.config.get('limits', {}).get('max_response_length', 500)] + "..."
                        warnings.append(f"{guardrail.name}: {reason}")
                    applied_rules.append(f"{guardrail.name}: {reason}")
                    return False, modified_text, applied_rules, warnings
                
                if reason:  # Warning but not blocking
                    warnings.append(f"{guardrail.name}: {reason}")
                
            except Exception as e:
                logger.error(f"Error in {guardrail.name}: {str(e)}")
                warnings.append(f"{guardrail.name}: Processing error")
        
        return True, modified_text, applied_rules, warnings