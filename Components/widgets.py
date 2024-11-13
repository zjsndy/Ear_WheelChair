from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QDialog, QWidget

from Common import get_abs_path
from Components import ClickButton, TextLabel


class ParadigmMovementWidget(QWidget):
    paradigm_select_signal = pyqtSignal(int)

    def __init__(self, paradigm_index, movement_type, description, parent=None):
        super().__init__(parent=parent)
        self.info_layout = QHBoxLayout()
        self.image_widget = QWidget()
        self.paradigm_index = paradigm_index
        self.movement_type = movement_type
        self.description = description
        self.selected = False
        self.setProperty("selected", self.selected)

        self.__init_ui()

    def __init_ui(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.image_widget.setStyleSheet(f'''
            QWidget{{
                image: url({get_abs_path(f'static/img/{self.movement_type}.svg')});
            }}
        ''')
        self.image_widget.setFixedSize(60, 60)
        self.info_layout.addWidget(self.image_widget)
        self.info_layout.addWidget(TextLabel(self.description))

        self.info_layout.setSpacing(10)
        self.info_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.info_layout)

        self.setObjectName('paradigm_widget')
        self.setStyleSheet('''
            #paradigm_widget{
                border-radius: 6;
            }
            #paradigm_widget[selected="false"]{
                background-color: #e9f0fd;
            }
            #paradigm_widget[selected="true"]{
                background-color: #d5e2fa;
                border: 3px solid #93b3f2;
            }
        ''')
    def mouseReleaseEvent(self, event):
        self.paradigm_select_signal.emit(self.paradigm_index)

    def select(self):
        self.selected = True
        self.setProperty("selected", self.selected)
        self.style().polish(self)

    def unselect(self):
        self.selected = False
        self.setProperty("selected", self.selected)
        self.style().polish(self)








class MessageBox(QDialog):
    def __init__(self, message, message_type="提示", button_ok_text=None, button_cancel_text=None):
        super().__init__()
        self.message_type = message_type
        self.message = message
        self.button_ok_text = button_ok_text
        self.button_cancel_text = button_cancel_text
        self.feedback = 0

        self.button_ok = ClickButton(text=self.button_ok_text, role='OK', font_size=16)
        self.button_cancel = ClickButton(text=self.button_cancel_text, role='CANCEL', font_size=16)

        self.button_layout = QHBoxLayout()
        self.layout = QVBoxLayout()
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle(self.message_type)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet('''
        QDialog{
            background-color: #ffffff;
        }
        ''')
        self.setFixedSize(400, 180)

        self.button_ok.setMinimumWidth(80)
        self.button_cancel.setMinimumWidth(80)
        # 根据按钮的数量进行排版
        if self.button_ok_text:
            self.button_layout.addStretch(1)
            self.button_layout.addWidget(self.button_ok)
            self.button_layout.addStretch(1)
        if self.button_cancel_text:
            if not self.button_ok_text:
                self.button_layout.addStretch(1)
            self.button_layout.addWidget(self.button_cancel)
            self.button_layout.addStretch(1)
        self.button_layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(TextLabel(text=self.message, font_size=18))
        self.layout.addStretch(1)
        self.layout.addLayout(self.button_layout)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.setLayout(self.layout)

        self.button_ok.clicked.connect(self.click_ok_feedback)
        self.button_cancel.clicked.connect(self.click_cancel_feedback)

    def click_ok_feedback(self):
        self.feedback = 1
        self.close()

    def click_cancel_feedback(self):
        self.feedback = 2
        self.close()
        
class CheckWidget(QWidget):
    def __init__(self, text="", state="invalid", parent=None):
        super().__init__(parent=parent)
        self.text_label = TextLabel(text, font_size=18)
        self.layout = QHBoxLayout()
        self.setProperty("state", state)
        self.__init_ui()

    def __init_ui(self):
        self.layout.addWidget(self.text_label, alignment=Qt.AlignCenter)
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName('check_widget')
        self.setStyleSheet('''
            #check_widget{
                border-radius: 6;
            }
            #check_widget[state="invalid"]{
                background-color: #ffe0e0;
            }
            #check_widget[state="valid"]{
                background-color: #d7f4d7;
            }
            #check_widget[state="none"]{
                background-color: #e1e1e1;
            }
        ''')
        self.setLayout(self.layout)

    def set_valid(self, text):
        self.text_label.setText(text)
        self.setProperty('state', "valid")
        self.style().polish(self)

    def set_invalid(self, text):
        self.text_label.setText(text)
        self.setProperty('state', "invalid")
        self.style().polish(self)

    def set_none(self, text):
        self.text_label.setText(text)
        self.setProperty('state', "none")
        self.style().polish(self)