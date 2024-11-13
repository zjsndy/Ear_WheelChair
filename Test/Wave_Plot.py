import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow
import pyqtgraph as pg

class WaveformPlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('500Hz Waveform Plotter')

        # 创建一个PlotWidget
        self.plotWidget = pg.PlotWidget()
        self.setCentralWidget(self.plotWidget)

        # 设置PlotWidget的属性
        self.plotWidget.setRange(xRange=[0, 1000], yRange=[-1, 1])
        self.plotWidget.setLabel(axis='left', text='Amplitude')
        self.plotWidget.setLabel(axis='bottom', text='Time')

        # 生成500Hz的波形数据
        self.generateWaveform()

    def generateWaveform(self):
        # 生成时间序列
        t = np.linspace(0, 1, 1000, endpoint=False)  # 1秒的时间序列，1000个点

        # 生成500Hz的正弦波
        self.waveform = np.sin(2 * np.pi * 500 * t)

        # 绘制波形
        self.plotWidget.plot(self.waveform, pen='y')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WaveformPlotter()
    ex.show()
    sys.exit(app.exec_())