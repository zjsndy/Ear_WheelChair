import asyncio
import sys

import matplotlib
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFontDatabase, QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QDesktopWidget, QApplication, QSplashScreen

from Config import GLOBAL_CONFIG
from data_manager import DataManager
#from Processor import PROCESSOR
from Common import get_abs_path
from Views import TopBar, Tab

matplotlib.use("Qt5Agg")

class EarWheelChair(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.widget = QWidget(self)
        
        self.top_bar_widget = TopBar(parent = self)
        self.tab_widget = Tab(parent = self)
        
        self.width = 1440
        self.height = 900
        
        self.data_manager = DataManager()
        
        self.__init_ui()
        self.__init_slot()
    
    def __init_ui(self):
        self.setMinimumSize(1440, 900)
        self.resize(self.width, self.height)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setHorizontalSpacing(0)
        self.layout.setVerticalSpacing(3)
        
        # 为了能使TopBar的阴影生效，后添加TopBar
        self.layout.addWidget(self.tab_widget.tab_bar, 1, 0, 1, 1)
        self.layout.addWidget(self.tab_widget.tab_view, 1, 1, 1, 1)
        self.layout.addWidget(self.top_bar_widget, 0, 0, 1, 2)
        
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.setWindowTitle('智能轮椅系统')
    
    def __init_slot(self):
        self.tab_widget.switch_tab_signal.connect(self.top_bar_widget.on_switch_tab)
        
        GLOBAL_CONFIG.filter_changed_signal.connect(self.data_manager.on_filter_changed)
        
        self.tab_widget.config_tab.connect_left_device_signal.connect(self.data_manager.connect_left_device)
        self.tab_widget.config_tab.disconnect_left_device_signal.connect(self.data_manager.disconnect_left_device)

        self.data_manager.send_left_plot_data_signal.connect(self.tab_widget.visual_tab.on_plot_left_data)
        self.data_manager.send_right_plot_data_signal.connect(self.tab_widget.visual_tab.on_plot_right_data)
        
        self.data_manager.left_connected_signal.connect(self.tab_widget.config_tab.change_left_device_connect)
        self.data_manager.right_connected_signal.connect(self.tab_widget.config_tab.change_right_device_connect)
        
        self.data_manager.force_stop_recording_signal.connect(self.tab_widget.visual_tab.on_force_stop_recording)
        
        self.tab_widget.visual_tab.record_start_signal.connect(self.data_manager.start_record_device)
      
        self.tab_widget.visual_tab.record_stop_signal.connect(self.data_manager.stop_record_device)

        GLOBAL_CONFIG.config_input_changed_signal.connect(self.tab_widget.config_tab.set_config)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 取消ComboBox下拉动画
    app.setEffectEnabled(Qt.UI_AnimateCombo, False)
    app.setWindowIcon(QIcon(get_abs_path('static/img/sys-icon.png')))
    # 添加自定义字体文件
    QFontDatabase.addApplicationFont(get_abs_path('static/fonts/Baloo2-Regular.ttf'))
    QFontDatabase.addApplicationFont(get_abs_path('static/fonts/Goldman-Regular.ttf'))
    QFontDatabase.addApplicationFont(get_abs_path('static/fonts/ChillDuanSans_Regular.otf'))
    main_window = EarWheelChair()
    main_window.show()
    sys.exit(app.exec_())
