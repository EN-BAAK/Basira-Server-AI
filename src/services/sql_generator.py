from config import models, client, settings
from src.prompts import build_schema_linking_prompt, build_sql_prompt, debug_sql_prompt, plan_sql_prompt, review_sql_prompt
from .sql_cleaner import clean_selection_tables, clean_sql_output

def llm_model_response(prompt, model=models.DeepSeek):
    tokens = settings.MAX_TOKENS if model == models.DeepSeek else 5000

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=tokens,
    )
    return response.choices[0].message.content.strip()

def llm_generate_sql(question, schema, plan, model=models.DeepSeek):
    prompt = build_sql_prompt(question, schema, plan)
    raw =  llm_model_response(prompt, model)

    return clean_sql_output(raw)

def llm_selection_schema(question, schema, model=models.DeepSeek):
    prompt = build_schema_linking_prompt(question, schema)
    response = llm_model_response(prompt, model)
    return clean_selection_tables(response)

def llm_review_sql(question, schema, sql, model=models.DeepSeek):
    prompt = review_sql_prompt(question, schema, sql)
    response = llm_model_response(prompt, model)

    return clean_sql_output(response)

def llm_debug_sql(question, schema, sql, error, model=models.DeepSeek):
    prompt = debug_sql_prompt(question, schema, sql, error)
    response = llm_model_response(prompt, model)

    return clean_sql_output(response)

def llm_plan_sql(question, schema, model=models.DeepSeek):
    prompt = plan_sql_prompt(question, schema)
    return llm_model_response(prompt, model)