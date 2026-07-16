from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from config import settings

app = FastAPI(
    title="Basira AI Backend",
    description="The Agentic AI Core for Basira Business Assistant",
    version=settings.VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.SERVER_SIDE],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    conversationId: str = Field(..., description="معرف جلسة المحادثة الفريد")
    message: str = Field(..., description="رسالة المستخدم المرسلة")
    companyId: str = Field(..., description="معرف الشركة لتحديد قاعدة البيانات الخاصة بها")
    userId: str = Field(..., description="معرف المستخدم الحالي")

class AgentStep(BaseModel):
    agent: str = Field(..., description="اسم الوكيل الذي تم استدعاؤه")
    action: str = Field(..., description="العملية التي قام بها الوكيل")
    description: str = Field(..., description="شرح تفصيلي للخطوة باللغة العربية")

class ChatResponseData(BaseModel):
    conversationId: str
    finalAnswer: str
    steps: List[AgentStep]
    metadata: dict = Field(default_factory=dict)

class ApiResponse(BaseModel):
    success: bool
    response: ChatResponseData


@app.get("/")
def read_root():
    return {
        "status": "healthy",
        "service": "Basira AI Engine",
        "environment": settings.ENV
    }


@app.post("/api/chat", response_model=ApiResponse)
async def handle_chat(request: ChatRequest):
    try:
        
        mock_steps = [
            AgentStep(
                agent="Supervisor",
                action="Planning",
                description="تم تحليل سؤالك وبناء خطة عمل لجمع البيانات وتحليلها."
            ),
            AgentStep(
                agent="SQL Agent",
                action="Query Execution",
                description="تم جلب بيانات المبيعات للربع الأخير من قاعدة بيانات متجرك بنجاح."
            ),
            AgentStep(
                agent="Analysis Agent",
                action="KPI Calculation",
                description="تم حساب المنتجات الأكثر مبيعاً ونسبة نمو الأرباح."
            ),
            AgentStep(
                agent="Response Agent",
                action="Generation",
                description="تم صياغة التوصيات النهائية بناءً على بياناتك حية."
            )
        ]
        
        mock_response_data = ChatResponseData(
            conversationId=request.conversationId,
            finalAnswer="أهلاً بك. مبيعاتك في الربع الأخير ممتازة، حيث حقق منتجك الأساسي نمواً بنسبة 12%. نوصي بزيادة مخزون هذا المنتج لتجنب نفاده في الشهر القادم.",
            steps=mock_steps,
            metadata={
                "executionTimeMs": 1200,
                "tokensUsed": 450,
                "model_used": settings.GEMINI_MODEL
            }
        )
        
        return ApiResponse(success=True, response=mock_response_data)
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail={"success": False, "response": {"errorCode": "SERVER_ERROR", "message": str(e)}}
        )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=(settings.ENV == "development")
    )