from src.tools import gemini_llm_model_response
from langchain_core.prompts import PromptTemplate
from src.prompts.response_formatter import RESPONSE_FORMATTER_PROMPT
from src.services import clean_response_output

def response_agent_pipeline(main_question: str, db_input: any) -> str:
    db_data_context = ""

    if isinstance(db_input, dict) and "database_responses" in db_input:

        db_data_context += (
            "The Asker Agent broke down the main question into multiple "
            "sub-questions and executed SQL queries for each:\n\n"
        )

        for sub_question, response in db_input["database_responses"].items():

            if isinstance(response, tuple) and len(response) == 2:
                sql_response, sql_query = response

                if isinstance(sql_response, dict):
                    sql_result = sql_response.get("result")
                else:
                    sql_result = sql_response

                db_data_context += (
                    f"Sub-Question: {sub_question}\n"
                    f"SQL Query: {sql_query}\n"
                    f"SQL Result: {sql_result}\n\n"
                )
            else:
                db_data_context += (
                    f"Sub-Question: {sub_question}\n"
                    f"SQL Result: {response}\n\n"
                )

    elif isinstance(db_input, tuple) and len(db_input) == 2:

        sql_response, sql_query = db_input

        if isinstance(sql_response, dict):
            sql_result = sql_response.get("result")
        else:
            sql_result = sql_response

        db_data_context = (
            f"Direct SQL Query Executed: {sql_query}\n"
            f"Result Set: {sql_result}"
        )

    elif isinstance(db_input, dict) and any(k in db_input for k in ("result", "query")):

        db_data_context = (
            f"Direct SQL Query Executed: {db_input.get('query')}\n"
            f"Result Set: {db_input.get('result')}"
        )

    else:
        db_data_context = str(db_input)

    prompt = RESPONSE_FORMATTER_PROMPT.format(    main_question=main_question,db_data_context=db_data_context)

    response = gemini_llm_model_response(prompt)
    return clean_response_output(response)