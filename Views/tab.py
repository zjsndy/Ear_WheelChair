from typing import List

from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtWidgets import QWidget, QTabWidget

from Common import TAB_BAR_WIDTH, INIT_TAB_INDEX, TAB_NAME_LIST
from Components import TabButton
from .tabs import *


class TabBar(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.tab_num = 0
        self.tab_bar_width = TAB_BAR_WIDTH
        self.tab_btn: List[TabButton] = []
        self.__init_ui()

    def __init_ui(self):
        # 使子类的央样式生效 https://stackoverflow.com/questions/7276330/qt-stylesheet-for-custom-widget
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName('tab_bar')
        self.setStyleSheet('''
            #tab_bar{
                background-color:#e1e1e1;
            }
        ''')
        self.setFixedWidth(self.tab_bar_width)

    def add_tab_btn(self, icon, icon_slt, index, tip_text=''):
        btn = TabButton(icon, icon_slt, index, parent=self)
        btn.setToolTip(tip_text)
        # TODO: 后续将tab_button的绝对布局改为layout布局
        btn.move(0, self.tab_bar_width * self.tab_num)
        self.tab_num = self.tab_num + 1
        self.tab_btn.append(btn)


class Tab(QObject):

    switch_tab_signal = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.tab_bar = TabBar(parent=parent)
        self.tab_view = QTabWidget(parent=parent)
        self.tab_main = MainTab()
        self.config_tab = ConfigTab()
        self.visual_tab = VisualTab()
        self.task_tab = TaskTab()
        self.control_tab = ControlTab()
        self.tab_num = 0
        self.current_tab_index = 1
        self.__init_ui()

    def __init_ui(self):
        # 添加所有的tab页面
        self.__add_tab(self.config_tab, 'config', 'config.png', 'config-w.png')
        self.__add_tab(self.visual_tab, 'visual', 'wave.png', 'wave-w.png')
        self.__add_tab(self.task_tab, 'user', 'user.png', 'user-w.png')
        self.__add_tab(self.control_tab, 'task', 'train.png', 'train-w.png')
        
        # 使子类的样式生效 https://stackoverflow.com/questions/67503789/pyqt5-stylesheet-and-inheritance-from-qwidget
        # 但是不能靠 self.setAttribute(Qt.WA_StyledBackground, True)，还是需要重写paintEvent
        self.tab_view.setStyleSheet('''
            QTabBar:tab{
                width: 0;
                height: 0; 
                margin: 0; 
                padding: 0; 
                border: none;
            }
            QTabWidget{
                margin: 0; 
                padding: 0; 
                border: none;
                background-color: #ffffff;
                border-bottom-right-radius: 10;
            }
            QTabWidget::pane{
                background-color: #ffffff;
                border: none;
            }
        ''')

        self.tab_view.setCurrentIndex(INIT_TAB_INDEX)
        self.tab_bar.tab_btn[INIT_TAB_INDEX].click()

    def __add_tab(self, tab, tab_name, tab_icon, tab_icon_slt):
        # add tab for QTabWidget
        self.tab_view.addTab(tab, tab_name)
        tab_index = self.tab_num
        # add tab button
        self.tab_bar.add_tab_btn(tab_icon, tab_icon_slt, index=tab_index, tip_text=TAB_NAME_LIST[tab_index])
        self.tab_bar.tab_btn[tab_index].selected_signal.connect(self.__on_switch_tab)
        self.tab_num = self.tab_num + 1

    def __on_switch_tab(self, index):
        if index == self.current_tab_index:
            return
        self.tab_view.setCurrentIndex(index)
        if self.current_tab_index >= 0:
            self.tab_bar.tab_btn[self.current_tab_index].unselect()
        self.tab_bar.tab_btn[index].select()
        self.current_tab_index = index
        self.switch_tab_signal.emit(index)
