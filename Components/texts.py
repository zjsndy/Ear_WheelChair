from PyQt5.QtWidgets import QLabel, QTextBrowser


class TextLabel(QLabel):
    def __init__(self, text=None, font_size=18, parent=None):
        super().__init__(text=text, parent=parent)
        self.style_sheet = f'''
            QLabel{{
                font-family: Baloo 2, ChillDuanSans;
                font-weight: bold;
                font-size: {font_size}px;
                color: #606060;
            }}
        '''
        self.__init_ui()

    def __init_ui(self):
        self.setStyleSheet(self.style_sheet)


class BandTextLabel(QLabel):
    def __init__(self, text=None, parent=None):
        super().__init__(text=text, parent=parent)
        self.style_sheet = '''
            QLabel{
                font-family: Goldman;
                font-weight: bold;
                font-size: 30px;
                color: #666666;
            }
        '''
        self.__init_ui()

    def __init_ui(self):
        self.setStyleSheet(self.style_sheet)


class TextView(QTextBrowser):

    def __init__(self, text=None, font_size=18, parent=None):
        super().__init__(parent=parent)
        self.style_sheet = f'''
                    QTextBrowser{{
                        font-family: Baloo 2, ChillDuanSans;
                        font-weight: bold;
                        font-size: {font_size}px;
                        color: #606060;
                        background-color: #ffffff;
                        border: 0;
                        border-radius: 10;
                    }}
                '''
        self.setText(text)
        self.__init_ui()

    def __init_ui(self):
        self.setStyleSheet(self.style_sheet)
