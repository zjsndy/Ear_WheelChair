from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QPushButton, QMenu, QProxyStyle, QStyle

from Common import *


class TabButton(QPushButton):
    selected_signal = pyqtSignal(int)

    def __init__(self, icon, icon_slt, index, parent=None):
        super().__init__(parent=parent)
        self.selected = False
        self.setProperty("selected", self.selected)
        self.index = index
        self.size = TAB_BUTTON_SIZE
        self.style_sheet = f'''
            QPushButton{{
                margin: 0;
                padding: 0;
                border: none;
                background-repeat:no-repeat;
                background-position:center;
                border-radius: 3;
            }}
            QPushButton[selected="false"]{{
                background-color:#e1e1e1;
                background-image: url({get_abs_path('static/img/' + icon)});
            }}
            QPushButton[selected="true"]{{
                background-color: #1967d2;
                background-image: url({get_abs_path('static/img/' + icon_slt)});
            }}
        '''
        self.__init_ui()

    def __init_ui(self):
        self.resize(self.size, self.size)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setStyleSheet(self.style_sheet)
        self.clicked.connect(lambda: self.selected_signal.emit(self.index))

    def select(self):
        self.selected = True
        self.setProperty("selected", self.selected)
        self.style().polish(self)

    def unselect(self):
        self.selected = False
        self.setProperty("selected", self.selected)
        self.style().polish(self)


class ClickButton(QPushButton):
    def __init__(self, text='', role='OK', font_size=18, parent=None):
        super().__init__(parent=parent, text=text)
        self.setProperty('role', role)
        self.style_sheet = f'''
            QPushButton{{
                border: none;
                border-radius: 4;
                padding: 5;
                font-size: {font_size}px;
                font-weight: bold;
                font-family: Baloo 2, ChillDuanSans;
            }}
            QPushButton[role="OK"]{{
                color: #ffffff;
                background-color: #4285f4;
            }}
            QPushButton:hover[role="OK"]{{
                background-color: #1967d2;
            }}
            QPushButton[role="CANCEL"]{{
                color: #3d3d3d;
                background-color: #e1e1e1;
            }}
            QPushButton:hover[role="CANCEL"]{{
                background-color: #d6d6d6;
            }}
            QPushButton[role="NORMAL"]{{
                color: #ffffff;
                background-color: #8a8a8a;
            }}
            QPushButton:hover[role="NORMAL"]{{
                background-color: #707070;
            }}
        '''
        self.__init_ui()

    def __init_ui(self):
        self.setStyleSheet(self.style_sheet)
        self.setCursor(QCursor(Qt.PointingHandCursor))


class CheckableButton(QPushButton):
    def __init__(self, check_text='', uncheck_text='', parent=None):
        super().__init__(parent=parent, text=uncheck_text)
        self.style_sheet = '''
            QPushButton{
                padding: 0;
                border: none;
                border-radius: 4;
                padding: 5;
                font-size: 18px;
                font-weight: bold;
                font-family: Baloo 2;
                background-color:  #4285f4;
            }
            QPushButton[checked="false"]{
                color: #ffffff;
                background-color:  #4285f4;
            }
            QPushButton:hover[checked="false"]{
                background-color:#1967d2;
            }
            QPushButton[checked="true"]{
                color: #3d3d3d;
                background-color: #e1e1e1;
            }
            QPushButton:hover[checked="true"]{
                background-color:#d6d6d6;
            }
        '''
        self.check_text = check_text
        self.uncheck_text = uncheck_text
        self.__init_ui()

    def __init_ui(self):
        self.setCheckable(True)
        self.setChecked(False)
        self.setProperty("checked", False)
        self.setStyleSheet(self.style_sheet)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.clicked.connect(self.__on_check)

    def __on_check(self, check):
        if check:
            self.setProperty("checked", True)
            self.setText('Stop')
            self.style().polish(self)
        else:
            self.setProperty("checked", False)
            self.setText('Start')
            self.style().polish(self)


