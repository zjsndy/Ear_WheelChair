from PyQt5.QtGui import QPaintEvent, QPainter
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QStyleOption, QStyle

from Components import *


class MainTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.layout = QHBoxLayout()
        self.__init_ui()

    def __init_ui(self):
        self.label = TextLabel(text='<center>欢迎来到智能轮椅系统!',
                               font_size=30)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def paintEvent(self, a0: QPaintEvent) -> None:
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, painter, self)
