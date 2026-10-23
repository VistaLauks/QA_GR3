import math

class SideException(Exception):
    """Пользовательское исключение для ошибок с длинами сторон"""
    pass

class TriangleCalculator:
    def  __init__(self, a: float, b: float, c: float):
        self.a = a
        self.b = b
        self.c = c

    def get_area(self) -> float:
        # Проверка допустимости сторон
        if not (1 <= self.a < 100 and 1 <= self.b < 100 and 1 <= self.c < 100):
            raise SideException("Стороны должны быть от 1 до 100")
        # Проверяем возможность образования треугольника
        if (
                self.a >= self.b + self.c or
                self.b >= self.a + self.c or
                self.c >= self.a + self.b
        ):
            raise SideException("Недопустимые длины сторон")

        # Вычисление полупериметра
        p = (self.a + self.b + self.c) / 2

        # Вычисление площади по формуле Герона
        try:
            area = math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))
        except ValueError:
            raise SideException("Невозможно вычислить площадь треугольника")

        # Округление до сотых
        return round(area, 2)

# Пример использования:
calculator = TriangleCalculator(3.0, 4.0, 5.0)
print(calculator.get_area())  # Выведет 6.0