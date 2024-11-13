from unittest.mock import DEFAULT

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QFileDialog

from Common import *


class GlobalConfig(QObject):
	left_device_changed_signal = pyqtSignal()
	right_device_changed_signal = pyqtSignal()

	plot_twindow_changed_signal = pyqtSignal()
	channel_scale_changed_signal = pyqtSignal()
	filter_changed_signal = pyqtSignal()
	config_input_changed_signal = pyqtSignal()
	
	def __init__(self):
		super().__init__()
		
		self.left_device_address = DEFAULT_CONFIG["left_device_address"]
		self.right_device_address = DEFAULT_CONFIG["right_device_address"]
		
		self.trans_rate = TRANS_RATE
		self.sample_rate = SAMPLE_RATE
		
		self.left_channel_num  = DEFAULT_CONFIG["left_channel_num"]
		self.left_channel_name = DEFAULT_CONFIG["left_channel_name"]
		self.right_channel_num  = DEFAULT_CONFIG["right_channel_num"]
		self.right_channel_name = DEFAULT_CONFIG["right_channel_name"]
		
		self.plot_twindow = DEFAULT_CONFIG["plot_twindow"]
		self.channel_scale = DEFAULT_CONFIG["channel_scale"]
		self.filter = DEFAULT_CONFIG["filter"]
		self.fmin = DEFAULT_CONFIG["fmin"]
		self.fmax = DEFAULT_CONFIG["fmax"]
		
		self.trial = DEFAULT_CONFIG["trial"]
		self.paradigm = DEFAULT_CONFIG["paradigm"]
		self.rest_time = DEFAULT_CONFIG["rest_time"]
		self.cue_time = CUE_TIME
		self.perform_time = DEFAULT_CONFIG["perform_time"]
		
		self.is_left_device_connected = False
		self.is_right_device_connected = False
		self.is_recording = False
		self.is_exp = False
		
	def change_plot_twindow(self, time_window):
		if time_window != self.plot_twindow:
			self.plot_twindow = time_window
			self.plot_twindow_changed_signal.emit()
	
	def change_channel_scale(self, channel_scale):
		if channel_scale != self.channel_scale:
			self.channel_scale = channel_scale
			self.channel_scale_changed_signal.emit()
	
	def change_filter(self, filter_, fmin, fmax):
		if filter_ != self.filter or self.fmin != fmin or self.fmax != fmax:
			self.filter = filter_
			self.fmin = fmin
			self.fmax = fmax
			self.filter_changed_signal.emit()
	
	def change_paradigm(self, paradigm):
		if paradigm != self.paradigm:
			self.paradigm = paradigm
	
	def change_exp_config(self, trial, perform_time, rest_time):
		self.trial = trial
		self.perform_time = perform_time
		self.rest_time = rest_time
	
	def change_recording_state(self, is_recording):
		self.is_recording = is_recording
	
	def change_exp_state(self, is_exp):
		self.is_exp = is_exp
	
	def change_left_device_connect_state(self, is_connected):
		self.is_left_device_connected = is_connected
		
	def change_right_device_connect_state(self, is_connected):
		self.is_right_device_connected = is_connected
		
GLOBAL_CONFIG = GlobalConfig()