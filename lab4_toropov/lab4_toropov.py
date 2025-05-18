"""
Лабораторная работа №4

QR и штрих код

Торопов Арсений Алексеевич РИ-320934
"""

import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)
from PyQt5.QtGui import QPixmap
import qrcode
import barcode
from barcode.writer import ImageWriter
import os
import tempfile
import shutil


class CodeGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Генератор QR- и Штрих-кодов")
        self.resize(400, 600)

        self.layout = QVBoxLayout()

        # Поле ввода
        self.input_line = QLineEdit(self)
        self.input_line.setPlaceholderText("Введите текст для кодирования...")
        self.input_line.textChanged.connect(self.on_input_changed)
        self.layout.addWidget(self.input_line)

        # QR-код
        self.qr_label = QLabel("QR-код:")
        self.layout.addWidget(self.qr_label)
        self.qr_image_label = QLabel(self)
        self.layout.addWidget(self.qr_image_label)

        # Штрих-код
        self.barcode_label = QLabel("Штрих-код:")
        self.layout.addWidget(self.barcode_label)
        self.barcode_image_label = QLabel(self)
        self.layout.addWidget(self.barcode_image_label)

        self.setLayout(self.layout)

    def on_input_changed(self):
        text = self.input_line.text()
        if text:
            self.generate_qr_code(text)
            self.generate_barcode()

    def generate_qr_code(self, text):
        qr = qrcode.make(text)
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            qr.save(tmp.name)
            pixmap = QPixmap(tmp.name).scaledToWidth(200)
            self.qr_image_label.setPixmap(pixmap)
            os.unlink(tmp.name)

    def generate_barcode(self):
        text = self.input_line.text()
        if not text:
            return

        try:
            ean = barcode.get_barcode_class("code128")
            bc = ean(text, writer=ImageWriter())
            options = {
                "module_width": 0.4,
                "module_height": 10.0,
                "quiet_zone": 1,
                "font_size": 10,
                "text_distance": 5,
                "background": "white",
                "foreground": "black",
                "write_text": True,
            }

            temp_dir = tempfile.mkdtemp()
            filename = os.path.join(temp_dir, "barcode")
            bc.save(filename, options=options)

            img_path = filename + ".png"
            pixmap = QPixmap(img_path).scaledToWidth(300)
            self.barcode_image_label.setPixmap(pixmap)

            shutil.rmtree(temp_dir)
        except Exception as e:
            print("Ошибка при генерации штрих-кода:", e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CodeGeneratorApp()
    window.show()
    sys.exit(app.exec_())
