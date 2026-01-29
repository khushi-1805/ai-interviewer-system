import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EVALUATION_RUBRIC = """
You are a strict technical interviewer.

Evaluate the candidate answer using the following metrics.
Score each metric from 0 to 10.

Metrics:
1. Accuracy – correctness of concepts
2. Depth – level of understanding
3. Clarity – structured and clear explanation
4. Communication – articulation and flow
5. Examples – use of relevant examples

Rules:
- Be unbiased
- Do NOT be polite
- Penalize vague answers
- Reward precise technical explanations

Return ONLY valid JSON in this exact format:

{
  "accuracy": number,
  "depth": number,
  "clarity": number,
  "communication": number,
  "examples": number,
  "overall_score": number,
  "strengths": [string],
  "weaknesses": [string],
  "final_feedback": string
}
"""

def evaluate_answer(question: str, answer: str, topic: str, difficulty: str):
    prompt = f"""
{EVALUATION_RUBRIC}

Topic: {topic}
Difficulty: {difficulty}

Question:
{question}

Candidate Answer:
{answer}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    raw_output = response.choices[0].message["content"]

    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON returned by LLM",
            "raw_output": raw_output
        }
