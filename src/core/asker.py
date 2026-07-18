import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from config import settings
from src.agents.rag_prof_agent import rag_prof_pipeline
from src.agents.text_to_sql_agent import text_to_sql_pipeline
from src.prompts.asker import QUESTION_BREAKER_PROMPT

def question_breaker_pipeline(question: str, pdfs_path: str, vector_db_path: str, tables: list) -> dict:
    """
    يحلل السؤال الأصلي بالاستعانة بالـ RAG، يفككه لـ 3 أسئلة فرعية كحد أقصى،
    ثم يمرر كل سؤال تلقائياً إلى الـ text_to_sql_pipeline ويعيد النتائج المجمعة.
    """
    
    business_context = rag_prof_pipeline(
        question=f"كيف يتم تحليل وتشخيص مشكلة: {question}",
        pdfs=pdfs_path,
        vector_db=vector_db_path
    )
    
    llm = ChatOpenAI(
        model=settings.OPENAI_MODEL, 
        openai_api_key=settings.OPENAI_API_KEY,
        temperature=0.0
    )
    
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=QUESTION_BREAKER_PROMPT
    )
    
    chain = prompt | llm
    ai_response = chain.invoke({"context": business_context, "question": question})
    
    sub_questions = []
    try:
        clean_content = ai_response.content.strip().replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_content)
        sub_questions = data.get("sub_questions", [])[:3]
    except Exception as e:
        print(f"[Warning] Failed to parse JSON from Question Breaker: {e}")
        sub_questions = [question]

    sql_results_summary = {}
    for sub_q in sub_questions:
        print(f"[Question Breaker] جاري إرسال السؤال الفرعي للـ SQL: {sub_q}")
        db_result = text_to_sql_pipeline(question=sub_q, tables=tables)
        sql_results_summary[sub_q] = db_result

    return {
        "original_question": question,
        "business_context_used": business_context,
        "sub_questions": sub_questions,
        "database_responses": sql_results_summary
    }