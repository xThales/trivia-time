from trivia_time.game.question import Question


class QuizSession:
    def __init__(self, questions: tuple[Question, ...]) -> None:
        if not questions:
            raise ValueError("No questions provided")

        self.questions = questions
        self.current_question_index = 0
        self.score = 0
        self.answered = False

    @property
    def current_question(self) -> Question:
        return self.questions[self.current_question_index]

    @property
    def is_finished(self) -> bool:
        return self.current_question_index >= len(self.questions)

    # TODO: Revist this method for unnecessary logic.
    def submit_answer(self, selected_index: int) -> bool:
        if self.is_finished:
            raise RuntimeError("The quiz session has finished.")

        if self.answered:
            raise RuntimeError("The current question has already been answered.")

        if not 0 <= selected_index < len(self.current_question.answers):
            raise ValueError("Selected answer index is out of range.")

        self.answered = True
        is_correct = selected_index == self.current_question.correct_answer

        if is_correct:
            self.score += 1

        return is_correct

    # REVIEW: Take a second look at this method.
    def next_question(self) -> None:
        if self.is_finished:
            raise RuntimeError("The quiz session has finished.")

        if not self.answered:
            raise RuntimeError("Answer the current question before continuing.")

        self.current_question_index += 1
        self.answered = False
