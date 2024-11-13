import asyncio

from PyQt5.QtCore import QThread, pyqtSignal
from bleak import BleakScanner


class scanbluetooth(QThread):
	scanFinished = pyqtSignal(list)
	
	def __init__(self):
		super(scanbluetooth, self).__init__()
	
	def run(self):
		# 使用 asyncio 运行异步函数
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		devices = loop.run_until_complete(BleakScanner.discover(timeout = 1))
		self.scanFinished.emit(devices)
