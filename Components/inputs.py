import logging
from typing import List

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (
    QLineEdit, QSpinBox, QComboBox,
    QListView, QCheckBox, QDoubleSpinBox,
    QListWidget, QListWidgetItem, QButtonGroup)

from Common import get_abs_path


class InputLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.__init_ui()

    def __init_ui(self):
        self.setStyleSheet('''
            QLineEdit{
                border: 2 solid #e0e0e0;
                border-radius: 6;
                padding: 4 6;
                font-weight: bold;
                font-size: 18px;
                color: #888888;
                font-family: Baloo 2;
                selection-background-color: #888888;
                selection-color: #ffffff;
            }
            QLineEdit:hover, QLineEdit:focus{
                border: 2 solid #aecbfa;
            }
        ''')


class InputSpinBox(QSpinBox):
    def __init__(self, min_value, max_value, step_value=1, enable=True):
        super().__init__()
        self.setMinimum(min_value)
        self.setMaximum(max_value)
        self.setEnabled(enable)
        self.setProperty("enable", enable)
        self.setSingleStep(step_value)
        self.__init_ui()

    def __init_ui(self):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setStyleSheet(f'''
            QSpinBox{{
                border: 2 solid #e0e0e0;
                border-radius: 6;
                padding: 4 6;
                font-weight: bold;
                font-size: 18px;
                font-family: Baloo 2;
                selection-background-color: #888888;
                selection-color: #ffffff;
                qproperty-alignment: AlignCenter;
            }}
            QSpinBox[enable="true"]{{
                background-color: #ffffff;
                color: #888888;
            }}
            QSpinBox[enable="false"]{{
                background-color: #f7f7f7;
                color: #dddddd;
            }}
            QSpinBox::up-button{{
                width: 30px;
                height: 30px;
                border: none;
                padding: 5;
                subcontrol-position: right;
            }}
            QSpinBox::down-button{{
                width: 30px;
                height: 30px;
                border: none;
                padding: 5;
                subcontrol-position: left;
            }}
            QSpinBox::up-arrow, QSpinBox::down-arrow{{
                width: 25px;
                height: 25px;
            }}
            QSpinBox[enable="true"]::down-arrow{{
                image: url({get_abs_path('static/img/sub.svg')});
            }}
            QSpinBox[enable="false"]::down-arrow{{
                image: url({get_abs_path('static/img/sub-unable.svg')});
            }}
            QSpinBox[enable="true"]::up-arrow{{
                image: url({get_abs_path('static/img/add.svg')});
            }}
            QSpinBox[enable="false"]::up-arrow{{
                image: url({get_abs_path('static/img/add-unable.svg')});
            }}
        ''')

    def on_enable_changed(self, state):
        if state == 0:
            self.set_enable(False)
        else:
            self.set_enable(True)

    def set_enable(self, enable):
        self.setEnabled(enable)
        self.setProperty("enable", enable)
        self.style().polish(self)


class InputDoubleSpinBox(QDoubleSpinBox):
    def __init__(self, min_value, max_value, step_value=0.1, enable=True):
        super().__init__()
        self.setMinimum(min_value)
        self.setMaximum(max_value)
        self.setEnabled(enable)
        self.setProperty("enable", enable)
        self.setSingleStep(step_value)
        self.__init_ui()

    def __init_ui(self):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setDecimals(1)
        self.setStyleSheet(f'''
            QDoubleSpinBox{{
                border: 2 solid #e0e0e0;
                border-radius: 6;
                padding: 4 6;
                font-weight: bold;
                font-size: 18px;
                font-family: Baloo 2;
                selection-background-color: #888888;
                selection-color: #ffffff;
                qproperty-alignment: AlignCenter;
            }}
            QDoubleSpinBox[enable="true"]{{
                background-color: #ffffff;
                color: #888888;
            }}
            QDoubleSpinBox[enable="false"]{{
                background-color: #f7f7f7;
                color: #dddddd;
            }}
            QDoubleSpinBox::up-button{{
                width: 30px;
                height: 30px;
                border: none;
                padding: 5;
                subcontrol-position: right;
            }}
            QDoubleSpinBox::down-button{{
                width: 30px;
                height: 30px;
                border: none;
                padding: 5;
                subcontrol-position: left;
            }}
            QDoubleSpinBox::up-arrow, QDoubleSpinBox::down-arrow{{
                width: 25px;
                height: 25px;
            }}
            QDoubleSpinBox[enable="true"]::down-arrow{{
                image: url({get_abs_path('static/img/sub.svg')});
            }}
            QDoubleSpinBox[enable="false"]::down-arrow{{
                image: url({get_abs_path('static/img/sub-unable.svg')});
            }}
            QDoubleSpinBox[enable="true"]::up-arrow{{
                image: url({get_abs_path('static/img/add.svg')});
            }}
            QDoubleSpinBox[enable="false"]::up-arrow{{
                image: url({get_abs_path('static/img/add-unable.svg')});
            }}
        ''')

    def on_enable_changed(self, state):
        if state == 0:
            self.set_enable(False)
        else:
            self.set_enable(True)

    def set_enable(self, enable):
        self.setEnabled(enable)
        self.setProperty("enable", enable)
        self.style().polish(self)


