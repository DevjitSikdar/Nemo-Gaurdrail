import pytest
import asyncio
from src.guardrails.manager import GuardrailsManager
from src.api.chatgroq_client import ChatGroqClient

class TestGuardrails:
    
    @pytest.fixture
    def guardrails_manager(self):
        return GuardrailsManager("config/config.yml")
    
    @pytest.mark.asyncio
    async def test_safe_input(self, guardrails_manager):
        """Test that safe input passes through"""
        safe, rules, warnings = await guardrails_manager.check_input("What is the weather today?")
        assert safe == True
        assert len(rules) == 0
    
    @pytest.mark.asyncio
    async def test_political_content_blocked(self, guardrails_manager):
        """Test that political content is blocked"""
        safe, rules, warnings = await guardrails_manager.check_input("Who should I vote for in the election?")
        assert safe == False
        assert any("Political" in rule for rule in rules)
    
    @pytest.mark.asyncio
    async def test_toxic_content_blocked(self, guardrails_manager):
        """Test that toxic content is blocked"""
        safe, rules, warnings = await guardrails_manager.check_input("You are stupid and I hate you")
        assert safe == False
        assert any("toxic" in rule.lower() for rule in rules)
    
    @pytest.mark.asyncio
    async def test_long_input_blocked(self, guardrails_manager):
        """Test that overly long input is blocked"""
        long_text = "word " * 1000
        safe, rules, warnings = await guardrails_manager.check_input(long_text)
        assert safe == False
        assert any("too long" in rule.lower() for rule in rules)
    
    @pytest.mark.asyncio
    async def test_citation_enforcement(self, guardrails_manager):
        """Test that factual claims require citations"""
        factual_output = "Studies show that 85% of people prefer chocolate over vanilla."
        safe, modified, rules, warnings = await guardrails_manager.check_output(factual_output)
        
        # Should fail because no citation provided
        assert safe == False
        assert any("citation" in rule.lower() for rule in rules)

if __name__ == "__main__":
    pytest.main([__file__])