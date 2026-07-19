from langgraph.graph import StateGraph, END
from src.workflows.state import AgentState
from src.agents import rag_prof_pipeline, text_to_sql_pipeline, supervisor_pipeline, asker_pipeline

def parse_supervisor_intent(text: str) -> str:
    text = text.upper()
    if "RAG_ONLY" in text:
        return "RAG_ONLY"
    if "SQL_ONLY" in text:
        return "SQL_ONLY"
    if "MIXED_ASKER" in text:
        return "MIXED_ASKER"
    return "OUT_OF_SCOPE"

def supervisor_node(state: AgentState) -> dict:
    steps = state.get("steps", [])

    raw_answer = supervisor_pipeline(question=state["question"], model=state["supervisor_model"])
    intent = parse_supervisor_intent(raw_answer)

    final_answer = ""
    next_agent = intent

    if intent == "OUT_OF_SCOPE":
        final_answer = (
            "Sorry, I am a business assistant specialized only in questions related to companies, sales, and invoices."
        )
        next_agent = "END"

    new_step = {
        "agent": "Supervisor",
        "action": "Routing",
        "description": f"The question was analyzed and routed to: {next_agent}",
    }

    return {
        "next_agent": next_agent,
        "final_answer": final_answer,
        "steps": steps + [new_step],
    }

def rag_node(state: AgentState) -> dict:
    steps = state.get("steps", [])

    answer = rag_prof_pipeline(
        question=state["question"],
        pdfs=state["pdfs_path"],
        vector_db=state["vector_db_path"],
        top_k=state["top_k"],
        chunk_size=state["chunk_size"],
        chunk_overlap=state["chunk_overlap"],
    )

    new_step = {
        "agent": "RAG Agent",
        "action": "Knowledge Retrieval",
        "description": "The general knowledge answer was successfully retrieved from the business documentation.",
    }

    return {"final_answer": answer, "steps": steps + [new_step]}

def sql_node(state: AgentState) -> dict:
    steps = state.get("steps", [])

    result = text_to_sql_pipeline(
        question=state["question"],
        tables=state["tables"],
        generator_model=state["generator_query_model"],
        selection_model=state["selection_table_model"]
    )

    new_step = {
        "agent": "SQL Agent",
        "action": "Query Execution",
        "description": "The requested live company data and metrics were successfully retrieved from the database tables.",
    }

    return {"final_answer": result, "steps": steps + [new_step]}

def asker_node(state: AgentState) -> dict:
    steps = state.get("steps", [])

    sub_questions = asker_pipeline(
        question=state["question"],
        vector_db=state["vector_db_path"],
        top_k=state["top_k"],
        model=state["asker_model"],
    )

    if isinstance(sub_questions, list):
        sub_questions = sub_questions[:3]
    else:
        sub_questions = [state["question"]]

    combined_db_results = {}
    for sub_q in sub_questions:
        print(f"[Workflow Asker] Executing SQL for sub-question: {sub_q}")
        combined_db_results[sub_q] = text_to_sql_pipeline(
            question=sub_q,
            tables=state["tables"],
            generator_model=state["generator_query_model"],
            selection_model=state["selection_table_model"]
        )

    new_step = {
        "agent": "Asker Agent",
        "action": "Deconstruction & Query",
        "description": f"The complex question was decomposed into {len(sub_questions)} sub-questions, and their financial data was retrieved.",
    }

    return {"final_answer": combined_db_results, "steps": steps + [new_step]}

def route_next(state: AgentState) -> str:
    target = state.get("next_agent")
    if target == "RAG_ONLY":
        return "rag"
    if target == "SQL_ONLY":
        return "sql"
    if target == "MIXED_ASKER":
        return "asker"
    return "end"

workflow = StateGraph(AgentState)

workflow.add_node("supervisor", supervisor_node)
workflow.add_node("rag", rag_node)
workflow.add_node("sql", sql_node)
workflow.add_node("asker", asker_node)

workflow.set_entry_point("supervisor")

workflow.add_conditional_edges(
    "supervisor",
    route_next,
    {
        "rag": "rag",
        "sql": "sql",
        "asker": "asker",
        "end": END,
    },
)
workflow.add_edge("rag", END)
workflow.add_edge("sql", END)
workflow.add_edge("asker", END)

basira_workflow = workflow.compile()