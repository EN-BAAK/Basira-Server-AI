from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    question: str
    tables: List[str]
    pdfs_path: str
    vector_db_path: str
    asker_model: Any
    selection_table_model: Any
    generator_query_model: Any
    supervisor_model: Any
    
    top_k: int
    chunk_size: int
    chunk_overlap: int

    next_agent: str
    final_answer: Any
    steps: List[Dict[str, str]]