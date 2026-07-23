import re
from langgraph.graph import StateGraph, END
from src.workflows.state import AgentState
from src.agents import (rag_prof_pipeline, text_to_sql_pipeline, supervisor_pipeline, asker_pipeline, response_agent_pipeline)

def supervisor_node(state: AgentState) -> dict:
    steps = state.get("steps", [])

    supervisor_result = supervisor_pipeline(question=state["question"], model=state["supervisor_model"])
    
    intent = supervisor_result.get("intent", "OUT_OF_SCOPE").upper()

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
        "description": f"The question was analyzed and routed to: {next_agent}. Reason: {supervisor_result.get('reasoning', '')}",
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

    raw_result = text_to_sql_pipeline(
        question=state["question"],
        tables=state["tables"],
        generator_model=state["generator_query_model"],
        selection_model=state["selection_table_model"]
    )

    formatted_answer = response_agent_pipeline(
        main_question=state["question"], 
        db_input=raw_result
    )

    new_step = {
        "agent": "SQL Agent",
        "action": "Query Execution & Formatting",
        "description": "The requested live company data was retrieved and formatted professionally.",
    }

    return {"final_answer": formatted_answer, "steps": steps + [new_step]}

def asker_node(state: AgentState) -> dict:
    steps = state.get("steps", [])

    sub_questions_data = asker_pipeline(
        question=state["question"],
        vector_db=state["vector_db_path"],
        top_k=state["top_k"],
        model=state["asker_model"],
    )

    if isinstance(sub_questions_data, dict) and "sub_questions" in sub_questions_data:
        sub_questions = sub_questions_data["sub_questions"][:3]
    elif isinstance(sub_questions_data, list):
        sub_questions = sub_questions_data[:3]
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

    asker_bundle = {"database_responses": combined_db_results}

    formatted_answer = response_agent_pipeline(
        main_question=state["question"], 
        db_input=asker_bundle
    )

    new_step = {
        "agent": "Asker Agent",
        "action": "Deconstruction, Query & Formatting",
        "description": f"The complex question was decomposed into {len(sub_questions)} sub-questions, and the generated results were styled professionally.",
    }

    return {"final_answer": formatted_answer, "steps": steps + [new_step]}

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