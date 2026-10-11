from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Question:
    text: str
    answers: tuple[str, ...]
    correct_answer: int
