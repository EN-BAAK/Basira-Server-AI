from typing import TypedDict, List
from src.apis.schemas import AgentStep

class AgentState(TypedDict):
    conversation_id: str
    user_message: str
    company_id: str
    user_id: str
    steps: List[AgentStep]
    rag_context: str
    final_answer: str