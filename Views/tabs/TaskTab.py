from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPaintEvent, QPainter
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGridLayout, QVBoxLayout, QStyleOption, QStyle, QScrollArea

from Common import *
from Components import *

class TaskTab(QWidget):
	
	start_exp_signal = pyqtSignal()
	def __init__(self, parent = None):
		super().__init__(parent)
		self.layout = QHBoxLayout()
		self.input_layout = QGridLayout()
		self.config_layout = QVBoxLayout()
		self.paradigm_layout = QGridLayout()
		
		self.config_widget = QWidget()
		self.paradigm_widgets = [[] for _ in range(len(PARADIGMS))]
		self.exp_window = ExpWindow()
		
		self.paradigm_combobox = InputComboBox(items = [DESCRIPTION[paradigm['paradigm']] for paradigm in PARADIGMS])
		self.trial_input = InputSpinBox(min_value = 2, max_value = 20, step_value = 2)
		self.rest_time_input = InputSpinBox(min_value = 2, max_value = 10, step_value = 1)
		self.perform_time_input = InputSpinBox(min_value = 2, max_value = 10, step_value = 1)
		self.exp_button = ClickButton(text = '开始实验', role = 'OK')
		
		self.__init_ui()
		# self.__init_slot()
		# self.__set_config()

	def __init_ui(self):
		self.input_layout = QGridLayout()
		self.input_layout.addWidget(TextLabel(text = '实验范式选择'), 0, 0, 1, 4)
		self.input_layout.addWidget(self.paradigm_combobox, 1, 0, 1, 4)
		self.input_layout.addWidget(TextLabel(text = 'Trial数(次)'), 2, 0, 1, 4)
		self.input_layout.addWidget(self.trial_input, 3, 0, 1, 4)
		self.input_layout.addWidget(TextLabel(text = '休息时间(s)'), 4, 0, 1, 4)
		self.input_layout.addWidget(self.rest_time_input, 5, 0, 1, 4)
		self.input_layout.addWidget(TextLabel(text = '执行时间(s)'), 6, 0, 1, 4)
		self.input_layout.addWidget(self.perform_time_input, 7, 0, 1, 4)
		
		self.input_layout.setHorizontalSpacing(10)
		self.input_layout.setVerticalSpacing(15)
		
		self.config_layout.addLayout(self.input_layout)
		self.config_layout.addStretch(1)
		self.config_layout.addWidget(self.exp_button)
		self.config_layout.setContentsMargins(30, 30, 30, 30)
		self.config_layout.setSpacing(15)
		self.config_widget.setFixedWidth(320)
		self.config_widget.setLayout(self.config_layout)
		self.config_widget.setObjectName('config_widget')
		self.config_widget.setStyleSheet('''
		            #config_widget{
		                border-right: 2 solid #eeeeee;
		            }
		        ''')
		
		rows = 0
		cols = 0
		for paradigm_index, paradigm in enumerate(PARADIGMS):
			paradigm_name = paradigm['paradigm']
			self.paradigm_layout.addWidget(
				TextLabel(DESCRIPTION[paradigm_name], font_size = 20, parent = self), rows, cols, 1, 4)
			rows += 1
			self.paradigm_widgets[paradigm_index] = []
			for movement in paradigm['movements']:
				movement_widget = ParadigmMovementWidget(parent = self, paradigm_index = paradigm_index,
														 movement_type = movement, description = DESCRIPTION[movement])
				movement_widget.paradigm_select_signal.connect(self.__on_paradigm_widget_changed)
				self.paradigm_widgets[paradigm_index].append(movement_widget)
				self.paradigm_layout.addWidget(movement_widget, rows, cols, 1, 1)
				cols += 1
				if cols == 4:
					rows += 1
					cols = 0
			rows += 1
			cols = 0
		self.paradigm_layout.setRowStretch(rows + 1, 1)
		self.paradigm_layout.setHorizontalSpacing(10)
		self.paradigm_layout.setVerticalSpacing(15)
		self.paradigm_layout.setContentsMargins(25, 25, 25, 25)
		paradigm_widget = QWidget()
		paradigm_widget.setObjectName('paradigm_widget')
		paradigm_widget.setStyleSheet("""
		    #paradigm_widget {
		        background-color: #ffffff;
		    }
		""")
		paradigm_widget.setLayout(self.paradigm_layout)
		
		paradigm_scroll_area = QScrollArea()
		paradigm_scroll_area.setWidgetResizable(True)
		paradigm_scroll_area.setStyleSheet("""
		    QScrollArea {
		        border: none;
		        background-color: #ffffff;
		    }
		    QScrollBar:vertical {
		        border: none;
		        background-color: #ffffff;
		        width: 8;
		    }
		    QScrollBar::handle:vertical {
		        background: #c0c0c0;
		        min-height: 10;
		        border-radius: 4;
		    }
		    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
		        border: none;
		        background: none;
		    }
		""")
		paradigm_scroll_area.setWidget(paradigm_widget)
		
		self.layout.addWidget(self.config_widget)
		self.layout.addWidget(paradigm_scroll_area)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.setSpacing(0)
		self.setLayout(self.layout)
	
	def __change_selected_paradigm(self, paradigm_index):
		for index, p_widgets in enumerate(self.paradigm_widgets):
			for p_widget in p_widgets:
				if index == paradigm_index:
					p_widget.select()
				else:
					p_widget.unselect()
	
	def __on_paradigm_widget_changed(self, paradigm_index):
		if self.paradigm_combobox.currentIndex() != paradigm_index:
			self.__change_selected_paradigm(paradigm_index)
			self.paradigm_combobox.setCurrentIndex(paradigm_index)

