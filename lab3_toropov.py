"""
Лабораторная работа №3

Помехоустойчивое кодирование

Торопов Арсений Алексеевич РИ-320934

Мною выбрано задание №2 - написание кода
"""

import math


def ceil_log2(x: int) -> int:
    return math.ceil(math.log2(x)) if x > 0 else 0


class CRCCalculator:
    def crc(self, dataword: str, generator: str):
        generator_length = len(generator)
        gen = self.to_dec(generator)
        dword = self.to_dec(dataword)

        crc = self.calculate_crc(dword, gen)

        codeword = (dword << (generator_length - 1)) | crc

        return {"codeword": self.to_bin(codeword), "crc": self.to_bin(crc)}

    def decode(self, received_codeword: str, generator: str):
        generator_length = len(generator)
        dataword_length = len(received_codeword) - generator_length + 1

        received_dataword = received_codeword[:dataword_length]
        received_crc = received_codeword[dataword_length:]

        calculated_crc = self.calculate_crc(
            self.to_dec(received_dataword), self.to_dec(generator)
        )

        return {
            "is_correct": self.to_bin(calculated_crc) == received_crc,
            "dataword_bin": received_dataword,
            "dataword_dec": self.to_dec(received_dataword),
            "crc_bin": received_crc,
            "crc_dec": self.to_dec(received_crc),
        }

    def calculate_crc(self, dataword: int, generator: int) -> int:
        generator_length = len(self.to_bin(generator))
        dividend = dataword << (generator_length - 1)
        shift = ceil_log2(dividend + 1) - generator_length if dividend > 0 else 0

        while dividend >= generator or shift >= 0:
            mask = (dividend >> shift) ^ generator
            dividend = (dividend & ((1 << shift) - 1)) | (mask << shift)
            if dividend == 0:
                break
            shift = ceil_log2(dividend + 1) - generator_length

        return dividend

    @staticmethod
    def to_bin(number: int) -> str:
        return bin(number)[2:] if number != 0 else "0"

    @staticmethod
    def to_dec(binary_str: str) -> int:
        return int(binary_str, 2)


MENU = """
1. Кодировать слово
2. Декодировать слово
3. Выйти
"""


def main():
    print(MENU)
    choice = input("Выберите опцию: ").strip()

    if choice == "1":
        dataword = input("Кодируемое слово (в двоичном виде): ").strip()
        generator = input("Генераторный полином (в двоичном виде): ").strip()

        calc = calculator.crc(dataword, generator)
        print(f"Закодированное слово: {calc['codeword']}, CRC: {calc['crc']}\n")
        main()

    elif choice == "2":
        codeword = input("Закодированное слово (в двоичном виде): ").strip()
        generator = input("Генераторный полином (в двоичном виде): ").strip()

        result = calculator.decode(codeword, generator)
        if result["is_correct"]:
            print("Данные корректны.")
        else:
            print("Данные повреждены.")

        print(
            f"Декодированное слово (bin): {result['dataword_bin']}, CRC: {result['crc_bin']}"
        )
        print(
            f"Декодированное слово (dec): {result['dataword_dec']}, CRC: {result['crc_dec']}"
        )
        main()

    elif choice == "3":
        print("Выход из программы.")
        exit()

    else:
        print("Неверный ввод. Попробуйте снова.\n")
        main()


if __name__ == "__main__":
    calculator = CRCCalculator()
    main()

"""
Проверка работы программы:

1. Выберем число для проверки. Я возьму число 34,
так как это порядковый номер моей академ. группы

2. Переведем его в двоичный вид - 100010

3. Будем использовать полином '1011' - xˆ3 + x + 1

4. Введем данные в программу и получим ответ:

---
1. Кодировать слово
2. Декодировать слово
3. Выйти

Выберите опцию: 1
Кодируемое слово (в двоичном виде): 100010
Генераторный полином (в двоичном виде): 1011
Закодированное слово: 100010100, CRC: 100
---

5. Попробуем декодировать полученное слово:

---
1. Кодировать слово
2. Декодировать слово
3. Выйти

Выберите опцию: 2
Закодированное слово (в двоичном виде): 100010100
Генераторный полином (в двоичном виде): 1011
Данные корректны.
Декодированное слово (bin): 100010, CRC: 100
Декодированное слово (dec): 34, CRC: 4
---

6. Проверим работу при ошибке в слове при декодировании
Наша закодированное слово: 100010100
Закодированное слово с ошибкой: 100010101

Получим ответ:

---
1. Кодировать слово
2. Декодировать слово
3. Выйти

Выберите опцию: 2
Закодированное слово (в двоичном виде): 100010101
Генераторный полином (в двоичном виде): 1011
Данные повреждены.
Декодированное слово (bin): 100010, CRC: 101
Декодированное слово (dec): 34, CRC: 5
---


"""
