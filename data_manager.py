from datetime import datetime

import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal
from Common import *
from Config import GLOBAL_CONFIG
from Device import BlueToothDevice, SimulateLeftDevice


class DataManager(QObject):
	send_left_plot_data_signal = pyqtSignal(np.ndarray)
	send_right_plot_data_signal = pyqtSignal(np.ndarray)
	left_connected_signal = pyqtSignal(bool)
	right_connected_signal = pyqtSignal(bool)
	force_stop_recording_signal = pyqtSignal()

	twindow_result_signal = pyqtSignal(np.ndarray)
	trial_result_signal = pyqtSignal(int, int)

	def __init__(self):
		super().__init__()
		self.sample_rate = GLOBAL_CONFIG.sample_rate
		self.trans_rate = GLOBAL_CONFIG.trans_rate
		self.refresh_rate = REFRESH_RATE

		self.left_channel_num = GLOBAL_CONFIG.left_channel_num
		self.right_channel_num = GLOBAL_CONFIG.right_channel_num

		self.filter = GLOBAL_CONFIG.filter
		self.fmin = GLOBAL_CONFIG.fmin
		self.fmax = GLOBAL_CONFIG.fmax

		self.left_data = None
		self.left_data_index = 0
		self.right_data = None
		self.right_data_index = 0
		self.markers = []
		self.start_time = datetime.now()

		self.left_plot_buffer = None
		self.right_plot_buffer = None

		self.left_device = None
		self.right_device = None
		

		self.twindow_classify_probs = None
		self.twindow_index = 0
		self.twindow_num = 0
		self.movement_index = 0
		self.model = None

		self.__init_left_device()
		self.__init_right_device()
		self.__init_data()
	def __init_left_device(self):
		# 如果之前有过设备，则需要将之前的信号断连以防意外
		# if self.left_device:
		# 	self.left_device.disconnect()
		# 初始化设备Device实例
		self.left_device = BlueToothDevice()
		# self.left_device = SimulateLeftDevice()
		# 连接从设备接收到的数据信号
		self.left_device.receive_data_signal.connect(self.receive_data_from_device)
	def __init_right_device(self):
		if self.right_device:
			self.right_device.disconnect()
		# self.right_device = BlueToothDevice()
		self.right_device = SimulateLeftDevice()
		self.right_device.receive_data_signal.connect(self.receive_data_from_device)
		
	def __init_data(self):
		self.left_data = np.zeros((0, self.left_channel_num))
		self.left_data_index = 0
		self.start_time = datetime.now()
		self.markers = []
		self.left_plot_buffer = np.zeros((int(MAX_TIME_WINDOW * self.sample_rate), self.left_channel_num))
		self.right_plot_buffer = np.zeros((int(MAX_TIME_WINDOW * self.sample_rate), self.right_channel_num))
	def connect_left_device(self):
		try:
			connected = self.left_device.device_connect()
			GLOBAL_CONFIG.change_left_device_connect_state(connected)
			self.left_connected_signal.emit(connected)
		except Exception as e:
			# 处理异常情况，例如连接失败
			GLOBAL_CONFIG.change_left_device_connect_state(False)
			self.left_connected_signal.emit(False)
			print(f"连接失败: {e}")
	def connect_right_device(self):
		if self.right_device:
			connected = self.right_device.device_connect()
			GLOBAL_CONFIG.change_right_connect_state(connected)
			self.right_connected_signal.emit(connected)

	def disconnect_left_device(self):
		if GLOBAL_CONFIG.is_recording:
			self.force_stop_recording_signal.emit()
		self.left_device.device_disconnect()
		GLOBAL_CONFIG.change_left_connect_state(False)
		self.left_connected_signal.emit(False)
		
	def disconnect_right_device(self):
		if GLOBAL_CONFIG.is_recording:
			self.force_stop_recording_signal.emit()
		if self.right_device:
			self.right_device.device_disconnect()
		GLOBAL_CONFIG.change_right_device_connect_state(False)
		self.right_connected_signal.emit(False)

	def start_record_device(self):
		GLOBAL_CONFIG.change_recording_state(True)
		self.__init_data()
		self.left_device.device_start_record()
		if self.right_device:
			self.right_device.device_start_record()
			
	def stop_record_device(self):
		GLOBAL_CONFIG.change_recording_state(False)
		self.left_device.device_stop_record()
		if self.right_device:
			self.right_device.device_stop_record()

	def on_filter_changed(self):
		self.filter = GLOBAL_CONFIG.filter
		self.fmin = GLOBAL_CONFIG.fmin
		self.fmax = GLOBAL_CONFIG.fmax

	def on_channel_changed(self):
		self.left_channel_num = GLOBAL_CONFIG.left_channel_num
		self.right_channel_num = GLOBAL_CONFIG.right_channel_num
		self.__init_data()

	def receive_data_from_device(self, sample, sample_type):
		# sample的长度是固定的，根据传输率
		if sample_type == 'left':
			self.left_data = np.concatenate((self.left_data, sample), axis = 0)
			assert len(sample) == (self.sample_rate // self.trans_rate)
			self.left_data_index += len(sample)
			self.send_left_plot_data(sample.copy())
	
		elif sample_type == 'right':
			self.right_data = np.concatenate((self.right_data, sample), axis = 0)
			assert len(sample) == (self.sample_rate // self.trans_rate)
			self.right_data_index += len(sample)
			self.send_right_plot_data(sample.copy())
	def send_left_plot_data(self, plot_sample):
		# 基线校正
		base_line = np.mean(self.left_data[: len(plot_sample), :], axis = 0, keepdims = True)
		plot_sample -= base_line

		# 加入buffer，并设置plot_data_buffer最大长度
		self.left_plot_buffer = np.concatenate((self.left_plot_buffer, plot_sample), axis = 0)
		self.left_plot_buffer = self.left_plot_buffer[-int(MAX_TIME_WINDOW * self.sample_rate):]
		plot_data = self.left_plot_buffer.copy()
		# 对EEG数据进行滤波
		if self.filter:
			plot_data = band_pass_filter(plot_data, axis = 0, fs = self.sample_rate, fmin = self.fmin,
										 fmax = self.fmax)
		self.send_left_plot_data_signal.emit(plot_data)
		
	def send_right_plot_data(self, plot_sample):
		base_line = np.mean(self.right_data[: len(plot_sample), :], axis = 0, keepdims = True)
		plot_sample -= base_line
		self.right_plot_buffer = np.concatenate((self.right_plot_buffer, plot_sample), axis = 0)
		self.right_plot_buffer = self.right_plot_buffer[-int(MAX_TIME_WINDOW * self.sample_rate):]
		plot_data = self.right_plot_buffer.copy()
		if self.filter:
			plot_data = band_pass_filter(plot_data, axis = 0, fs = self.sample_rate, fmin = self.fmin,
										 fmax = self.fmax)
		self.send_right_plot_data_signal.emit(plot_data)

	
	