class ExpWindow(QWidget):
	manual_stop_exp_signal = pyqtSignal()
	
	# 由于窗口显示的内容和每次训练时候的范式配置有关，所以每次训练都要先移除layout中的控件，再重新添加
	# 参考: https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt
	@staticmethod
	def clear_layout(layout):
		while layout.count():
			child = layout.takeAt(0)
			if child.widget():
				child.widget().deleteLater()
			elif child.layout():
				ExpWindow.clear_layout(child.layout())
	
	def __init__(self, parent = None):
		super().__init__(parent = parent)
		self.layout = QHBoxLayout()
		self.classify_layout = QVBoxLayout()
		self.cue_layout = QVBoxLayout()
		
		self.classify_widget = None
		self.classify_item_widgets: List[ClassifyItemWidget] = []
		self.classify_instruct_widget = None
		
		self.cue_image_widget = None
		self.cue_text_widget = None
		
		self.__init_ui()
	
	def __init_ui(self):
		self.resize(960, 640)
		# self.setMaximumSize(1080, 720)
		self.setObjectName('exp_widget')
		self.setStyleSheet('''
	           #exp_widget{
	               background-color:#ffffff;
	           }
	       ''')
	
	def init_layout(self):
		self.clear_layout(self.classify_layout)
		self.clear_layout(self.layout)
		
		self.classify_layout.addStretch(1)
		self.classify_layout.addWidget(
			TextLabel(text = f"{DESCRIPTION[PARADIGMS[GLOBAL_CONFIG.paradigm]['paradigm']]}", font_size = 24),
			alignment = Qt.AlignCenter)
		self.classify_item_widgets = []
		for movement in PARADIGMS[GLOBAL_CONFIG.paradigm]['movements']:
			self.classify_item_widgets.append(ClassifyItemWidget(movement = DESCRIPTION[movement]))
		for p in self.classify_item_widgets:
			self.classify_layout.addWidget(p)
		self.classify_instruct_widget = ClassifyInstructWidget(text = '实验准备开始')
		self.classify_layout.addWidget(self.classify_instruct_widget)
		self.classify_layout.addStretch(1)
		self.classify_layout.setSpacing(10)
		self.classify_layout.setContentsMargins(15, 10, 15, 10)
		self.classify_widget = QWidget()
		self.classify_widget.setFixedWidth(420)
		self.classify_widget.setLayout(self.classify_layout)
		
		self.cue_image_widget = QLabel()
		self.cue_image_widget.setScaledContents(True)
		self.cue_image_widget.setFixedSize(500, 500)
		self.cue_text_widget = CueInstructWidget()
		self.cue_layout.addStretch(1)
		self.cue_layout.addWidget(self.cue_image_widget, alignment = Qt.AlignCenter)
		self.cue_layout.addWidget(self.cue_text_widget)
		self.cue_layout.addStretch(1)
		self.cue_layout.setContentsMargins(15, 10, 15, 10)
		
		self.layout.addStretch(1)
		self.layout.addLayout(self.cue_layout)
		self.layout.addWidget(self.classify_widget)
		self.layout.addStretch(1)
		
		self.setLayout(self.layout)
	
	def display_paradigm_cue(self, stage, movement_index):
		if stage == 0:
			self.cue_image_widget.setStyleSheet(f'''
	               QLabel{{
	                   image: url({get_abs_path(f'static/img/rest.svg')});
	               }}
	           ''')
			# cue_gif = QMovie(get_abs_path(f'static/img/rest.gif'))
			# self.cue_image_widget.setMovie(cue_gif)
			# cue_gif.start()
			self.cue_text_widget.set_stage('rest', '休息')
		else:
			movement = DESCRIPTION[PARADIGMS[GLOBAL_CONFIG.paradigm]['movements'][movement_index]]
			movement_image = f"{PARADIGMS[GLOBAL_CONFIG.paradigm]['movements'][movement_index]}.svg"
			self.cue_image_widget.setStyleSheet(f'''
	               QLabel{{
	                   image: url({get_abs_path(f'static/img/{movement_image}')});
	               }}
	           ''')
			# cue_gif = QMovie(get_abs_path(f'static/img/left_hand.gif'))
			# self.cue_image_widget.setMovie(cue_gif)
			# cue_gif.start()
			
			if stage == 1:
				# 将上一个动作的分类概率清空
				for p_widget in self.classify_item_widgets:
					p_widget.clear_probability()
				self.cue_text_widget.set_stage('cue', f'下一个动作：{movement}')
				self.classify_instruct_widget.set_text('准备下一个动作')
			elif stage == 2:
				self.cue_text_widget.set_stage('perform', f'执行动作：{movement}')
	
	def display_twindow_start(self, twindow_index, twindow_num):
		self.classify_instruct_widget.set_text(f'动作分类中: {twindow_index} / {twindow_num}')
	
	def display_twindow_result(self, probability):
		assert len(probability) == len(self.classify_item_widgets)
		for i, p_widget in enumerate(self.classify_item_widgets):
			p_widget.update_probability(probability[i])
	
	def display_classify_result(self, classify_movement, perform_movement):
		if classify_movement == perform_movement:
			self.classify_instruct_widget.set_text('分类正确')
		else:
			self.classify_instruct_widget.set_text('分类错误')
	
	def closeEvent(self, event):
		if GLOBAL_CONFIG.is_exp:
			self.manual_stop_exp_signal.emit()
		print('cue windows closed.')
		event.accept()
		
		
		
		
	
	
	
	def paintEvent(self, a0: QPaintEvent) -> None:
		opt = QStyleOption()
		opt.initFrom(self)
		painter = QPainter(self)
		self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, painter, self)
