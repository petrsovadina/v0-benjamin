from langchain_anthropic import ChatAnthropic
from backend.app.core.config import settings

def get_llm(model: str = "claude-3-haiku-20240307", temperature: float = 0.0):
    """
    Returns an instance of ChatAnthropic.
    """
    if not settings.ANTHROPIC_API_KEY:
        # Fallback for compilation/testing without keys
        return None
        
    return ChatAnthropic(
        model_name=model,
        api_key=settings.ANTHROPIC_API_KEY,
        temperature=temperature,
    )
