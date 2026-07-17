from src.services import get_schema, llm_selection_schema, build_schema_from_llm, llm_generate_sql, llm_plan_sql, llm_review_sql
from config import models

def select_schema(question, tables, model=models.DeepSeek):
    db_schema = get_schema(tables_file=tables)
    selected = llm_selection_schema(question, db_schema, model)
    return build_schema_from_llm(selected)

def generate_sql_from_agents(question, schema, reviewer=False, model=models.DeepSeek):
    plan = llm_plan_sql(question, schema, model)
    sql = llm_generate_sql(question, schema, plan, model)

    if reviewer:
        for _ in range(1):
            new_sql = llm_review_sql(question, schema, sql, model)
            if not new_sql or new_sql == sql:
                break
            sql = new_sql

    return sql