from PyQt5.QtGui import QPaintEvent, QPainter
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGridLayout, QVBoxLayout, QStyleOption, QStyle


class ControlTab(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.__init_ui()
		
	def __init_ui(self):
		self.layout = QHBoxLayout()
		self.input_layout = QGridLayout()
		self.config_layout = QVBoxLayout()
		self.config_widget = QWidget()
	
	def paintEvent(self, a0: QPaintEvent) -> None:
		opt = QStyleOption()
		opt.initFrom(self)
		painter = QPainter(self)
		self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, painter, self)
		