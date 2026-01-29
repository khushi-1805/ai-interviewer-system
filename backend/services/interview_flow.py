class InterviewSession:
    def __init__(self, topic: str, question_plan: list[str]):
        self.topic = topic
        self.question_plan = question_plan  # e.g. ["TECH", "TECH", "CODING", "HR", "HR"]
        self.current_index = 0

        self.questions = []
        self.evaluations = []

    def is_finished(self) -> bool:
        return self.current_index >= len(self.question_plan)

    def get_current_question_type(self) -> str:
        return self.question_plan[self.current_index]

    def advance(self, question: str, evaluation: str):
        self.questions.append(question)
        self.evaluations.append(evaluation)
        self.current_index += 1

    def get_summary(self) -> str:
        summary = "Interview Summary:\n\n"
        for i, (q, e) in enumerate(zip(self.questions, self.evaluations), start=1):
            summary += f"{i}. Question: {q}\n"
            summary += f"   Evaluation: {e}\n\n"
        return summary
