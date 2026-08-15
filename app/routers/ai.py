from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..ai_agent_service import ask_inventory_agent
from ..database import get_db
from ..inventory_services import generate_reorder_recommendations
from ..schemas import ChatRequest, ChatResponse, ReorderRecommendation

router = APIRouter(prefix="/ai", tags=["AI Assistant"])


@router.get("/recommendations", response_model=list[ReorderRecommendation])
def get_ai_recommendations(db: Session = Depends(get_db)):
    return generate_reorder_recommendations(db)


@router.post("/chat", response_model=ChatResponse)
def chat_with_agent(request: ChatRequest, db: Session = Depends(get_db)):
    answer = ask_inventory_agent(request.message, db)
    return {"answer": answer}