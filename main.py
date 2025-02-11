import sys
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from interface import Ui_MainWindow  # Arquivo gerado pelo Qt Designer

class DHTApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Detecta automaticamente a porta do Arduino
        self.arduino = serial.Serial("COM5", 9600, timeout=1)  # Exemplo

        #self.arduino = self.detect_serial_port()

        # Criando um Timer para leitura contínua
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.read_serial_data)

        # Conectar o botão ao início da leitura
        self.ui.btn_start.clicked.connect(self.start_reading)

    def start_reading(self):
        """ Inicia a leitura dos dados do Arduino a cada 1 segundo """
        if self.arduino:
            self.timer.start(1000)  # Atualiza a cada 1s
    
    '''def read_serial_data(self):
        if self.arduino and self.arduino.in_waiting:
            try:
                linha = self.arduino.readline().decode(errors="ignore").strip()
                print(f"Recebido: {linha}")  # Debug para ver a saída

                if linha.startswith("Temperature="):
                    temperatura = linha.split('=')[1].strip()
                    self.ui.label_temp.setText(f"Temperatura: {temperatura}°C")
                elif linha.startswith("Humidity="):
                    umidade = linha.split('=')[1].strip()
                    self.ui.label_humi.setText(f"Umidade: {umidade}%")
                elif linha.startswith("Pressure="):
                    pressao = linha.split('=')[1].strip()
                    self.ui.label_press.setText(f"Pressão: {pressao} Pa")
                elif linha.startswith("Luminosidade="):
                    luminosidade = linha.split('=')[1].strip()
                    self.ui.label_lum.setText(f"Luminosidade: {luminosidade}")
            except Exception as e:
                print(f"Erro ao ler dados: {e}")'''
    

    def read_serial_data(self):
        """ Lê os dados da Serial e atualiza os Labels na GUI """
        if self.arduino and self.arduino.in_waiting:
            try:
                linha = self.arduino.readline().decode().strip()
                if "Temperature" in linha:
                    temperatura = linha.split('=')[1].strip()
                    self.ui.label_temp.setText(f"Temperatura: {temperatura}°C")
                elif "Humidity" in linha:
                    umidade = linha.split('=')[1].strip()
                    self.ui.label_humi.setText(f"Umidade: {umidade}%")
                elif "Pressure" in linha:
                    pressão = linha.split('=')[1].strip()
                    self.ui.label_press.setText(f"Pressão:{pressão}")
                elif "Luminosidade" in linha:
                    luminosidade = linha.split('=')[1].strip()
                    self.ui.label_lum.setText(f"{luminosidade}")
            except Exception as e:
                print(f"Erro ao ler dados: {e}")

    def closeEvent(self, event):
        """ Fecha a conexão serial ao sair """
        if self.arduino:
            self.arduino.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DHTApp()
    window.show()
    sys.exit(app.exec_())
