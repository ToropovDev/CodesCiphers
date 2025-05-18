"""
Лабораторная работа №5

Генераторы псевдослучайных чисел

Торопов Арсений Алексеевич РИ-320934
"""

import matplotlib.pyplot as plt


class LCG:
    """
    Испольую линейный конгруэнтный метод
    (Linear Congruential Generator, LCG)
    """

    def __init__(self, seed):
        self.state = seed
        self.a = 1664525
        self.c = 1013904223
        self.m = 2**32

    def next(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state

    def next_int(self, min_val=0, max_val=2**32 - 1):
        return min_val + self.next() % (max_val - min_val + 1)

    def get_sequence(self, n):
        return [self.next_int() for _ in range(n)]


if __name__ == "__main__":
    seed = 320934
    lcg = LCG(seed)
    sequence = lcg.get_sequence(100000)

    """
    Построим график распределения чисел
    Увидим, что на графике нет выбросов 
    и все столбцы примерно равны
    """
    plt.hist(sequence, bins=50, edgecolor="black")
    plt.title("Распределение псевдослучайных чисел")
    plt.xlabel("Значение")
    plt.ylabel("Частота")
    plt.show()

    print("Первые 100 чисел:")
    print(sequence[:100])

    def autocorrelation(seq, lag=1):
        """
        Проведем проверку используя автокорреляцию
        """
        mean = sum(seq) / len(seq)
        numerator = sum(
            (seq[i] - mean) * (seq[i + lag] - mean) for i in range(len(seq) - lag)
        )
        denominator = sum((x - mean) ** 2 for x in seq)
        return numerator / denominator if denominator != 0 else 0

    print(f"\nАвтокорреляция с лагом 1: {autocorrelation(sequence):.4f}")

"""
Вывод программы:
[2640625869, 862153672, 4227144839, 2054041658, 283673169, 1980946300, 3361426603, 1179712014, ...

Автокорреляция с лагом 1: -0.0006

Видим что значение автокорреляции очеень близко к нулю,
что является хорошим подтверждением исправности работы
генерации псевдослучайных чисел
"""
