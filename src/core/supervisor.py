from src.prompts import SUPERVISOR_PROMPT
from src.tools import ghaumah_llm_model_response as llm_model_response
from src.services import clean_supervisor_output

def supervisor(question,model):
    prompt = SUPERVISOR_PROMPT.format(question)
    answer = llm_model_response(prompt, model)

    return clean_supervisor_output(answer)