class InputCheckBox(QCheckBox):
    def __init__(self, text):
        super().__init__(text=text)
        self.__init_ui()

    def __init_ui(self):
        self.setStyleSheet(f'''
            QCheckBox{{
                border: none;
                font-weight: bold;
                font-size: 18px;
                color: #606060;
                font-family: Baloo 2;
                spacing: 15;
            }}
            QCheckBox::indicator:unchecked{{
                border: none;
                image: url({get_abs_path('static/img/uncheck.svg')});
                width: 25;
                height: 25;
            }}
            QCheckBox::indicator:checked{{
                border: none;
                image: url({get_abs_path('static/img/check.svg')});
                width: 25;
                height: 25;
            }}
        ''')
        self.setCursor(QCursor(Qt.PointingHandCursor))


class InputComboBox(QComboBox):
    def __init__(self, items=None):
        super().__init__()
        if items is None:
            items = []
        self.items: list[str] = items
        self.__init_ui()

    def __init_ui(self):
        self.replace_items(self.items)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setView(QListView())
        self.setStyleSheet(f'''
            QComboBox{{
                border: 2 solid #e0e0e0;
                border-radius: 6;
                padding: 4 10;
                font-size: 18px;
                font-weight: bold;
                color: #888888;
                font-family: Baloo 2;
                selection-background-color: #888888;
                selection-color: #ffffff;
            }}
            QComboBox::drop-down{{
                border: none;
                width: 35px;
            }}
            QComboBox::down-arrow{{
                image: url({get_abs_path('static/img/arrow.png')});
            }}
            QListView{{
                border-radius: 6;
                font-size: 16px;
                font-weight: bold;
                color: #888888;
                font-family: Baloo 2;
                border: 2 solid #e1e1e1;
                background-color: #ffffff;
                outline: none;
                padding: 6;
            }}
            QListView:item{{
                border-radius: 4;
                padding: 4;
            }}
            QListView:item:selected{{
                color: #888888;
                background-color: #e7f0fe;
            }}
        ''')
        # 给ComboBox加圆角 https://stackoverflow.com/questions/27962162/rounded-qcombobox-without-square-box-behind
        self.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.view().window().setAttribute(Qt.WA_TranslucentBackground)

    def set_current_item(self, item):
        index = self.items.index(item)
        self.setCurrentIndex(index)

    def set_non_sel(self):
        self.setCurrentIndex(-1)

    def replace_items(self, items: list[str]):
        self.clear()
        self.items = []
        if items is None or len(items) == 0:
            self.set_non_sel()
        else:
            self.items = items
            self.addItems(items)


class InputMulSelList(QListWidget):
    def __init__(self, items=None):
        super().__init__()
        if items is None:
            items = []

        self.items: list[str] = items
        self.length = len(items)

        self.checked_list: list[int] = []
        # 非单选按钮组统一管理信号
        self.btn_group = QButtonGroup()
        self.btn_group.setExclusive(False)

        self.__init_ui()

    def get_sel_labels(self):
        sel_lab: list[str] = []
        self.checked_list = sorted(self.checked_list)
        for i in self.checked_list:
            sel_lab.append(self.items[i])
        return sel_lab

    def get_sel_ids(self):
        self.checked_list = sorted(self.checked_list)
        return self.checked_list

    def on_source_change(self, labels: list[str]):
        self.__new_check_items(labels)

    def __on_select_change(self, idx: int, check: bool):
        if check:
            self.checked_list.append(idx)
            self.checked_list.sort()
        else:
            self.checked_list.remove(idx)

    def on_all_sel_clicked(self):
        self.__on_sel_btn_clicked(True)

    def on_non_sel_clicked(self):
        self.__on_sel_btn_clicked(False)

    def __on_sel_btn_clicked(self, check: bool):
        self.btn_group.buttonToggled[int, bool].disconnect(self.__on_select_change)
        self.checked_list = []

        for btn in self.btn_group.buttons():
            btn.setChecked(check)
            if check:
                self.checked_list.append(self.btn_group.id(btn))

        self.btn_group.buttonToggled[int, bool].connect(self.__on_select_change)

    def __apply_style_sheet(self):
        self.setStyleSheet(f'''
            QListWidget{{
                border-radius: 6;
                font-size: 16px;
                font-weight: bold;
                color: #888888;
                font-family: Baloo 2;
                border: 2 solid #e1e1e1;
                background-color: #ffffff;
                outline: none;
                padding: 6;
            }}
            QListWidget:item{{
                border-radius: 4;
                padding: 4;
            }}
            QListWidget:item:selected{{
                color: #888888;
                background-color: #e7f0fe;
            }}
            QListWidget:item:hover{{
                color: #ffffff;
                background-color: #a7cbf6;
            }}
        ''')

    def __add_check_item(self, text: str, idx: int):
        # construct list item using customized checkbox
        item = QListWidgetItem(parent=self)
        box = InputCheckBox(text)
        # add to unified group to collect signal
        self.btn_group.addButton(box, idx)
        # add single styled item to list
        self.addItem(item)
        self.setItemWidget(item, box)

    def __new_check_items(self, text_list: list[str], idx_list: list[int] = None):
        if idx_list is None:
            idx_list = np.arange(0, len(text_list)).tolist()

        if len(text_list) != len(idx_list):
            logging.log(logging.WARNING,
                        "Mismatched length of channel labels and indexes")
            return

        self.__remove_all_check()

        self.length = len(text_list)
        self.items = text_list
        self.checked_list = []

        for i in range(self.length):
            self.__add_check_item(text_list[i], idx_list[i])

    def __remove_all_check(self):
        btn_list = self.btn_group.buttons()
        for btn in btn_list:
            self.btn_group.removeButton(btn)
        self.clear()
        self.checked_list = []

    def __init_ui(self):
        self.__new_check_items(self.items)
        self.__apply_style_sheet()

        self.btn_group.buttonToggled[int, bool].connect(self.__on_select_change)
