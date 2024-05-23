import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QMessageBox, \
    QHBoxLayout
from PyQt5.QtGui import QFont, QColor, QPalette
from datetime import datetime


class KrediNotuHesaplama(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Kredi Notu Hesaplama")
        self.setGeometry(100, 100, 600, 400)  # Pencere boyutları 

        # Arka plan rengini sarı olarak ayarlayın
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(255, 255, 0))
        self.setPalette(palette)

        layout = QVBoxLayout()

        header_label = QLabel("Kredi Notu Hesaplama Sistemi")
        header_label.setFont(QFont("Arial", 24, QFont.Bold))
        header_label.setStyleSheet("color: #4b0082;")  # Koyu mor renk
        layout.addWidget(header_label)
        layout.addSpacing(20)

        # Gelir
        gelir_layout = QHBoxLayout()
        gelir_label = QLabel("Gelir:")
        gelir_label.setFont(QFont("Arial", 14))
        self.gelir_input = QLineEdit()
        self.gelir_input.setFont(QFont("Arial", 14))
        gelir_layout.addWidget(gelir_label)
        gelir_layout.addWidget(self.gelir_input)
        layout.addLayout(gelir_layout)

        # Borç
        borc_layout = QHBoxLayout()
        borc_label = QLabel("Borç:")
        borc_label.setFont(QFont("Arial", 14))
        self.borc_input = QLineEdit()
        self.borc_input.setFont(QFont("Arial", 14))
        borc_layout.addWidget(borc_label)
        borc_layout.addWidget(self.borc_input)
        layout.addLayout(borc_layout)

        # İstihdam Durumu
        istihdam_layout = QHBoxLayout()
        istihdam_label = QLabel("İstihdam Durumu:")
        istihdam_label.setFont(QFont("Arial", 14))
        self.istihdam_combo = QComboBox()
        self.istihdam_combo.addItems(["tam_zamanli", "yarı_zamanli", "issiz"])
        self.istihdam_combo.setFont(QFont("Arial", 14))
        istihdam_layout.addWidget(istihdam_label)
        istihdam_layout.addWidget(self.istihdam_combo)
        layout.addLayout(istihdam_layout)

        # Yaş
        yas_layout = QHBoxLayout()
        yas_label = QLabel("Yaş:")
        yas_label.setFont(QFont("Arial", 14))
        self.yas_input = QLineEdit()
        self.yas_input.setFont(QFont("Arial", 14))
        yas_layout.addWidget(yas_label)
        yas_layout.addWidget(self.yas_input)
        layout.addLayout(yas_layout)

        # Hesaplama Butonu
        self.hesapla_button = QPushButton("Kredi Notunu Hesapla")
        self.hesapla_button.setFont(QFont("Arial", 14))
        self.hesapla_button.setStyleSheet("background-color: #4b0082; color: white;")
        self.hesapla_button.clicked.connect(self.kredi_notu_hesapla)
        layout.addWidget(self.hesapla_button)
        layout.addSpacing(20)

        self.setLayout(layout)

    def kredi_notu_hesapla(self):
        try:
            gelir = float(self.gelir_input.text())
            borc = float(self.borc_input.text())
            istihdam_durumu = self.istihdam_combo.currentText()
            yas = int(self.yas_input.text())

            AGIRLIK_GELIR = 0.3
            AGIRLIK_BORC = 0.25
            AGIRLIK_ISTIHDAM = 0.1
            AGIRLIK_YAS = 0.05

            if gelir >= 60000:
                gelir_puan = 10
            elif gelir >= 30000:
                gelir_puan = 8
            elif gelir >= 15000:
                gelir_puan = 5
            else:
                gelir_puan = 2

            if borc == 0:
                borc_puan = 10
            elif borc <= 5000:
                borc_puan = 8
            elif borc <= 20000:
                borc_puan = 5
            else:
                borc_puan = 2



            if istihdam_durumu == "tam_zamanli":
                istihdam_puan = 10
            elif istihdam_durumu == "yarı_zamanli":
                istihdam_puan = 5
            else:
                istihdam_puan = 2

            if yas >= 18 and yas <= 25:
                yas_puan = 5
            elif yas <= 35:
                yas_puan = 8
            elif yas <= 50:
                yas_puan = 10
            else:
                yas_puan = 6

            kredi_notu = (gelir_puan * AGIRLIK_GELIR +
                          borc_puan * AGIRLIK_BORC +
                          istihdam_puan * AGIRLIK_ISTIHDAM +
                          yas_puan * AGIRLIK_YAS)

            kredi_notu = round(kredi_notu, 2)

            # Hesaplama işlemlerini ve kredi notunu log dosyasına kaydetme
            with open("kredi_notu_log.txt", "a") as log_file:
                log_file.write(f"{datetime.now()}: Gelir: {gelir}, Borç: {borc} "
                               f"İstihdam: {istihdam_durumu}, Yaş: {yas}, Kredi Notu: {kredi_notu}\n")

            # Kredi notunu ayrı bir dosyaya kaydetme
            with open("kredi_notu_sonuclar.txt", "a") as result_file:
                result_file.write(f"{datetime.now()}: Kredi Notu: {kredi_notu}\n")

            QMessageBox.information(self, "Kredi Notu", f"Kredi Notu: {kredi_notu}")
        except ValueError:
            QMessageBox.critical(self, "Hata", "Lütfen tüm alanları doğru şekilde doldurun.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = KrediNotuHesaplama()
    ex.show()
    sys.exit(app.exec_())
