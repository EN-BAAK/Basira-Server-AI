from src.prompts import build_schema_linking_prompt, build_sql_prompt, debug_sql_prompt, plan_sql_prompt, review_sql_prompt
from .llm_response_cleaner import clean_selection_tables, clean_sql_output
from src.tools import ghaumah_llm_model_response as llm_model_response

def llm_generate_sql(question, schema, plan, model):
    prompt = build_sql_prompt(question, schema, plan)
    raw =  llm_model_response(prompt, model)

    return clean_sql_output(raw)

def llm_selection_schema(question, schema, model):
    prompt = build_schema_linking_prompt(question, schema)
    response = llm_model_response(prompt, model)
    return clean_selection_tables(response)

def llm_review_sql(question, schema, sql, model):
    prompt = review_sql_prompt(question, schema, sql)
    response = llm_model_response(prompt, model)

    return clean_sql_output(response)

def llm_debug_sql(question, schema, sql, error, model):
    prompt = debug_sql_prompt(question, schema, sql, error)
    response = llm_model_response(prompt, model)

    return clean_sql_output(response)

def llm_plan_sql(question, schema, model):
    prompt = plan_sql_prompt(question, schema)
    return llm_model_response(prompt, model)