import pytest
from math_utils import add

#Фикстура подготовки данных
@pytest.fixture
def addition_function():
    print(" Start Fixture!")
    yield add  # <-- yield разделяет подготовку (до) и очистку (после), позволяя проводить каждый тест в исходном состоянии
    print(" End Fixture!")

#Подготовка тестового окружения
@pytest.mark.parametrize(
    "args, expected",
    [
        ([1, 2], 3),
        ([0, 0, 0], 0),
        ([-1, -2, -3], -6),
        ([5], 5),
        ([], 0),
        ([10, -5, 3.5], 8.5),
        ([1, 1, 1, 1, 1], 5),
        ([-10, 10], 0),
        ([23, -26, 17, -74], -60),
        ([23, -26, 17, 0], 14)
    ],
    #Подпись теста
    ids=[
        "2 Positive",
        "3 Zero",
        "3 Negative",
        "Only one Element",
        "Zero list and Zero",
        "Int and Float",
        "Many Equal arguments",
        "1 Positive and 1 negative (sum = 0)",
        "Sum three or more Elements with Different sings",
        "Sum some Elements with Zero"
    ]
)

# Вызов функции для проверки
def test_add_with_fixture(addition_function, args, expected):
    result = addition_function(*args)
    #В случае если тест упал, сообщение об ошибке
    assert result == expected, print (f"Ошибка: Для набора тестовых данных {args} ожидалось {expected}, но получено {result}")
