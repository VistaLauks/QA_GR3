import unittest
import pytest
from triangle import TriangleCalculator, SideException


# ============================================================
# 1. ТЕСТЫ В СТИЛЕ UNITTEST С МАРКЕРАМИ PYTEST
# ============================================================

@pytest.mark.smoke
class TestTriangleSmoke(unittest.TestCase):
    """Дымовые тесты в стиле unittest"""

    def test_area_3_4_5(self):
        calc = TriangleCalculator(3.0, 4.0, 5.0)
        self.assertEqual(calc.get_area(), 6.0)

    def test_invalid_triangle(self):
        calc = TriangleCalculator(1.0, 2.0, 10.0)
        with self.assertRaises(SideException):
            calc.get_area()


@pytest.mark.regression
class TestTriangleRegression(unittest.TestCase):
    """Регрессионные тесты в стиле unittest"""

    def test_area_5_5_6(self):
        calc = TriangleCalculator(5.0, 5.0, 6.0)
        self.assertEqual(calc.get_area(), 12.0)

    def test_side_too_small(self):
        calc = TriangleCalculator(0.5, 4.0, 5.0)
        with self.assertRaises(SideException):
            calc.get_area()

    def test_side_too_large(self):
        calc = TriangleCalculator(150.0, 100.0, 50.0)
        with self.assertRaises(SideException):
            calc.get_area()


# ============================================================
# 2. ПАРАМЕТРИЗАЦИЯ В UNITTEST (через subTest)
# ============================================================

@pytest.mark.regression
class TestTriangleParametrized(unittest.TestCase):
    """Параметризованные тесты в стиле unittest (через subTest)"""

    def test_area(self):
        test_data = [
            (3.0, 4.0, 5.0, 6.0),
            (5.0, 5.0, 6.0, 12.0),
            (1.0, 1.0, 1.0, 0.43),
            (6.0, 8.0, 10.0, 24.0),
        ]
        for a, b, c, expected in test_data:
            with self.subTest(a=a, b=b, c=c, expected=expected):
                calc = TriangleCalculator(a, b, c)
                self.assertEqual(calc.get_area(), expected)


    def test_invalid_data(self):
        test_data = [
            (0.5, 4.0, 5.0, "Стороны должны быть от 1 до 100"),
            (101.0, 4.0, 5.0, "Стороны должны быть от 1 до 100"),
            (1.0, 2.0, 10.0, "Недопустимые длины сторон"),
        ]
        for a, b, c, expected_msg in test_data:
            with self.subTest(a=a, b=b, c=c, expected_msg=expected_msg):
                calc = TriangleCalculator(a, b, c)
                with self.assertRaises(SideException) as cm:
                    calc.get_area()
                self.assertEqual(str(cm.exception), expected_msg)


# ============================================================
# 3. ТЕСТЫ В ЧИСТОМ СТИЛЕ PYTEST
# ============================================================

@pytest.mark.smoke
def test_pytest_smoke():
    """Дымовой тест в стиле pytest"""
    calc = TriangleCalculator(3.0, 4.0, 5.0)
    assert calc.get_area() == 6.0


@pytest.mark.regression
def test_pytest_regression():
    """Регрессионный тест в стиле pytest"""
    calc = TriangleCalculator(5.0, 5.0, 6.0)
    assert calc.get_area() == 12.0


# ============================================================
# 4. ПАРАМЕТРИЗАЦИЯ В СТИЛЕ PYTEST (БОЛЕЕ КОМПАКТНО)
# ============================================================

@pytest.mark.regression
@pytest.mark.parametrize("a, b, c, expected", [
    (3.0, 4.0, 5.0, 6.0),
    (5.0, 5.0, 6.0, 12.0),
    (1.0, 1.0, 1.0, 0.43),
    (6.0, 8.0, 10.0, 24.0),
])
def test_pytest_parametrized(a, b, c, expected):
    """Параметризованный тест в стиле pytest"""
    calc = TriangleCalculator(a, b, c)
    assert calc.get_area() == expected


# ============================================================
# 5. ПРОВЕРКА ИСКЛЮЧЕНИЙ В СТИЛЕ PYTEST
# ============================================================

@pytest.mark.regression
@pytest.mark.parametrize("a, b, c, expected_msg", [
    (0.5, 4.0, 5.0, "Стороны должны быть от 1 до 100"),
    (101.0, 4.0, 5.0, "Стороны должны быть от 1 до 100"),
    (1.0, 2.0, 10.0, "Недопустимые длины сторон"),
    (1.0, 1.0, 3.0, "Недопустимые длины сторон"),
])
def test_pytest_negative_parametrized(a, b, c, expected_msg):
    """Параметризованная проверка исключений в стиле pytest"""
    calc = TriangleCalculator(a, b, c)
    with pytest.raises(SideException, match=expected_msg):
        calc.get_area()


# ============================================================
# 6. ОБЩАЯ СТРУКТУРА С МАРКЕРАМИ
# ============================================================

@pytest.mark.skip(reason="Тест временно отключён")
def test_skipped():
    """Пропущенный тест"""
    assert 1 + 1 == 2


@pytest.mark.xfail(reason="Этот тест пока не должен проходить")
def test_xfail():
    """Ожидаемо падающий тест"""
    assert 1 + 1 == 3


# ============================================================
# 7. ФИКСТУРЫ В СТИЛЕ UNITTEST (setUp/tearDown)
# ============================================================

@pytest.mark.regression
class TestTriangleWithSetup(unittest.TestCase):
    """Использование setUp и tearDown в unittest"""

    def setUp(self):
        """Выполняется перед каждым тестом"""
        self.calc = TriangleCalculator(3.0, 4.0, 5.0)
        print("\n🔧 setUp: создан треугольник 3-4-5")

    def tearDown(self):
        """Выполняется после каждого теста"""
        print("🧹 tearDown: очистка после теста")

    def test_area(self):
        self.assertEqual(self.calc.get_area(), 6.0)

    def test_perimeter(self):
        perimeter = self.calc.a + self.calc.b + self.calc.c
        self.assertEqual(perimeter, 12.0)


if __name__ == "__main__":
    pytest.main(["-v", "--tb=short", __file__])