import time

import numpy as np

from Common import *
from Config import GLOBAL_CONFIG
from .device import Device


class SimulateLeftDevice(Device):

    def __init__(self):
        super().__init__()
        self.source_data_file = get_abs_path('data/ljm_1.npy')
        print(self.source_data_file)
        self.source_data = np.load(self.source_data_file).reshape((-1, 1))
        self.source_data_index = 0

        self.t0 = 0
        self.cnt = 0

    def device_connect(self):
        return True

    def device_disconnect(self):
        pass

    def device_start_record(self):
        self.start()

    def device_stop_record(self):
        GLOBAL_CONFIG.change_recording_state(False)

    def run(self):
        self.t0 = time.time()
        self.cnt = 0
        # print(GLOBAL_CONFIG.is_recording)
        # while GLOBAL_CONFIG.is_recording:
        while(True):
            data_length = self.sample_rate // self.trans_rate
            simulate_sample = self.source_data[self.source_data_index: self.source_data_index + data_length,
                              :GLOBAL_CONFIG.left_channel_num].copy()
            self.receive_data(simulate_sample)
            self.source_data_index += data_length
            if self.source_data_index >= len(self.source_data):
                self.source_data_index = 0

            # 计算时间差，用来校准时间
            self.cnt += 1
            delta = self.t0 + self.cnt * (1000 // self.trans_rate / 1000) - time.time()
            if delta > 0:
                time.sleep(delta)

    def receive_data(self, sample):
        self.receive_data_signal.emit(sample, 'left')


class SimulateRightDevice(Device):

    def __init__(self):
        super().__init__()
        self.source_data_file = get_abs_path('data/my_list_1.npy')
        self.source_data = np.load(self.source_data_file)
        self.source_data_index = 0

        self.t0 = 0
        self.cnt = 0

    def device_connect(self):
        return True

    def device_disconnect(self):
        pass

    def device_start_record(self):
        self.start()

    def device_stop_record(self):
        GLOBAL_CONFIG.change_recording_state(False)

    def run(self):
        self.t0 = time.time()
        self.cnt = 0
        while GLOBAL_CONFIG.is_recording:
            data_length = self.sample_rate // self.trans_rate
            simulate_sample = self.source_data[self.source_data_index: self.source_data_index + data_length,
                              :GLOBAL_CONFIG.left_channel_num].copy()
            self.receive_data(simulate_sample)
            self.source_data_index += data_length
            if self.source_data_index >= len(self.source_data):
                self.source_data_index = 0
            self.cnt += 1
            delta = self.t0 + self.cnt * (1000 // self.trans_rate / 1000) - time.time()
            if delta > 0:
                time.sleep(delta)

    def receive_data(self, sample):
        self.receive_data_signal.emit(sample, 'right')
