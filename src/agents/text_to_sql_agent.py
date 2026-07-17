from src.core import generate_sql_from_agents, select_schema
from src.services import execute_query
from config import models

def text_to_sql_pipeline(question, tables):
    schema = select_schema(question, tables, model=models.Qwen3)
    sql = generate_sql_from_agents(question, schema, True, model=models.Qwen3)
    result = execute_query(sql)
    return result;