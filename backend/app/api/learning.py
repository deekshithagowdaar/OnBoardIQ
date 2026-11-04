from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.analytics.learning_engine import LearningEngine
from app.schemas.analytics import LearningAnalyticsResponse

router = APIRouter(prefix="/learning", tags=["Continuous Learning & Analytics"])

@router.get("/analytics", response_model=LearningAnalyticsResponse)
def get_learning_analytics(db: Session = Depends(get_db)):
    return LearningEngine.get_analytics(db)
