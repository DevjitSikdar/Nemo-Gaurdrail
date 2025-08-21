import asyncio
import logging
from typing import Optional, Dict, Any
import os
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class ChatGroqClient:
    """Async client for ChatGroq API"""
    
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = AsyncGroq(api_key=self.api_key)
        self.model = "llama3-8b-8192"
    
    async def generate_response(
        self, 
        message: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate response using ChatGroq API"""
        try:
            # Prepare messages
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant. Provide accurate and helpful responses."
                },
                {
                    "role": "user", 
                    "content": message
                }
            ]
            
            # Add context if provided
            if context:
                context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
                messages[0]["content"] += f"\n\nContext: {context_str}"
            
            # Call ChatGroq API
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
                timeout=30.0
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"ChatGroq API error: {str(e)}")
            raise Exception(f"Failed to generate response: {str(e)}")
    
    async def health_check(self) -> bool:
        """Check if ChatGroq API is accessible"""
        try:
            await self.generate_response("Hello")
            return True
        except:
            return False