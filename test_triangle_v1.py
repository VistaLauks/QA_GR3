import pytest
from triangle import TriangleCalculator, SideException

# ============================================================
# 1. ПОЗИТИВНЫЕ ТЕСТЫ (проверка площади)
# ============================================================

def test_area_3_4_5():
    """Прямоугольный треугольник 3-4-5 → площадь 6.0"""
    calc = TriangleCalculator(3.0, 4.0, 5.0)
    assert calc.get_area() == 6.0

def test_area_5_5_6():
    """Равнобедренный треугольник 5-5-6 → площадь 12.0"""
    calc = TriangleCalculator(5.0, 5.0, 6.0)
    assert calc.get_area() == 12.0

def test_area_1_1_1():
    """Равносторонний треугольник 1-1-1 → площадь ≈0.43"""
    calc = TriangleCalculator(1.0, 1.0, 1.0)
    assert calc.get_area() == 0.43

# ============================================================`
# 2. ПАРАМЕТРИЗОВАННЫЙ ТЕСТ (один тест – много данных)
# ============================================================

@pytest.mark.parametrize("a, b, c, expected", [
    (3.0, 4.0, 5.0, 6.0),
    (5.0, 5.0, 6.0, 12.0),
    (2.0, 2.0, 3.0, 1.98),
    (6.0, 8.0, 10.0, 24.0),
    (1.0, 1.0, 1.0, 0.43),
])
def test_area_parametrized(a, b, c, expected):
    """Проверка площади для разных треугольников"""
    calc = TriangleCalculator(a, b, c)
    assert calc.get_area() == expected

# ============================================================
# 3. НЕГАТИВНЫЕ ТЕСТЫ (проверка исключений)
# ============================================================

def test_side_too_small():
    """Сторона меньше 1 → SideException"""
    calc = TriangleCalculator(0.5, 4.0, 5.0)
    with pytest.raises(SideException, match="Стороны должны быть от 1 до 100"):
        calc.get_area()

def test_side_too_large():
    """Сторона больше 100 → SideException"""
    calc = TriangleCalculator(150.0, 100.0, 50.0)
    with pytest.raises(SideException, match="Стороны должны быть от 1 до 100"):
        calc.get_area()

def test_invalid_triangle():
    """Стороны не образуют треугольник → SideException"""
    calc = TriangleCalculator(1.0, 2.0, 10.0)
    with pytest.raises(SideException, match="Недопустимые длины сторон"):
        calc.get_area()

# ============================================================
# 4. ПАРАМЕТРИЗОВАННЫЙ НЕГАТИВНЫЙ ТЕСТ
# ============================================================

@pytest.mark.parametrize("a, b, c, expected_msg", [
    (0.5, 4.0, 5.0, "Стороны должны быть от 1 до 100"),
    (101.0, 4.0, 5.0, "Стороны должны быть от 1 до 100"),
    (1.0, 2.0, 10.0, "Недопустимые длины сторон"),
    (1.0, 1.0, 3.0, "Недопустимые длины сторон"),
])
def test_negative_parametrized(a, b, c, expected_msg):
    """Проверка нескольких невалидных наборов"""
    calc = TriangleCalculator(a, b, c)
    with pytest.raises(SideException, match=expected_msg):
        calc.get_area()

# ============================================================
# 5. ПРОВЕРКА ОКРУГЛЕНИЯ
# ============================================================

def test_rounding():
    """Проверка, что площадь округляется до сотых"""
    calc = TriangleCalculator(2.0, 3.0, 4.0)
    assert calc.get_area() == 2.90

# ============================================================
# 6. ТЕСТЫ С МАРКЕРАМИ (для группировки)
# ============================================================

@pytest.mark.smoke
def test_smoke_valid():
    """Дымовой тест: проверяем базовую работоспособность"""
    calc = TriangleCalculator(3.0, 4.0, 5.0)
    assert calc.get_area() == 6.0

@pytest.mark.smoke
def test_smoke_invalid():
    """Дымовой тест: проверяем, что исключение выбрасывается"""
    calc = TriangleCalculator(1.0, 2.0, 10.0)
    with pytest.raises(SideException):
        calc.get_area()

@pytest.mark.regression
def test_regression_equilateral():
    """Регрессионный тест: равносторонний треугольник"""
    calc = TriangleCalculator(1.0, 1.0, 1.0)
    assert calc.get_area() == 0.43