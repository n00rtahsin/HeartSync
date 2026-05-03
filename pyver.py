import sys
import serial
import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets
from scipy.signal import butter, lfilter

# --- CONFIGURATION ---
SERIAL_PORT = 'COM7' 
BAUD_RATE = 115200
WINDOW_SIZE = 500

class ClinicalMonitor(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clinical Signal Processor")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: #0A0A0A;")

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.bpm_label = QtWidgets.QLabel("CALIBRATING...")
        self.bpm_label.setStyleSheet("font-size: 90px; color: #00FF41; font-family: 'Consolas';")
        self.bpm_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.bpm_label)

        self.graph = pg.PlotWidget()
        self.graph.setBackground('#0A0A0A')
        self.graph.setYRange(0, 300)
        self.layout.addWidget(self.graph)

        # Blue = Heartbeat, Yellow = Threshold
        self.curve = self.graph.plot(pen=pg.mkPen('#00BFFF', width=3))
        self.data_y = [0] * WINDOW_SIZE

        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
        except:
            print("Error: Port busy or disconnected.")
            sys.exit()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)

    # DIGITAL FILTER: Specifically removes 50Hz/60Hz sawtooth noise
    def lowpass_filter(self, data, cutoff=3.5, fs=100, order=2):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return lfilter(b, a, data)

    def update(self):
        try:
            while self.ser.in_waiting:
                line = self.ser.readline().decode('utf-8').strip()
                if "HEART RATE" in line:
                    val = line.split(":")[-1].strip().split(" ")[0]
                    self.bpm_label.setText(f"{val} BPM")
                elif "," in line:
                    raw_val = float(line.split(',')[0])
                    self.data_y = self.data_y[1:] + [raw_val]
                    
                    # Apply filter to smooth the GUI line
                    filtered = self.lowpass_filter(self.data_y)
                    self.curve.setData(filtered)
        except: pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = ClinicalMonitor()
    win.show()
    sys.exit(app.exec_())