from fastapi import FastAPI
from pydantic import BaseModel
from services.groq_llm import ask_groq
from services.evaluator import evaluate_answer
from services.interview_flow import InterviewSession
from services.code_executor import run_code


app = FastAPI()
current_interview: InterviewSession | None = None

class QuestionRequest(BaseModel):
    topic: str

class EvaluationRequest(BaseModel):
    question: str
    answer: str
class StartInterviewRequest(BaseModel):
    topic: str
    question_plan: list[str]  # ["TECH", "TECH", "CODING", "HR", "HR"]


class AnswerRequest(BaseModel):
    answer: str

CODING_PROBLEM = {
    "question": "Given an integer n, print n multiplied by 2.",
    "input": "5",
    "expected_output": "10"
}


@app.post("/start_interview")
def start_interview(data: StartInterviewRequest):
    global current_interview

    current_interview = InterviewSession(
        topic=data.topic,
        question_plan=data.question_plan
    )

    q_type = current_interview.get_current_question_type()

    if q_type == "TECH":
        prompt = (
            "You are a computer science technical interviewer.\n"
            f"Ask ONE interview question on {data.topic} related to DSA."
        )
        question = ask_groq(prompt)

    elif q_type == "HR":
        prompt = (
            "You are an HR interviewer.\n"
            "Ask ONE behavioral interview question."
        )
        question = ask_groq(prompt)

    elif q_type == "CODING":
        question = "CODING QUESTION PLACEHOLDER (compiler will be added later)"

    else:
        return {"error": "Invalid question type"}

    current_interview.questions.append(question)

    return {
        "message": "Interview started",
        "question_number": 1,
        "type": q_type,
        "question": question
    }

@app.post("/next_step")
def next_step(data: AnswerRequest):
    global current_interview

    if current_interview is None:
        return {"error": "No active interview"}

    q_type = current_interview.get_current_question_type()
    last_question = current_interview.questions[-1]

    # Evaluate based on type
    if q_type in ["TECH", "HR"]:
        evaluation = evaluate_answer(last_question, data.answer)
    elif q_type == "CODING":
        result = run_code(
        source_code=data.answer,
        language="python",
        stdin=CODING_PROBLEM["input"]
    )

        stdout = result.get("stdout")
        stderr = result.get("stderr")
        compile_output = result.get("compile_output")

        if stdout is not None:
            output = stdout.strip()
        elif stderr is not None:
            evaluation = f"Runtime Error: {stderr}"
        elif compile_output is not None:
            evaluation = f"Compilation Error: {compile_output}"
        else:
            evaluation = "No output produced."

        if stdout is not None and output == CODING_PROBLEM["expected_output"]:
            evaluation = "Code executed successfully and passed all test cases."


    current_interview.advance(last_question, evaluation)

    if current_interview.is_finished():
        summary = current_interview.get_summary()
        current_interview = None
        return {
            "message": "Interview completed",
            "summary": summary
        }

    # Ask next question
    next_type = current_interview.get_current_question_type()

    if next_type == "TECH":
        prompt = (
            "You are a computer science technical interviewer.\n"
            f"Ask ONE interview question on {current_interview.topic} related to DSA."
        )
        question = ask_groq(prompt)

    elif next_type == "HR":
        prompt = (
            "You are an HR interviewer.\n"
            "Ask ONE behavioral interview question."
        )
        question = ask_groq(prompt)

    elif next_type == "CODING":
        question = "CODING QUESTION PLACEHOLDER (compiler will be added later)"

    else:
        return {"error": "Invalid question type"}

    current_interview.questions.append(question)

    return {
        "question_number": current_interview.current_index + 1,
        "type": next_type,
        "question": question,
        "previous_evaluation": evaluation
    }



@app.post("/evaluate_answer")
def evaluate(data: EvaluationRequest):
    result = evaluate_answer(data.question, data.answer)
    return {"evaluation": result}
