from src.workflows.graph import basira_workflow
from config import models

initial_state = {
    "question": "ماهي المنتجات التي لدي",
    "tables": "./data/tables.json",
    "pdfs_path": "./data/pdfs",
    "vector_db_path": "./data/vector",
    "asker_model": models.gamma,
    "selection_table_model": models.QweQ,
    "generator_query_model": models.QweQ,
    "supervisor_model": models.DeepSeek,
    "top_k": 3,
    "chunk_size": 500,
    "chunk_overlap": 50,
    "steps": []
}

final_output = basira_workflow.invoke(initial_state)