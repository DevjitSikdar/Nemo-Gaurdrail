from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)

class BaseGuardrail(ABC):
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = self.__class__.__name__
    
    @abstractmethod
    async def check_input(self, text: str) -> Tuple[bool, str, float]:
        pass
    
    @abstractmethod
    async def check_output(self, text: str) -> Tuple[bool, str, float]:
        pass
    
    def log_violation(self, text: str, reason: str):
        logger.warning(f"{self.name} violation: {reason}")