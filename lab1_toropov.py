"""
Лабораторная работа №1

Эффективное кодирование

Торопов Арсений Алексеевич РИ-320934
"""

import math
from heapq import heappush, heappop


class Symbol:
    """
    Создадим собственный класс
    для символа, чтобы задать ему
    все необходимые свойства
    и определить операцию сравнения "меньше"
    """

    def __init__(self, character, probability):
        self.character = character
        self.probability = probability
        self.code = ""

    def __lt__(self, other):
        return self.probability < other.probability


class ShannonFano:
    """
    Определим класс для построения
    кода Шеннона-Фано и переопределения
    методы вывода
    """

    def __init__(self, symbols):
        self.symbols = sorted(symbols, key=lambda s: s.probability, reverse=True)
        self.codes = {}

    def encode(self):
        self._shannon_fano([s for s in self.symbols], "")

    def _shannon_fano(self, symbols, prefix):
        if len(symbols) == 1:
            symbols[0].code = prefix
            return

        total_prob = sum(s.probability for s in symbols)

        min_diff = float("inf")
        split_index = 1

        # Разделение на две части с минимальной разницей вероятностей
        for i in range(1, len(symbols)):
            left_sum = sum(s.probability for s in symbols[:i])
            right_sum = total_prob - left_sum
            diff = abs(left_sum - right_sum)

            if diff < min_diff:
                min_diff = diff
                split_index = i

        # Рекурсивное кодирование обеих частей
        self._shannon_fano(symbols[:split_index], prefix + "0")
        self._shannon_fano(symbols[split_index:], prefix + "1")

    def print_codes(self):
        print("Коды Шеннона-Фано:")
        for s in self.symbols:
            print(f"{s.character}: {s.code}")


class Huffman:
    """
    Аналогичное создание класса
    для построения кода Хаффмена
    """

    def __init__(self, symbols):
        self.symbols = symbols
        self.heap = []
        self.codes = {}

    def encode(self):
        # Создание кучи
        for s in self.symbols:
            heappush(self.heap, (s.probability, id(s), s))

        # Построение дерева Хаффмана
        while len(self.heap) > 1:
            p1, _, left = heappop(self.heap)
            p2, _, right = heappop(self.heap)

            merged = Symbol(f"{left.character}{right.character}", p1 + p2)
            merged.code = ""
            heappush(self.heap, ((p1 + p2), id(merged), merged))

            left.parent = merged
            right.parent = merged

        # Назначение кодов листьям
        for s in self.symbols:
            code = ""
            current = s
            while hasattr(current, "parent"):
                parent = current.parent

                if parent.character.startswith(current.character):
                    code = "0" + code
                else:
                    code = "1" + code
                current = parent
            s.code = code

    def print_codes(self):
        print("Коды Хаффмана:")
        for s in self.symbols:
            print(f"{s.character}: {s.code}")


def calculate_metrics(symbols):
    """
    Функция для расчета всех
    необходимых метрик
    согласно формулам
    """
    n = len(symbols)

    entropy = math.log2(n)
    relative_entropy = -sum(s.probability * math.log2(s.probability) for s in symbols)

    avg_length = sum(s.probability * len(s.code) for s in symbols)

    k_cc = entropy / avg_length
    k_o = relative_entropy / avg_length
    return {
        "entropy": entropy,
        "relative_entropy": relative_entropy,
        "avg_length": avg_length,
        "k_cc": k_cc,
        "k_o": k_o,
    }


if __name__ == "__main__":
    """
    Мой порядковый номер в списке: 37
    Беру вариант №17, верхние значения
    из таблицы распределения вероятностей
    """

    symbols_data = [
        ("1", 0.209),
        ("2", 0.172),
        ("3", 0.137),
        ("4", 0.133),
        ("5", 0.102),
        ("6", 0.095),
        ("7", 0.079),
        ("8", 0.073),
    ]

    symbols = [Symbol(char, prob) for char, prob in symbols_data]

    print("Метод Шеннона-Фано")
    sf = ShannonFano(symbols)
    sf.encode()
    sf.print_codes()

    metrics = calculate_metrics(symbols)
    print("\nХарактеристики:")
    print(f"Энтропия H_max: {metrics['entropy']:.3f}")
    print(f"Относительная энтропия H: {metrics['relative_entropy']:.3f}")
    print(f"Средняя длина кода l_ср: {metrics['avg_length']:.3f}")
    print(f"Коэффициент статического сжатия K_cc: {metrics['k_cc']:.3f}")
    print(f"Коэффициент относительной эффективности K_о: {metrics['k_o']:.3f}")

    print("\nМетод Хаффмана")
    huffman = Huffman(symbols)
    huffman.encode()
    huffman.print_codes()

    metrics = calculate_metrics(symbols)
    print("\nХарактеристики:")
    print(f"Энтропия H_max: {metrics['entropy']:.3f}")
    print(f"Относительная энтропия H: {metrics['relative_entropy']:.3f}")
    print(f"Средняя длина кода l_ср: {metrics['avg_length']:.3f}")
    print(f"Коэффициент статического сжатия K_cc: {metrics['k_cc']:.3f}")
    print(f"Коэффициент относительной эффективности K_о: {metrics['k_o']:.3f}")

"""
Вывод программы:

Метод Шеннона-Фано
Коды Шеннона-Фано:
1: 00
2: 010
3: 011
4: 100
5: 101
6: 110
7: 1110
8: 1111

Характеристики:
Энтропия H_max: 3.000
Относительная энтропия H: 2.912
Средняя длина кода l_ср: 2.943
Коэффициент статического сжатия K_cc: 1.019
Коэффициент относительной эффективности K_о: 0.990

Метод Хаффмана
Коды Хаффмана:
1: 01
2: 111
3: 101
4: 100
5: 001
6: 000
7: 1101
8: 1100

Характеристики:
Энтропия H_max: 3.000
Относительная энтропия H: 2.912
Средняя длина кода l_ср: 2.943
Коэффициент статического сжатия K_cc: 1.019
Коэффициент относительной эффективности K_о: 0.990
"""
