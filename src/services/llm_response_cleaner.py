import re
import json

def clean_selection_tables(text: str):
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    text = text.strip()

    try:
        data = json.loads(text)

        if "tables" in data and "columns" in data:
            return data
        else:
            raise ValueError("Invalid schema format")

    except (json.JSONDecodeError, ValueError):
        return {
            "tables": [],
            "columns": {}
        }

def clean_sql_output(text: str) -> str:
    if not text:
        return ""

    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = re.sub(r"```sql", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)

    match = re.search(r"select .*", text, re.IGNORECASE | re.DOTALL)
    if match:
        text = match.group(0)
    else:
        return ""

    text = text.split(";")[0]

    text = re.sub(r"\s+", " ", text)

    text = text.strip()

    if not text.lower().startswith("select"):
        return ""

    return text

def clean_asker_output(text: str) -> dict:
    if not text:
        return {"sub_questions": []}

    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    
    text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)
    
    text = text.strip()

    try:
        data = json.loads(text)
        if "sub_questions" in data and isinstance(data["sub_questions"], list):
            return data
    except json.JSONDecodeError:
        pass

    json_match = re.search(r"\{.*\}", text, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group(0))
            if "sub_questions" in data and isinstance(data["sub_questions"], list):
                return data
        except json.JSONDecodeError:
            pass

    return {"sub_questions": []}

def clean_supervisor_output(text: str) -> dict:
    if not text:
        return {"intent": "OUT_OF_SCOPE", "reasoning": "Empty input"}
    
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)
    text = text.strip()
    
    try:
        data = json.loads(text)
        if "intent" in data:
            return data
    except json.JSONDecodeError:
        pass
        
    json_match = re.search(r"\{.*\}", text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass
            
    return {"intent": "OUT_OF_SCOPE", "reasoning": "Failed to parse supervisor output"}