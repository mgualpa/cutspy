import pytest

from cutspy.cutspy_dom import CSPModel


@pytest.fixture
def basic_model_ex01() -> CSPModel:
    m = CSPModel()
    m.add_stock(name="A", lenght=5.0, cost=6)
    m.add_stock(name="B", lenght=6.0, cost=7)
    m.add_stock(name="C", lenght=9.0, cost=10)

    m.add_part(name="S", lenght=2, demand=20)
    m.add_part(name="M", lenght=3, demand=10)
    m.add_part(name="L", lenght=4, demand=20)
    return m


@pytest.fixture
def pattterns_as_dict() -> list:
    p = [
        {"stock": "A", "cuts": {"S": 2, "M": 0, "L": 0}},
        {"stock": "B", "cuts": {"S": 3, "M": 0, "L": 0}},
        {"stock": "C", "cuts": {"S": 4, "M": 0, "L": 0}},
        {"stock": "A", "cuts": {"S": 0, "M": 1, "L": 0}},
        {"stock": "B", "cuts": {"S": 0, "M": 2, "L": 0}},
        {"stock": "C", "cuts": {"S": 0, "M": 3, "L": 0}},
        {"stock": "A", "cuts": {"S": 0, "M": 0, "L": 1}},
        {"stock": "B", "cuts": {"S": 0, "M": 0, "L": 1}},
        {"stock": "C", "cuts": {"S": 0, "M": 0, "L": 2}},
    ]
    return p


def test_model_make_patterns(
    basic_model_ex01: CSPModel, pattterns_as_dict: list
):
    patterns_as_dict = basic_model_ex01.make_patterns()
    assert len(patterns_as_dict) == 9
    assert patterns_as_dict == pattterns_as_dict
