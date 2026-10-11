import pytest

from trivia_time.game.question import Question
from trivia_time.game.session import QuizSession


@pytest.fixture
def questions() -> tuple[Question, ...]:
    return (
        Question(
            text="Which planet is known as the Red Planet?",
            answers=("Venus", "Mars", "Jupiter", "Mercury"),
            correct_answer=1,
        ),
        Question(
            text="How many sides does a triangle have?",
            answers=("Two", "Three", "Four", "Five"),
            correct_answer=1,
        ),
    )


def test_correct_answer_increases_score(questions: tuple[Question, ...]) -> None:
    session = QuizSession(questions)

    assert session.submit_answer(1) is True
    assert session.score == 1


def test_incorrect_answer_does_not_increase_score(questions: tuple[Question, ...]) -> None:
    session = QuizSession(questions)

    assert session.submit_answer(0) is False
    assert session.score == 0


def test_next_question_advances_session(questions: tuple[Question, ...]) -> None:
    session = QuizSession(questions)

    session.submit_answer(1)
    session.next_question()

    assert session.current_question_index == 1
    assert session.current_question.text == "How many sides does a triangle have?"
    assert session.answered is False


def test_session_finishes_after_last_question(questions: tuple[Question, ...]) -> None:
    session = QuizSession(questions)

    for _ in questions:
        session.submit_answer(1)
        session.next_question()

    assert session.is_finished is True
    assert session.score == 2
