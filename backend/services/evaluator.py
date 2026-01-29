from services.groq_llm import ask_groq

def evaluate_answer(question: str, answer: str) -> str:
    prompt = (
        "You are a computer science interviewer.\n\n"
        f"Question: {question}\n"
        f"Candidate Answer: {answer}\n\n"
        "Evaluate the answer.\n"
        "State clearly:\n"
        "- Whether the answer is correct or partially correct\n"
        "- What is missing or can be improved\n\n"
        "Rules:\n"
        "- Do NOT use markdown\n"
        "- Do NOT ask a follow-up question\n"
        "- Keep the response concise and professional"
    )

    return ask_groq(prompt)
