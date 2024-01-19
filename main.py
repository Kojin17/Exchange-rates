import sys
import requests
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QTabWidget
from PySide6.QtGui import QDoubleValidator, QFont
from PySide6.QtCore import Qt, QEvent

class CurrencyConverterApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Конвертер валют')
        self.setFixedSize(600, 400)
        self.setStyleSheet("""
            QWidget {
                background-color: #333;
                color: #fff;
            }

            QLabel {
                font-size: 14px;
                margin-bottom: 5px;
                color: #fff;
            }

            QLineEdit, QComboBox {
                font-size: 14px;
                padding: 5px;
                margin-bottom: 10px;
                background-color: #fff;
                color: #000;
                border-radius: 5px;
            }

            QPushButton {
                font-size: 14px;
                height: 40px;
                width: 200px;
                margin-bottom: 10px;
                background-color: #fff;
                color: #000;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #ddd;
            }

            #resultField, #resultCryptoField {
                font-size: 16px;
                padding: 5px;
                background-color: #fff;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
        """)

        # Создаем виджеты для денежных валют
        self.label_amount_currency = QLabel('Введите значение:')
        self.entry_amount_currency = QLineEdit()
        self.from_currency = QComboBox()
        self.to_currency = QComboBox()
        self.button_convert = QPushButton('Конвертировать')
        self.button_swap = QPushButton('Поменять валюты местами')
        self.label_result_currency = QLabel('Результат:')
        self.result_field_currency = QLineEdit()
        self.result_field_currency.setReadOnly(True)

        # Заполняем выпадающие списки валют
        currencies = ['USD', 'EUR', 'JPY', 'CNY', 'RUB', 'GBP', 'AED', 'CHF']
        self.from_currency.addItems(currencies)
        self.to_currency.addItems(currencies)

        # Устанавливаем валидатор для ввода только чисел
        double_validator_currency = QDoubleValidator()
        double_validator_currency.setNotation(QDoubleValidator.StandardNotation)
        self.entry_amount_currency.setValidator(double_validator_currency)

        # Устанавливаем поле ввода по середине
        self.entry_amount_currency.setAlignment(Qt.AlignHCenter)

        # Увеличиваем шрифт для полей ввода
        font_currency = QFont()
        font_currency.setPointSize(16)
        self.entry_amount_currency.setFont(font_currency)
        self.result_field_currency.setFont(font_currency)

        # Создаем компоновщик интерфейса для денежных валют
        layout_currency = QVBoxLayout()
        layout_currency.addWidget(self.label_amount_currency, alignment=Qt.AlignHCenter)
        layout_currency.addWidget(self.entry_amount_currency, alignment=Qt.AlignHCenter)
        layout_currency.addWidget(self.label_result_currency, alignment=Qt.AlignHCenter)
        layout_currency.addWidget(self.result_field_currency, alignment=Qt.AlignHCenter)
        layout_currency.addWidget(self.from_currency, alignment=Qt.AlignHCenter)
        layout_currency.addWidget(self.to_currency, alignment=Qt.AlignHCenter)
        layout_currency.addWidget(self.button_convert, alignment=Qt.AlignHCenter)
        layout_currency.addWidget(self.button_swap, alignment=Qt.AlignHCenter)

        # Создаем виджет для денежных валют
        widget_currency = QWidget()
        widget_currency.setLayout(layout_currency)

        # Создаем виджеты для криптовалют
        self.label_choose_crypto = QLabel('Выберите криптовалюту:')
        self.crypto_currency = QComboBox()
        self.label_amount_crypto = QLabel('Введите значение:')
        self.entry_amount_crypto = QLineEdit()
        self.button_convert_crypto = QPushButton('Конвертировать')
        self.label_result_crypto = QLabel('Результат:')
        self.result_crypto_field = QLineEdit()
        self.result_crypto_field.setReadOnly(True)

        # Заполняем выпадающий список криптовалют
        crypto_currencies = ['Bitcoin', 'Ethereum']
        self.crypto_currency.addItems(crypto_currencies)

        # Устанавливаем поле ввода по середине
        self.entry_amount_crypto.setAlignment(Qt.AlignHCenter)

        # Увеличиваем шрифт для полей ввода
        font_crypto = QFont()
        font_crypto.setPointSize(16)
        self.entry_amount_crypto.setFont(font_crypto)
        self.result_crypto_field.setFont(font_crypto)

        # Создаем компоновщик интерфейса для криптовалют
        layout_crypto = QVBoxLayout()
        layout_crypto.addWidget(self.label_amount_crypto, alignment=Qt.AlignHCenter)
        layout_crypto.addWidget(self.entry_amount_crypto, alignment=Qt.AlignHCenter)
        layout_crypto.addWidget(self.label_choose_crypto, alignment=Qt.AlignHCenter)
        layout_crypto.addWidget(self.crypto_currency, alignment=Qt.AlignHCenter)
        layout_crypto.addWidget(self.label_result_crypto, alignment=Qt.AlignHCenter)
        layout_crypto.addWidget(self.result_crypto_field, alignment=Qt.AlignHCenter)
        layout_crypto.addWidget(self.button_convert_crypto, alignment=Qt.AlignHCenter)

        # Создаем виджет для криптовалют
        widget_crypto = QWidget()
        widget_crypto.setLayout(layout_crypto)

        # Создаем виджет вкладок и добавляем созданные виджеты
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(widget_currency, 'Денежные валюты')
        self.tab_widget.addTab(widget_crypto, 'Криптовалюты')

        # Создаем главный компоновщик интерфейса
        layout_main = QVBoxLayout()
        layout_main.addWidget(self.tab_widget)

        # Устанавливаем компоновщик для основного виджета
        self.setLayout(layout_main)

        # Подключаем обработчики событий
        self.button_convert.clicked.connect(self.convert_currency)
        self.button_swap.clicked.connect(self.swap_currencies)
        self.button_convert_crypto.clicked.connect(self.convert_crypto_currency)

        # Обработчики для клавиш Enter и Esc
        self.installEventFilter(self)

        # Устанавливаем цвет шрифта для вкладок
        self.tab_widget.setStyleSheet("QTabWidget QTabBar::tab { color: black; }")

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Escape:
                self.close()
            elif event.key() in (Qt.Key_Enter, Qt.Key_Return):
                if self.tab_widget.currentIndex() == 0:
                    self.convert_currency()
                elif self.tab_widget.currentIndex() == 1:
                    self.convert_crypto_currency()

        return super().eventFilter(obj, event)

    def convert_currency(self):
        try:
            amount = float(self.entry_amount_currency.text())
            from_currency = self.from_currency.currentText()
            to_currency = self.to_currency.currentText()

            api_key = "ba4eb9390342318d0ef7f3cb"
            base_url = f"https://open.er-api.com/v6/latest/{from_currency}"

            params = {
                "apikey": api_key,
                "symbols": to_currency
            }

            response = requests.get(base_url, params=params)

            if response.status_code == 200:
                data = response.json()
                exchange_rate = data["rates"].get(to_currency, 1.0)

                converted_amount = amount * exchange_rate
                self.result_field_currency.setText(f"{converted_amount:.2f} {to_currency}")

            else:
                self.result_field_currency.setText("Ошибка: Невозможно получить курсы валют.")

        except ValueError:
            self.result_field_currency.setText("Ошибка: Введите корректное число.")

    def swap_currencies(self):
        from_currency_index = self.from_currency.currentIndex()
        to_currency_index = self.to_currency.currentIndex()

        self.from_currency.setCurrentIndex(to_currency_index)
        self.to_currency.setCurrentIndex(from_currency_index)

        self.convert_currency()

    def convert_crypto_currency(self):
        try:
            amount_text = self.entry_amount_crypto.text()
            if not amount_text:
                raise ValueError("Введите корректное число.")

            amount = float(amount_text)
            crypto_currency = self.crypto_currency.currentText()

            base_url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_currency.lower()}&vs_currencies=usd"
            response = requests.get(base_url)

            if response.status_code == 200:
                data = response.json()
                exchange_rate = data.get(crypto_currency.lower(), {}).get("usd", 1.0)

                converted_amount = amount * exchange_rate
                self.result_crypto_field.setText(f"{converted_amount:.2f} USD")
            else:
                self.result_crypto_field.setText("Ошибка: Невозможно получить курс криптовалюты в долларах.")
        except ValueError as e:
            self.result_crypto_field.setText(f"Ошибка: {e}")

def main():
    app = QApplication(sys.argv)
    converter_app = CurrencyConverterApp()
    converter_app.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
