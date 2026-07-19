from src.core import generate_sql_from_agents, select_schema
from src.services import execute_query
from config import models

def text_to_sql_pipeline(question, tables, selection_model=models.Qwen3, generator_model=models.QweQ):
    schema = select_schema(question, tables, model=selection_model)
    sql = generate_sql_from_agents(question, schema, True, model=generator_model)
    result = execute_query(sql)
    return result;