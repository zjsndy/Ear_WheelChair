import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal

from Config import GLOBAL_CONFIG


class Device(QThread):
    receive_data_signal = pyqtSignal(np.ndarray, str)

    def __init__(self):
        super().__init__()
        self.sample_rate = GLOBAL_CONFIG.sample_rate
        self.trans_rate = GLOBAL_CONFIG.trans_rate

    def device_connect(self):
        pass

    def device_disconnect(self):
        pass

    def device_start_record(self):
        pass

    def device_stop_record(self):
        pass

    def receive_data(self, sample):
        pass
