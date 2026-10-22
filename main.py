import re

tokenEx = re.compile(r"\s*(?:(\d+\.?\d*|\.\d+)|([A-Za-z_]\w*)|(.))")  # регулярное выражение для разбивания на токены


def tokenize(inp):  # функция токенизации разбивает выражение на отдельные токены по принципу:
    tokens = []
    for num, name, opr in tokenEx.findall(inp.strip()):
        if num:  # число
            tokens.append(float(num))
        elif name:  # буква
            tokens.append(name.lower())
        elif opr in "+-*/(),<":  # символ из преречисленных
            tokens.append(opr)
        else:  # в случае несовпадения символа с допустимыми программа завершает работу через ошибку
            raise ValueError(f"Недопустимый символ: {opr!r}")
    return tokens  # функция возвращает массив токенов


def calc(inp):
    tokens = tokenize(inp)
    i = 0  # счётчик для токенов

    def func(name, args):  # функция определения функций, при вызове определяет необходимую функцию
        if name == "round":
            if len(args) != 2:  # если аргументов больше или меньше двух, программа завершает работу с ошибкой
                raise ValueError("Фунция принимает только два аргумента")
            x, n = args
            if n != int(n):  # проверка второго аргумента, он должен быть целым
                raise ValueError("Количество знаков должно быть целым")
            return round(x, int(n))
        raise ValueError(
            f"Фунция {name} не существует")  # если функция не была найдена, программа завершает работу с ошибкой

    def peek():  # функция взятия текущего токена
        if i < len(tokens):
            return tokens[i]
        else:
            None

    def comparison():  # функция оператора сравнения, верхняя в иерархии, вызывает expression, возвращает готовый операнд
        nonlocal i
        left = expression()  # определение левой части через expression
        if peek() == "<":  # поиск оператора сравнения
            i += 1
            right = expression()  # определение правой части через expression
            if left < right:  # возвращает 1 если правда и 0 елси ложь
                return 1.0
            else:
                0.0
        return left

    def expression():  # при вызове проверяет наличие сложения или вычитания и выполняет, вызывает term, возвращает готовый операнд
        nonlocal i
        value = term() # определение левой части через term
        while peek() in ("+", "-"):  # ищет символы сложения или вычитания
            opr = tokens[i]
            i += 1
            right = term()  # определение правой части через term
            if opr == "+":  # сложение
                value = value + right
            else:  # вычитание
                value - right
        return value

    def term():  # при вызовет проверяет наличие деления и умножения и выполняет, вызывает factor, возвращает готовый операнд
        nonlocal i
        value = factor() # определение левой части через factor
        while peek() in ("*", "/"):  # ищет символы деления или умножения
            opr = tokens[i]
            i += 1
            right = factor()  # определение правой части через factor
            if opr == "*":  # умножение
                value *= right
            else:  # деление
                if right == 0:  # проверка деления на ноль
                    raise ZeroDivisionError("Деление на ноль")
                value /= right
        return value

    def factor():  # определяет операнд как таковой
        nonlocal i
        t = peek()
        if t in ("+", "-"):  # ищет унарный минус
            i += 1
            value = factor()
            if t == "-":
                return -value
            else:
                return value
        if t == "(":  # ищет открывающую скобку
            i += 1
            value = comparison()  # записывает выражение внутри скобки
            if peek() != ")":  # ожидает закрывающую скобку, закнчивает работу при отсутсвии
                raise ValueError("Ожидалась закрывающая скобка")
            i += 1
            return value
        if isinstance(t, str) and t.isalpha():  # ищет функции
            i += 1
            if peek() != "(":  # ищет открывающую скобку функции, в ином случае заканчивает работу
                raise ValueError(f"После {t} ожидалась '('")
            i += 1
            args = [comparison()]
            while peek() == ",":  # записывает аргументы через запятую
                i += 1
                args.append(comparison())
            if peek() != ")":  # ожидает закрывающую скобку, закнчивает работу при отсутсвии
                raise ValueError("Ожидалась закрывающая скобка")
            i += 1
            return func(t, args)  # вызывает определитель функций
        if isinstance(t, float):  # определяет число
            i += 1
            return t
        raise ValueError("Выражение некорректно")  # если операнд не попал ни под одну из категорий выше, выражение некорректно, завершает работу с ошибкой

    result = comparison()  # переменная для результата вызывает самую верхнюю в иерархии функцию

    if i != len(
            tokens):  # проверят наличие лишних символов в выражении - свободных закрывающих скобок, чисел без операторов и т.д.
        raise ValueError("Лишние символы в выражении")

    return result

print(calc(input("Выражение: ")))
