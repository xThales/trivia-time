import pygame

from trivia_time.config import FPS, WINDOW_HEIGHT, WINDOW_WIDTH
from trivia_time.game.question import Question
from trivia_time.game.session import QuizSession
from trivia_time.game.state import GameState
from trivia_time.ui import quiz
from trivia_time.ui.menu import MainMenu
from trivia_time.ui.quiz import QuizScreen


def run() -> None:
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Trivia Time")

    menu = MainMenu(screen)

    questions = (
        Question(
            text="What is 2 + 2?",
            answers=("4", "5", "6", "7"),
            correct_answer=0,
        ),
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
    session = QuizSession(questions)
    quiz_screen = QuizScreen(screen, session.current_question)

    result_font = pygame.font.Font(None, 48)
    instruction_font = pygame.font.Font(None, 30)
    clock = pygame.time.Clock()

    current_state = GameState.MAIN_MENU
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif current_state == GameState.MAIN_MENU:
                if menu.handle_event(event):
                    if session.is_finished:
                        session = QuizSession(questions)
                        quiz_screen.set_question(session.current_question)

                    current_state = GameState.QUIZ

            elif current_state == GameState.QUIZ:
                if (
                    session.answered
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_RETURN
                ):
                    session.next_question()
                    if session.is_finished:
                        current_state = GameState.RESULTS
                    else:
                        quiz_screen.set_question(session.current_question)
                else:
                    selected_index = quiz_screen.handle_event(event)
                    if selected_index is not None:
                        is_correct = session.submit_answer(selected_index)
                        quiz_screen.show_feedback(selected_index, is_correct)

            elif current_state == GameState.RESULTS:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    current_state = GameState.MAIN_MENU

        screen.fill((30, 30, 30))

        if current_state == GameState.MAIN_MENU:
            menu.draw()
        elif current_state == GameState.QUIZ:
            quiz_screen.draw()
        elif current_state == GameState.RESULTS:
            result_text = f"Quiz complete! Score: {session.score}/{len(questions)}"
            result_surface = result_font.render(
                result_text,
                True,
                (245, 245, 245),
            )
            result_rect = result_surface.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30),
            )
            screen.blit(result_surface, result_rect)

            instruction_surface = instruction_font.render(
                "Press Enter to return to the menu",
                True,
                (190, 190, 190),
            )
            instruction_rect = instruction_surface.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30),
            )
            screen.blit(instruction_surface, instruction_rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
