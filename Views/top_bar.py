from PyQt5.QtGui import QIcon, QColor, QPaintEvent, QPainter
from PyQt5.QtWidgets import QAction, QGraphicsDropShadowEffect, QWidget, QHBoxLayout, QStyleOption

from Components import *
#from config import CONFIG


class TopBar(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.band_widget = BandTextLabel(text='Ear_WheelChair')
        self.tab_name_widget = TextLabel('', font_size=20)
        self.ext_menu = IconButton(icon='menu.png', parent=self)
        self.layout = QHBoxLayout()
        self.top_menu = DropMenu()
        self.__init_ui()

    def __init_ui(self):
        self.layout.addWidget(self.band_widget, alignment=Qt.AlignCenter)
        self.layout.addStretch(1)
        self.layout.addWidget(self.tab_name_widget)
        self.layout.addStretch(1)
        self.layout.addWidget(self.ext_menu, alignment=Qt.AlignCenter)
        self.layout.setContentsMargins(15, 0, 10, 0)
        self.setLayout(self.layout)
        self.setObjectName('top_bar')
        self.setStyleSheet('''
            #top_bar{
                background-color:#ffffff;
                margin: 0;
                padding: 0;
                border-bottom: 0 solid #cccccc;
                border-top-left-radius: 10;
                border-top-right-radius: 10;
            }
        ''')
        self.setFixedHeight(TOP_BAR_HEIGHT)

        # 给TopBar添加底部阴影
        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(222, 222, 222))
        shadow.setBlurRadius(8)
        shadow.setOffset(0, 3)
        self.setGraphicsEffect(shadow)

        self.ext_menu.setMenu(self.top_menu)

        self.on_switch_tab(INIT_TAB_INDEX)

    def on_switch_tab(self, index):
        self.tab_name_widget.setText(TAB_NAME_LIST[index])

    def paintEvent(self, a0: QPaintEvent) -> None:
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, painter, self)
