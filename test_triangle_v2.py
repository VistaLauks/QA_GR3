import pytest
from triangle import TriangleCalculator, SideException


# ============================================================
# 1. ФИКСТУРЫ (подготовка данных для тестов)
# ============================================================

@pytest.fixture
def right_triangle():
    """Фикстура: прямоугольный треугольник 3-4-5 (площадь 6.0)"""
    return TriangleCalculator(3.0, 4.0, 5.0)

@pytest.fixture
def equilateral_triangle():
    """Фикстура: равносторонний треугольник 1-1-1 (площадь ≈ 0.43)"""
    return TriangleCalculator(1.0, 1.0, 1.0)

@pytest.fixture
def invalid_triangle():
    """Фикстура: невалидный треугольник (1, 2, 10)"""
    return TriangleCalculator(1.0, 2.0, 10.0)

# Фикстура с областью видимости module (создаётся один раз для всех тестов в файле)
@pytest.fixture(scope="module")
def large_triangle():
    """Фикстура: треугольник 6-8-10 (прямоугольный)"""
    return TriangleCalculator(6.0, 8.0, 10.0)

# Фикстура, которая использует другую фикстуру
@pytest.fixture
def right_triangle_area(right_triangle):
    """Фикстура, возвращающая площадь прямоугольного треугольника"""
    return right_triangle.get_area()


# ============================================================
# 2. ПОЗИТИВНЫЕ ТЕСТЫ (используют фикстуры)
# ============================================================

def test_area_right_triangle(right_triangle):
    """Проверка площади прямоугольного треугольника 3-4-5"""
    assert right_triangle.get_area() == 6.0

def test_area_equilateral(equilateral_triangle):
    """Проверка площади равностороннего треугольника 1-1-1"""
    assert equilateral_triangle.get_area() == 0.43

def test_area_large_triangle(large_triangle):
    """Проверка площади треугольника 6-8-10"""
    assert large_triangle.get_area() == 24.0

def test_fixture_returns_area(right_triangle_area):
    """Использование фикстуры, которая возвращает площадь"""
    assert right_triangle_area == 6.0


# ============================================================
# 3. ПАРАМЕТРИЗОВАННЫЕ ТЕСТЫ (смешиваем с фикстурами)
# ============================================================

@pytest.mark.parametrize("a, b, c, expected", [
    (3.0, 4.0, 5.0, 6.0),
    (5.0, 5.0, 6.0, 12.0),
    (2.0, 2.0, 3.0, 1.98),
])
def test_parametrized_without_fixture(a, b, c, expected):
    """Параметризованный тест без фикстур (создаём объект внутри)"""
    calc = TriangleCalculator(a, b, c)
    assert calc.get_area() == expected

# Параметризованная фикстура (продвинутый уровень)
@pytest.fixture(params=[
    (3.0, 4.0, 5.0, 6.0),
    (5.0, 5.0, 6.0, 12.0),
    (2.0, 2.0, 3.0, 1.98),
])
def triangle_data(request):
    """Параметризованная фикстура: возвращает кортеж (a, b, c, expected)"""
    return request.param

def test_parametrized_fixture(triangle_data):
    """Тест использует параметризованную фикстуру"""
    a, b, c, expected = triangle_data
    calc = TriangleCalculator(a, b, c)
    assert calc.get_area() == expected


# ============================================================
# 4. НЕГАТИВНЫЕ ТЕСТЫ (используют фикстуры)
# ============================================================

def test_invalid_triangle_using_fixture(invalid_triangle):
    """Использование фикстуры с невалидным треугольником"""
    with pytest.raises(SideException, match="Недопустимые длины сторон"):
        invalid_triangle.get_area()

# Фикстура для негативных тестов с параметрами
@pytest.fixture(params=[
    (0.5, 4.0, 5.0, "Стороны должны быть от 1 до 100"),
    (101.0, 4.0, 5.0, "Стороны должны быть от 1 до 100"),
    (1.0, 2.0, 10.0, "Недопустимые длины сторон"),
])
def invalid_data(request):
    """Параметризованная фикстура для негативных тестов"""
    return request.param

def test_negative_with_fixture(invalid_data):
    """Негативный тест с параметризованной фикстурой"""
    a, b, c, expected_msg = invalid_data
    calc = TriangleCalculator(a, b, c)
    with pytest.raises(SideException, match=expected_msg):
        calc.get_area()


# ============================================================
# 5. ФИКСТУРА С YIELD (setup/teardown)
# ============================================================

@pytest.fixture
def triangle_with_teardown():
    """Фикстура с yield: создаёт объект и выполняет очистку после теста"""
    print("\n🔧 Создаём треугольник...")
    calc = TriangleCalculator(3.0, 4.0, 5.0)
    yield calc  # передаём объект в тест
    print("\n🧹 Очистка после теста...")
    # Здесь можно закрыть файлы, соединения с БД, браузер и т.д.

def test_with_setup_teardown(triangle_with_teardown):
    """Тест, использующий фикстуру с yield"""
    assert triangle_with_teardown.get_area() == 6.0


# ============================================================
# 6. МАРКЕРЫ (группировка тестов)
# ============================================================

@pytest.mark.smoke
def test_smoke_with_fixture(right_triangle):
    """Дымовой тест с фикстурой"""
    assert right_triangle.get_area() == 6.0

@pytest.mark.regression
def test_regression_with_fixture(equilateral_triangle):
    """Регрессионный тест с фикстурой"""
    assert equilateral_triangle.get_area() == 0.43


# ============================================================
# 7. ТЕСТЫ БЕЗ ФИКСТУР (для сравнения)
# ============================================================

def test_without_fixture():
    """Обычный тест без фикстуры — всё создаётся внутри"""
    calc = TriangleCalculator(3.0, 4.0, 5.0)
    assert calc.get_area() == 6.0

def test_multiple_without_fixture():
    """Без фикстур приходится создавать объект в каждом тесте"""
    calc1 = TriangleCalculator(3.0, 4.0, 5.0)
    assert calc1.get_area() == 6.0

    calc2 = TriangleCalculator(1.0, 1.0, 1.0)
    assert calc2.get_area() == 0.43