"""
Лабораторная работа №2

Методы упаковки данных

Торопов Арсений Алексеевич РИ-320934

Мною был выбран второй метод архивации: LZW
"""

import struct


class LzwArchiver:
    """
    Создадим класс архиватора,
    который будет иметь два метода:
    архивирования и дезархивирования
    """

    def __init__(self, bit_size=12):
        self.bit_size = bit_size
        self.max_table_size = 2**self.bit_size

    @staticmethod
    def compress(input_path: str, output_path: str) -> bool:
        try:
            with open(input_path, "rb") as file:
                data = file.read()

            table = {bytes([i]): i for i in range(256)}
            next_code = 256
            result = []
            current_string = b""

            for byte in data:
                current_string += bytes([byte])
                if current_string not in table:
                    table[current_string] = next_code
                    next_code += 1

                    result.append(table[current_string[:-1]])
                    current_string = current_string[-1:]

            if current_string:
                result.append(table[current_string])

            with open(output_path, "wb") as out_file:
                for code in result:
                    out_file.write(struct.pack(">H", code))

            return True
        except Exception as e:
            print(f"Ошибка при сжатии: {e}")
            return False

    @staticmethod
    def decompress(input_path: str, output_path: str) -> bool:
        try:
            with open(input_path, "rb") as file:
                packed_data = file.read()

            codes = list(
                struct.unpack(">" + "H" * (len(packed_data) // 2), packed_data)
            )

            table = {i: bytes([i]) for i in range(256)}
            next_code = 256
            old_code = codes[0]
            decompressed = table[old_code]
            current_string = decompressed

            for code in codes[1:]:
                if code not in table:
                    entry = current_string + current_string[:1]
                else:
                    entry = table[code]

                decompressed += entry
                table[next_code] = table[old_code] + bytes([entry[0]])
                next_code += 1
                old_code = code
                current_string = entry

            with open(output_path, "wb") as out_file:
                out_file.write(decompressed)

            return True
        except Exception as e:
            print(f"Ошибка при распаковке: {e}")
            return False


if __name__ == "__main__":
    lzw = LzwArchiver()

    input_file = r"lzw_origin.txt"
    compressed_file = r"lzw_compressed.lzw"
    decompressed_file = r"lzw_decomressed.txt"

    if lzw.compress(input_file, compressed_file):
        print("Файл успешно сжат.")

    if lzw.decompress(compressed_file, decompressed_file):
        print("Файл успешно распакован.")

"""
Содержание исходного файла: 'Торопов Арсений Алексеевич'

Содержание файла после дезархивации: 'Торопов Арсений Алексеевич'
"""
