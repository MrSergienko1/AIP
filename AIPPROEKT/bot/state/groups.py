from typing import TypedDict

from aiogram.fsm.state import State, StatesGroup


class TicketState(StatesGroup):
    """Класс состояния прохождения билета"""

    class Data(TypedDict):
        """Класс описания данных состояния прохождения билета TicketState"""

        questions_len: int
        """Количество вопросов текущего билета"""

        right_answers_count: int
        """Счетчик правильных ответов"""

    waiting_answer = State()
