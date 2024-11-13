from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPaintEvent, QPainter
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGridLayout, QVBoxLayout, QStyleOption, QStyle
from Components import *
from Views.plotter.plotter import DataPlotWidget
from Config import GLOBAL_CONFIG

class VisualTab(QWidget):
	record_start_signal = pyqtSignal()
	record_stop_signal = pyqtSignal()
	def __init__(self, parent = None):
		super().__init__(parent=parent)
		self.layout = QHBoxLayout()
		self.input_layout = QGridLayout()
		self.config_layout = QVBoxLayout()
		self.plot_layout = QHBoxLayout()
		
		self.config_widget = QWidget(parent = self)
		self.left_plot_widget = None
		self.right_plot_widget = None
		self.__init_left_plot_widget()
		self.__init_right_plot_widget()
		
		self.twindow_input = InputSpinBox(min_value = MIN_TIME_WINDOW, max_value = MAX_TIME_WINDOW)
		self.scale_input = InputSpinBox(min_value = MIN_CHANNEL_SCALE, max_value = MAX_CHANNEL_SCALE, step_value = 5)
		self.filter_check_box = InputCheckBox(text = '设置带通滤波')
		self.fmax_input = InputDoubleSpinBox(min_value = MIN_FILTER, max_value = MAX_FILTER)
		self.fmin_input = InputDoubleSpinBox(min_value = MIN_FILTER, max_value = MAX_FILTER)
		self.apply_button = ClickButton(text = '保存设置', role = 'OK')
		self.record_control_button = CheckButton(check_text = '停止采集', uncheck_text = '开始采集')
		
		self.__init_ui()
		self.__init_slot()
		self.__set_config()

	def __init_ui(self):
		self.input_layout = QGridLayout()
		self.input_layout.addWidget(TextLabel(text = '时间窗口大小(s)'), 0, 0, 1, 4)
		self.input_layout.addWidget(self.twindow_input, 1, 0, 1, 4)
		self.input_layout.addWidget(TextLabel(text = '通道阈值(uV)'), 2, 0, 1, 4)
		self.input_layout.addWidget(self.scale_input, 3, 0, 1, 4)
		self.input_layout.addWidget(self.filter_check_box, 4, 0, 1, 4)
		self.input_layout.addWidget(TextLabel(text = '高通滤波(Hz)'), 5, 0, 1, 4)
		self.input_layout.addWidget(self.fmin_input, 6, 0, 1, 4)
		self.input_layout.addWidget(TextLabel(text = '低通滤波(Hz)'), 7, 0, 1, 4)
		self.input_layout.addWidget(self.fmax_input, 8, 0, 1, 4)
		self.input_layout.setHorizontalSpacing(10)
		self.input_layout.setVerticalSpacing(15)

		self.config_layout.addLayout(self.input_layout)
		self.config_layout.addStretch(1)
		self.config_layout.addWidget(self.apply_button)
		self.config_layout.addWidget(self.record_control_button)
		self.config_layout.setSpacing(15)
		self.config_layout.setContentsMargins(30, 30, 30, 30)

		self.config_widget.setFixedWidth(330)
		self.config_widget.setLayout(self.config_layout)
		self.config_widget.setObjectName('config_widget')
		self.config_widget.setStyleSheet('''
		            #config_widget{
		                border-right: 2 solid #eeeeee;
		            }
		        ''')


		self.__init_plot_layout()
		self.plot_layout.setContentsMargins(0, 0, 0, 0)

		self.layout.addWidget(self.config_widget,alignment = Qt.AlignLeft)
		self.layout.addLayout(self.plot_layout)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.setSpacing(0)
		self.setLayout(self.layout)
	def __init_slot(self):
		self.filter_check_box.stateChanged.connect(self.fmax_input.on_enable_changed)
		self.filter_check_box.stateChanged.connect(self.fmin_input.on_enable_changed)
		self.apply_button.clicked.connect(self.__on_apply_config)
		GLOBAL_CONFIG.plot_twindow_changed_signal.connect(self.on_plot_twindow_changed)
		GLOBAL_CONFIG.channel_scale_changed_signal.connect(self.on_channel_scale_changed)
		GLOBAL_CONFIG.config_input_changed_signal.connect(self.__set_config)
		self.record_control_button.clicked.connect(self.__on_record_control)
		self.record_start_signal.connect(self.__reset_plot_widget)


	def __init_left_plot_widget(self):
		self.left_plot_widget = DataPlotWidget(channel_num = GLOBAL_CONFIG.left_channel_num,
											  channel_names = GLOBAL_CONFIG.left_channel_name,
											  sample_rate = GLOBAL_CONFIG.sample_rate,
											  time_window = GLOBAL_CONFIG.plot_twindow,
											  channel_scale = GLOBAL_CONFIG.channel_scale)
	def __init_right_plot_widget(self):
		self.right_plot_widget = DataPlotWidget(channel_num = GLOBAL_CONFIG.right_channel_num,
												channel_names = GLOBAL_CONFIG.right_channel_name,
												sample_rate = GLOBAL_CONFIG.sample_rate,
												time_window = GLOBAL_CONFIG.plot_twindow,
												channel_scale = GLOBAL_CONFIG.channel_scale)
	def __init_plot_layout(self):
		# 先清空layout
		for i in reversed(range(self.plot_layout.count())):
			self.plot_layout.removeWidget(self.plot_layout.itemAt(i).widget())
		
		if self.right_plot_widget:
			self.plot_layout.addWidget(self.left_plot_widget,4)
			self.plot_layout.addWidget(self.right_plot_widget,4)
			
	def __reset_plot_widget(self):
		self.left_plot_widget.reset()
		if self.right_plot_widget:
			self.right_plot_widget.reset()

	def on_plot_left_data(self, data):
		self.left_plot_widget.plotItem.plot_data(data)
		
	def on_plot_right_data(self, data):
		self.right_plot_widget.plotItem.plot_data(data)
	def on_plot_twindow_changed(self):
		self.left_plot_widget.plotItem.on_plot_twindow_changed(GLOBAL_CONFIG.plot_twindow)
		self.right_plot_widget.plotItem.on_plot_twindow_changed(GLOBAL_CONFIG.plot_twindow)

	def on_channel_scale_changed(self):
		self.left_plot_widget.plotItem.on_channel_scale_changed(GLOBAL_CONFIG.channel_scale)
		self.right_plot_widget.plotItem.on_channel_scale_changed(GLOBAL_CONFIG.channel_scale)

	def __set_config(self):
		self.twindow_input.setValue(GLOBAL_CONFIG.plot_twindow)
		self.scale_input.setValue(GLOBAL_CONFIG.channel_scale)
		self.filter_check_box.setChecked(GLOBAL_CONFIG.filter)
		self.fmin_input.set_enable(GLOBAL_CONFIG.filter)
		self.fmax_input.set_enable(GLOBAL_CONFIG.filter)
		self.fmin_input.setValue(GLOBAL_CONFIG.fmin)
		self.fmax_input.setValue(GLOBAL_CONFIG.fmax)

	def __on_apply_config(self):
		GLOBAL_CONFIG.change_plot_twindow(self.twindow_input.value())
		GLOBAL_CONFIG.change_channel_scale(self.scale_input.value())
		GLOBAL_CONFIG.change_filter(self.filter_check_box.isChecked(), self.fmin_input.value(), self.fmax_input.value())
	def on_force_stop_recording(self):
		self.record_control_button.uncheck()
		self.record_stop_signal.emit()

	def __on_record_control(self):
		if not self.record_control_button.checked:
			connected = False
			if GLOBAL_CONFIG.is_left_device_connected:
				connected = True
			elif GLOBAL_CONFIG.is_right_device_connected:
				connected = True
			if connected:
				self.record_control_button.check()
				self.record_start_signal.emit()
			else:
				return MessageBox(message = '设备未连接，请先连接设备！', button_ok_text = '确认')
	def paintEvent(self, a0: QPaintEvent) -> None:
		opt = QStyleOption()
		opt.initFrom(self)
		painter = QPainter(self)
		self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, painter, self)
