from fastapi import APIRouter
from pydantic import BaseModel
from services.answer_evaluator import evaluate_answer

router = APIRouter()

class EvaluationRequest(BaseModel):
    question: str
    answer: str
    topic: str
    difficulty: str

@router.post("/evaluate_answer")
def evaluate(data: EvaluationRequest):
    return evaluate_answer(
        data.question,
        data.answer,
        data.topic,
        data.difficulty
    )
