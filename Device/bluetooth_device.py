import asyncio
from datetime import time


import numpy as np
from PyQt5.QtCore import QThread
from bleak import BleakClient

from Config import GLOBAL_CONFIG
from .device import Device
from Common import *

class BlueToothDevice(Device):
	
	def __init__(self):
		super().__init__()
		self.is_running = False
		self.connection = None
		self.data_buffer = None
		#写死了，后续再优化
		self.device_address = GLOBAL_CONFIG.left_device_address
		
	async def device_connect(self):
		try:
			self.connection = BleakClient(self.device_address)
			await self.connection.connect()
			if self.connection.is_connected:
				print("连接成功:")
				self.is_running = True
				self.start()
				return True
			else:
				print("连接失败：设备未连接")
				self.connection = None
				self.is_running = False
				return False
		except Exception as e:
			self.connection = None
			self.is_running = False
			print(f"连接失败: {e}")
			return False


	def device_start_record(self):
		self.data_buffer = np.zeros((0, 1))
	
	async def run(self):
		"""
		启动数据通知接收，并每 25 个数据点计算一次 Alpha/Beta 比例。

		参数:
			client (BleakClient): 已连接的蓝牙客户端
			total_data (list): 存储所有接收到的数据
			sample_buffer (list): 用于存储当前 25 个点的数据缓冲
			device_name (str): 设备名称，用于日志显示
		"""
		# buffer = bytearray()  # 每个设备独立的缓冲区
		# last_ratio = None  # 保存上一次的 ratio 值

		async def notification_handler(data):
			# nonlocal buffer, last_ratio
			if data[:4] != bytearray([0xff, 0xff, 0x01, 0x1f]) and len(self.data_buffer) == 0:
				print("帧头不正确，丢弃数据")
			else:
				self.data_buffer.extend(data)
				if len(self.data_buffer) >= 35:
					complete_data = self.data_buffer[:35]
					self.data_buffer = self.data_buffer[35:]
					pts = parse_earphone_data_frame(complete_data)
				
					if GLOBAL_CONFIG.is_recording:
						trans_length = self.sample_rate // self.trans_rate
						# sample = np.array(pts).reshape((-1, 1)) * self.channelResolutions
						# self.data_buffer = np.concatenate((self.data_buffer, sample), axis = 0)
						# if len(self.data_buffer) >= trans_length:
						# 	send_sample = self.data_buffer[:trans_length]
						# 	self.data_buffer = self.data_buffer[trans_length:]
						# 	self.receive_data(send_sample.copy())
					# if pts is not None:
					# 	total_data.append(pts)
					# 	sample_buffer.append(pts)
					# 	# 累积到 5 个点后判断刹车
					# 	if len(sample_buffer) >= 5:
					# 		flattened_data = np.concatenate(sample_buffer).flatten()
					# 		stop = filter_and_get_amplitude(flattened_data, fs = 500, lowcut = 2, highcut = 45,
					# 										threshold = 22,
					# 										window_size = 10)
					# 		if stop == True:
					# 			controller.current_state = '0'
					# 			# 清空样本缓冲区
					# 			sample_buffer.clear()
					#
					# 	# 累积到 25 个点后计算 Alpha/Beta 比例
					# 	if len(sample_buffer) >= 25:
					# 		flattened_data = np.concatenate(sample_buffer).flatten()
					# 		alpha_power = band_calculator.calculate_band_power(flattened_data, (8, 13))
					# 		beta_power = band_calculator.calculate_band_power(flattened_data, (13, 30))
					# 		ratio = alpha_power / beta_power if beta_power != 0 else np.inf
					# 		print(f"{device_name} Alpha/Beta Ratio: {ratio:.2f}")
					#
					# 		# 判断alpha波和beta波的波动
					# 		if last_ratio is not None and ratio >= 1.5 * last_ratio and 1 <= ratio <= 3:
					# 			controller.current_state = '1'
					# 			print(f"{device_name} Ratio increased by 3x or more: {ratio:.2f}")
					#
					# 		# 更新 last_ratio
					# 		last_ratio = ratio
					#
					# 		# 清空样本缓冲区
					# 		sample_buffer.clear()
		
		await self.connection.start_notify(NOTIFY_UUID, notification_handler)
		print(" 开始接收数据")
		
		# 接收数据 360 秒
		await asyncio.sleep(360)
		await self.connection.stop_notify(NOTIFY_UUID)
	
	
	#	def __init__(self):
	# 	super().__init__()
	# 	self.is_running = False
	# 	self.connection = None
	#
	# 	self.lastBlock = -1
	# 	self.channelResolutions = None
	# 	self.channelCount = 0
	# 	self.data_buffer = None
	#
	# def device_connect(self):
	# 	try:
	# 		self.connection = socket(AF_INET, SOCK_STREAM)
	# 		self.connection.connect(("localhost", 51244))
	# 		print("BP device connect done.")
	# 		self.is_running = True
	# 		self.start()
	# 		return True
	# 	except AttributeError:
	# 		self.connection = None
	# 		print("Connect error, please recheck.")
	# 		return False
	#
	# def device_start_record(self):
	# 	self.data_buffer = np.zeros((0, self.channelCount))
	#
	# def run(self):
	# 	while self.is_running:
	# 		try:
	# 			# Get message header as raw array of chars
	# 			rawhdr = RecvData(self.connection, 24)
	# 			# Split array into usefully information id1 to id4 are constants
	# 			(id1, id2, id3, id4, msgsize, msgtype) = unpack('<llllLL', rawhdr)
	# 			# Get data part of message, which is of variable size
	# 			rawdata = RecvData(self.connection, msgsize - 24)
	# 		except:
	# 			print('connection error!')
	# 			continue
	#
	# 		# Perform action dependent on the message type
	# 		if msgtype == 1:
	# 			# Start message, extract eeg properties and display them
	# 			(channelCount, samplingInterval, resolutions, channelNames) = GetProperties(rawdata)
	# 			print("Start")
	# 			print("Number of channels: " + str(channelCount))
	# 			print("Sampling interval: " + str(samplingInterval))
	# 			print("Resolutions: " + str(resolutions))
	# 			print("Channel Names: " + str(channelNames))
	# 			self.lastBlock = -1
	# 			self.channelResolutions = np.array(resolutions)
	# 			self.channelCount = channelCount
	# 			self.data_buffer = np.zeros((0, self.channelCount))
	#
	# 		elif msgtype == 4:
	# 			# Data message, extract data and markers
	# 			(block, points, markerCount, data, markers) = GetData(rawdata, self.channelCount)
	# 			# Check for overflow
	# 			if self.lastBlock != -1 and block > self.lastBlock + 1:
	# 				print("Overflow with " + str(block - self.lastBlock) + " data blocks!")
	# 			self.lastBlock = block
	# 			# Print markers, if there are some in actual block
	# 			if markerCount > 0:
	# 				for m in range(markerCount):
	# 					print("Marker " + markers[m].description + " of type " + markers[m].type)
	#
	# 			if GLOBAL_CONFIG.is_recording:
	# 				trans_length = self.eeg_sample_rate // self.trans_rate
	# 				sample = np.array(data).reshape((-1, self.channelCount)) * self.channelResolutions
	# 				self.data_buffer = np.concatenate((self.data_buffer, sample), axis = 0)
	# 				if len(self.data_buffer) >= trans_length:
	# 					send_sample = self.data_buffer[:trans_length]
	# 					self.data_buffer = self.data_buffer[trans_length:]
	# 					self.receive_data(send_sample.copy())
	#
	# 		elif msgtype == 3:
	# 			# Stop message, terminate program
	# 			self.is_running = False
	# 			print("Stop")
	#
	# def device_stop_record(self):
	# 	pass
	#
	# def device_disconnect(self):
	# 	if self.connection:
	# 		self.is_running = False
	# 		self.connection.close()
	#
	# def receive_data(self, sample):
	# 	# 发送EEG和EMG的数据
	# 	self.receive_data_signal.emit(sample[:, :GLOBAL_CONFIG.left_channel_num], 'left')
	# 	self.receive_data_signal.emit(sample[:, -GLOBAL_CONFIG.right_channel_num:], 'right')
