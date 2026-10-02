def add(a, b):
    return a + b
def sub(a, b):
    return a - b
def mult(a, b):
    return a * b
def safe_div(a, b):
    if b == 0:
        return "Ошибка: деление на ноль"
    return a / b
print('Сложение:', add(5, 3))
print('Вычитание:', sub(5, 3))
print('Умножение:', mult(5, 3))
print('Деление:', safe_div(5, 0))