class ElectrodeButton(QPushButton):
    def __init__(self, text='', selected=False, font_size=16, parent=None):
        super().__init__(text=text, parent=parent)
        self.electrode = text
        self.size = ELECTRODE_BUTTON_SIZE
        self.style_sheet = f'''
            QPushButton{{
                border-radius: 24;
                font-size: {font_size}px;
                font-weight: bold;
                font-family: Baloo 2, ChillDuanSans;
            }}
            QPushButton[selected="false"]{{
                background-color: #e8f0fe;
                color: #174ea6;
            }}
            QPushButton:hover[selected="false"]{{
                background-color: #d2e3fc;
            }}
            QPushButton[selected="true"]{{
                background-color: #4285f4;
                color: #ffffff;
            }}
        '''
        self.selected = selected
        self.setProperty("selected", selected)
        self.__init_ui()

    def __init_ui(self):
        self.resize(self.size, self.size)
        self.setStyleSheet(self.style_sheet)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.clicked.connect(self.__on_click)

    def __on_click(self):
        self.unselect() if self.selected else self.select()

    def select(self):
        self.selected = True
        self.setProperty("selected", self.selected)
        self.style().polish(self)

    def unselect(self):
        self.selected = False
        self.setProperty("selected", self.selected)
        self.style().polish(self)

    def unable(self):
        self.unselect()
        self.setEnabled(False)
        self.setCursor(QCursor(Qt.ForbiddenCursor))

    def enable(self):
        self.select()
        self.setEnabled(True)
        self.setCursor(QCursor(Qt.PointingHandCursor))


class IconButton(QPushButton):

    def __init__(self, icon, parent=None):
        super().__init__(parent=parent)
        self.style_sheet = f'''
            QPushButton{{
                border: none;
                border-radius: 5;
                background-repeat:no-repeat;
                background-position:center;
                background-image: url({get_abs_path('static/img/' + icon)});
            }}
            QPushButton:hover{{
                background-color: #eeeeee;
            }}
            QPushButton::menu-indicator{{
                image: none;
            }}
        '''
        self.__init_ui()

    def __init_ui(self):
        self.setFixedSize(45, 45)
        self.setStyleSheet(self.style_sheet)
        self.setCursor(QCursor(Qt.PointingHandCursor))


# 改变QMenu菜单图标大小的方法 https://stackoverflow.com/questions/39396707/how-to-make-icon-in-qmenu-larger-pyqt
class CustomMenuStyle(QProxyStyle):

    def __init__(self, icon_size=25):
        super().__init__()
        self.icon_size = icon_size

    def pixelMetric(self, metric, option, widget):
        if metric == QStyle.PM_SmallIconSize:
            return self.icon_size

        return super().pixelMetric(metric, option, widget)


class DropMenu(QMenu):
    def __init__(self):
        super().__init__()
        self.style_sheet = '''
            QMenu {
                border-radius: 6;
                border: 1px solid #e1e1e1;
                background-color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                font-family: Baloo 2;
                color: #606060;
                margin: 0;
                padding: 7;
            }
            QMenu::item{
                border-radius: 3;
                padding: 4 8;
            }
            QMenu::item:selected{
                background-color: #efefef;
            }
        '''
        self.__init_ui()

    # 给QMenu背景添加圆角 https://stackoverflow.com/questions/65574567/rounded-corners-for-qmenu-in-pyqt
    def __init_ui(self):
        self.setStyle(CustomMenuStyle())
        self.setStyleSheet(self.style_sheet)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

class CheckButton(QPushButton):
    def __init__(self, check_text='', uncheck_text='', parent=None):
        super().__init__(parent=parent, text=uncheck_text)
        self.style_sheet = '''
            QPushButton{
                padding: 0;
                border: none;
                border-radius: 4;
                padding: 5;
                font-size: 18px;
                font-weight: bold;
                font-family: Baloo 2, ChillDuanSans;
                background-color:  #4285f4;
            }
            QPushButton[check="false"]{
                color: #ffffff;
                background-color:  #4285f4;
            }
            QPushButton:hover[check="false"]{
                background-color:#1967d2;
            }
            QPushButton[check="true"]{
                color: #3d3d3d;
                background-color: #e1e1e1;
            }
            QPushButton:hover[check="true"]{
                background-color:#d6d6d6;
            }
        '''
        self.check_text = check_text
        self.uncheck_text = uncheck_text
        self.checked = False
        self.__init_ui()

    def __init_ui(self):
        self.setProperty("check", False)
        self.setStyleSheet(self.style_sheet)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def check(self):
        self.checked = True
        self.setProperty("check", True)
        self.setText(self.check_text)
        self.style().polish(self)

    def uncheck(self):
        self.checked = False
        self.setProperty("check", False)
        self.setText(self.uncheck_text)
        self.style().polish(self)
