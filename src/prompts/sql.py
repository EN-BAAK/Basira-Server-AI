import json

def build_sql_prompt(question, schema, plan=""):
    return f"""
        You are an expert PostgreSQL SQL engineer.
        
        Database: PostgreSQL

        Question:
        {question}

        Schema:
        {schema}

        Plan:
        {plan}

        Generate the SQL query based on the plan.

        Rules:
        - Follow the plan strictly
        - Use correct tables and columns
        - Output ONLY SQL
        - Single line only
        - PostgreSQL Specific Case-Sensitivity Rule: PostgreSQL converts unquoted identifiers to lowercase. Therefore, any table or column name containing uppercase letters (e.g., camelCase like "productId" or "colorId") MUST be enclosed in double quotes (e.g., product_colors."productId"), (e.g. 2, products."imgUrl"). Never lowercase them.

        SQL:
        """

def build_schema_linking_prompt(question, schema):
    return f"""
        You are a database expert.
    
        Your task is to select ONLY the necessary tables and columns needed to answer the question.

        Database schema:
        {json.dumps(schema, indent=2)}

        Question:
        {question}?

        Your response format (STRICT JSON) should be:
        {{
        "tables": ["table1", "table2"],
        "columns": {{
            "table1": [
            {{ "type": "col1 type", "column": "col1 name", "isPrimary": col1 is_primary }},
            {{ "type": "col2 type", "column": "col2 name", "isPrimary": col2 is_primary }}
            ],
            "table2": [
            {{ "type": "col1 type", "column": "col1 name", "isPrimary": col1 is_primary }}
            ]
        }} }}

        Rules:
        - Select only the tables required to answer the question.
        - Select only the columns required to answer the question.
        - Never return an empty result if the requested table exists in the schema.
        - Do Not include explanations after selection.
        - Do NOT include any text before or after the JSON.
        - Do NOT include markdown.
        - Do not invent tables or columns that are not present in the schema.
        - Output ONLY valid JSON.
        - Do not return a query.
    """

def review_sql_prompt(question, schema, sql):
    return f"""
        You are an expert SQL reviewer.

        Your task is to verify whether the SQL query correctly answers the question.

        Question:
        {question}

        Schema:
        {schema}

        SQL:
        {sql}

        Instructions:
        - If the SQL is correct, return it unchanged
        - If the SQL is incorrect, fix it
        - Ensure correct columns and tables
        - Ensure proper JOINs if needed
        - Do NOT explain anything
        - Output ONLY the SQL query
        - Output must be in a single line

        SQL:
        """

def debug_sql_prompt(question, schema, sql, error):
    return f"""
        You are a SQL debugging expert.

        The following SQL query failed during execution.

        Question:
        {question}

        Schema:
        {schema}

        SQL:
        {sql}

        Error:
        {error}

        Your task:
        - Fix the SQL query based on the error
        - Ensure it answers the question correctly
        - Do NOT explain anything
        - Output ONLY the corrected SQL
        - Output must be in a single line

        SQL:
        """

def plan_sql_prompt(question, schema):
    return f"""
        You are a SQL query planner.

        Your task is to analyze the question and create a structured plan for the SQL query.

        Question:
        {question}

        Schema:
        {schema}

        Create a plan with the following format:

        Tables: ...
        Columns: ...
        Conditions: ...
        Aggregation: ...
        Grouping: ...
        Ordering: ...

        Rules:
        - Be concise
        - Only include necessary elements
        - Do NOT write SQL
        - Do NOT explain

        Plan:
        """