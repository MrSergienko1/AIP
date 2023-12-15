import pytest

from bot.routers.user.start import check_if_ticket_passed
from bot.utils import tickets


def test_ticket_by_idx():
    with pytest.raises(IndexError):
        tickets.get_ticket_by_idx(len(tickets._TICKETS) + 1)

    tickets.get_ticket_by_idx(0)


def test_check_if_right_answer():
    ticket = tickets._TICKETS[0]
    question = ticket.questions[0]

    assert tickets.check_if_right_answer(question, question.right_answer_idx)
    assert not tickets.check_if_right_answer(question, question.right_answer_idx + 1)


def test_check_if_ticket_passed():
    assert check_if_ticket_passed({"questions_len": 1, "right_answers_count": 1})
    assert not check_if_ticket_passed({"questions_len": 10, "right_answers_count": 0})
