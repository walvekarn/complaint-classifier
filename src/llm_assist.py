"""
LLM-assisted classification (optional enhancement).
Author: Nikita Walvekar (walvekarn)

This module provides optional LLM-powered classification to enhance
the rule-based baseline. Requires API keys set as environment variables.
Falls back gracefully if keys are not present.
"""

import os
import logging
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def classify_with_llm(
    text: str,
    provider: str = "openai"
) -> Optional[Dict[str, Any]]:
    """
    Classify complaint using LLM provider (OpenAI, Anthropic, etc.).
    
    This is a safe stub that checks for API keys and falls back gracefully.
    
    Args:
        text: The complaint text to classify
        provider: LLM provider ("openai", "anthropic", "azure")
        
    Returns:
        Classification result dict if successful, None if LLM unavailable
        
    Environment Variables Required:
        - OPENAI_API_KEY: For OpenAI provider
        - ANTHROPIC_API_KEY: For Anthropic provider
        - AZURE_OPENAI_KEY + AZURE_OPENAI_ENDPOINT: For Azure
        
    Example:
        >>> result = classify_with_llm("Fraud on my credit card", provider="openai")
        >>> if result:
        ...     print(f"LLM Classification: {result}")
        ... else:
        ...     print("LLM unavailable, using rule-based fallback")
    """
    
    if not text or not text.strip():
        logger.warning("Empty text provided to LLM classifier")
        return None
    
    # Check for API keys based on provider
    api_key = None
    
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.info("OPENAI_API_KEY not set. LLM-assisted classification disabled. "
                       "Using rule-based classifier.")
            return None
            
    elif provider == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            logger.info("ANTHROPIC_API_KEY not set. LLM-assisted classification disabled. "
                       "Using rule-based classifier.")
            return None
            
    elif provider == "azure":
        api_key = os.getenv("AZURE_OPENAI_KEY")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        if not api_key or not endpoint:
            logger.info("Azure OpenAI credentials not set. LLM-assisted classification disabled. "
                       "Using rule-based classifier.")
            return None
    else:
        logger.warning(f"Unknown provider: {provider}. Supported: openai, anthropic, azure")
        return None
    
    # At this point, API key exists but we don't actually call the LLM
    # This is a safe stub for portfolio demonstration
    logger.info(f"LLM assist available with provider: {provider}")
    logger.info("Note: This is a stub implementation. Actual LLM calls would be made here.")
    
    # In a production implementation, you would:
    # 1. Import the provider SDK (openai, anthropic, etc.)
    # 2. Make the API call with proper error handling
    # 3. Parse and return the structured result
    #
    # Example pseudo-code:
    # try:
    #     if provider == "openai":
    #         import openai
    #         response = openai.ChatCompletion.create(...)
    #         return parse_response(response)
    # except Exception as e:
    #     logger.error(f"LLM API call failed: {e}")
    #     return None
    
    return None


def get_llm_status() -> Dict[str, bool]:
    """
    Check which LLM providers are configured.
    
    Returns:
        Dictionary with provider availability status
    """
    return {
        "openai": bool(os.getenv("OPENAI_API_KEY")),
        "anthropic": bool(os.getenv("ANTHROPIC_API_KEY")),
        "azure": bool(os.getenv("AZURE_OPENAI_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"))
    }


def validate_llm_config(provider: str) -> bool:
    """
    Validate that the required environment variables are set for a provider.
    
    Args:
        provider: LLM provider name
        
    Returns:
        True if provider is properly configured
    """
    status = get_llm_status()
    return status.get(provider, False)


# Example usage demonstrating safe fallback pattern
if __name__ == "__main__":
    print("LLM Assist Configuration Check")
    print("=" * 50)
    
    status = get_llm_status()
    for provider, available in status.items():
        symbol = "✓" if available else "✗"
        print(f"{symbol} {provider.capitalize()}: {'Available' if available else 'Not configured'}")
    
    print("\nExample Usage:")
    print("-" * 50)
    
    sample_text = "I found unauthorized charges on my credit card!"
    
    result = classify_with_llm(sample_text, provider="openai")
    
    if result:
        print(f"LLM Classification: {result}")
    else:
        print("LLM unavailable → Falling back to rule-based classification")
        # In actual use, you would call the rule-based classifier here
        from src.classifier import classify_complaint
        baseline_result = classify_complaint(sample_text)
        print(f"Rule-based Classification: {baseline_result}")

