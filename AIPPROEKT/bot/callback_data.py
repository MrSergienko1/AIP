from aiogram.filters.callback_data import CallbackData


class TicketCallbackData(CallbackData, prefix="ticket"):
    """Класс CallbackData для выбора билета"""

    ticket_idx: int


class QuestionAnswerCallbackData(CallbackData, prefix="question_answer"):
    """Класс CallbackData для выбора ответа"""

    ticket_idx: int
    question_idx: int
    answer_idx: int


class TicketQuestionCallbackData(CallbackData, prefix="ticket_question"):
    """Класс CallbackData для перехода к следующему вопросу"""

    ticket_idx: int
    question_idx: int
