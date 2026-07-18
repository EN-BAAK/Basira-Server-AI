from src.core import supervisor

def supervisor_pipeline(question, model):
    answer = supervisor(question, model)
    return answer