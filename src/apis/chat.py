from src.workflows.graph import basira_workflow

initial_state = {
    "question": "لماذا أرباحي انخفضت؟",
    "tables": ["sales", "expenses"],
    "pdfs_path": "../data/pdfs",
    "vector_db_path": "../data/vector",
    "model": models.Qwen3,
    "top_k": 3,
    "chunk_size": 500,
    "chunk_overlap": 50,
    "steps": []
}

final_output = basira_workflow.invoke(initial_state)

print(final_output["final_answer"])
print(final_output["steps"])