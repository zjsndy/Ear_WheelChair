import asyncio
import os.path

from PyQt5.QtGui import QPaintEvent, QPainter
from PyQt5.QtWidgets import QGridLayout, QWidget, QHBoxLayout, QVBoxLayout, QStyleOption
from bleak import BleakScanner, BleakClient

from Config import GLOBAL_CONFIG
from Device import BlueToothDevice

from Processor import scanbluetooth
from Components import *
#from config import CONFIG


class ConfigTab(QWidget):
    connect_left_device_signal = pyqtSignal()
    disconnect_left_device_signal = pyqtSignal()
    connect_right_device_signal = pyqtSignal()
    disconnect_right_device_signal = pyqtSignal()
    
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.left_client = None
        self.right_client = None
        
        self.layout = QHBoxLayout()
        self.input_layout_top = QGridLayout()
        self.input_layout_bottom = QGridLayout()
        self.config_layout = QVBoxLayout()
        self.empty_layout = QGridLayout()
        self.left_button_layout = QHBoxLayout()
        self.right_button_layout = QHBoxLayout()
        self.wheal_chair = QGridLayout()
        self.chair_button_layout = QHBoxLayout()
        
        self.config_widget = QWidget(parent = self)
        self.empty_widget = QWidget(parent = self)
        
        self.check_left_connect_Widget = CheckWidget()
        self.check_right_connect_Widget = CheckWidget()
        
        self.left_device_combobox = InputComboBox()
        self.right_device_combobox = InputComboBox()
        self.wheal_chair_combobox = InputComboBox()
        
        self.wheelchair_potter_rate_input = InputSpinBox(2000, 100000, 1000, False)
        
        
        self.scan_left_button = ClickButton('扫描', 'OK')
        self.connect_left_button = ClickButton('连接','OK')
        self.disconnect_left_button = ClickButton('断开','OK')
        self.scan_right_button = ClickButton('扫描', 'OK')
        self.connect_right_button = ClickButton('连接', 'OK')
        self.disconnect_right_button = ClickButton('断开', 'OK')
        self.connect_chair_button = ClickButton('连接', 'OK')
        self.disconnect_chair_button = ClickButton('断开', 'OK')
        
        self.left_button_layout.addWidget(self.scan_left_button)
        self.left_button_layout.addSpacing(10)
        self.left_button_layout.addWidget(self.connect_left_button)
        self.left_button_layout.addSpacing(10)
        self.left_button_layout.addWidget(self.disconnect_left_button)
        
        self.right_button_layout.addWidget(self.scan_right_button)
        self.right_button_layout.addWidget(self.connect_right_button)
        self.right_button_layout.addWidget(self.disconnect_right_button)
        
        self.chair_button_layout.addWidget(self.connect_chair_button)
        self.chair_button_layout.addWidget(self.disconnect_chair_button)
        
        
        self.__init_ui()
        self.__init_slot()
        self.set_config()
        
    def __init_ui(self):
        self.input_layout_top.addWidget(TextLabel(text = '左耳'), 1, 0, 1, 4)
        self.input_layout_top.addWidget(self.left_device_combobox, 2, 0, 1, 4)
        self.input_layout_top.addWidget(TextLabel(text = '扫描信息'), 3, 0, 1, 4)
        self.input_layout_top.addWidget(self.check_left_connect_Widget, 4, 0, 1, 4)
        self.check_left_connect_Widget.set_invalid('未连接')
        self.input_layout_top.addLayout(self.left_button_layout, 5, 0, 1, 4)
        self.input_layout_top.setHorizontalSpacing(10)
        self.input_layout_top.setVerticalSpacing(15)

        self.input_layout_bottom.addWidget(TextLabel(text = '右耳'), 1, 0, 1, 4)
        self.input_layout_bottom.addWidget(self.right_device_combobox, 2, 0, 1, 4)
        self.input_layout_bottom.addWidget(TextLabel(text = '扫描信息'), 3, 0, 1, 4)
        self.input_layout_bottom.addWidget(self.check_right_connect_Widget, 4, 0, 1, 4)
        self.check_right_connect_Widget.set_invalid('未连接')
        self.input_layout_bottom.addLayout(self.right_button_layout, 5, 0, 1, 4)
        self.input_layout_top.setHorizontalSpacing(10)
        self.input_layout_top.setVerticalSpacing(15)
        
        self.wheal_chair.addWidget(TextLabel(text = '轮椅COM端口'), 1, 0, 1, 4)
        self.wheal_chair.addWidget(self.wheal_chair_combobox, 2, 0, 1, 4)
        self.wheal_chair_combobox.setCurrentText("待定")
        self.wheal_chair.addWidget(TextLabel(text = '波特率'),3, 0, 1, 4)
        self.wheal_chair.addWidget(self.wheelchair_potter_rate_input, 4, 0, 1, 4)
        self.wheal_chair.addLayout(self.chair_button_layout, 5, 0, 1, 4)
        self.input_layout_top.setHorizontalSpacing(10)
        self.input_layout_top.setVerticalSpacing(15)
        
        
        
        
        self.config_layout.addLayout(self.input_layout_top)
        self.config_layout.addStretch(1)
        self.config_layout.addLayout(self.input_layout_bottom)
        self.config_layout.addStretch(1)
        self.config_layout.addLayout(self.wheal_chair)
        
        self.config_layout.setSpacing(20)
        self.config_layout.setContentsMargins(30, 30, 30, 30)
        
        self.layout.setAlignment(Qt.AlignLeft)
        self.config_widget.setFixedWidth(320)
        self.config_widget.setLayout(self.config_layout)
        self.config_widget.setObjectName('config_widget')
        self.config_widget.setStyleSheet('''
                   #config_widget{
                       border-right: 2 solid #eeeeee;
                   }
               ''')
        
        self.empty_widget.setFixedSize(720,720)
        
        self.layout.addWidget(self.config_widget)
        self.layout.addWidget(self.empty_widget)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
    def __init_slot(self):
        self.scan_left_button.clicked.connect(self.scan_left_bluetooth)
        self.scan_right_button.clicked.connect(self.scan_right_bluetooth)
        # self.connect_left_button.clicked.connect(self.connect_to_left_device)
        self.connect_right_button.clicked.connect(self.connect_to_right_device)
        # self.disconnect_left_button.clicked.connect(self.disconnect_left_device)
        self.disconnect_right_button.clicked.connect(self.disconnect_right_device)
        self.connect_left_button.clicked.connect(self.on_connect_left_device)

    def set_config(self):
        self.left_device_combobox.addItems([GLOBAL_CONFIG.left_device_address])
        self.right_device_combobox.addItems([GLOBAL_CONFIG.right_device_address])
        self.change_left_device_connect(False)
        self.change_right_device_connect(False)

    def change_left_device_connect(self, connected):
        if connected:
             self.check_left_connect_Widget.set_valid(text = '已连接')
        else:
            self.check_right_connect_Widget.set_invalid(text = '未连接')

    def change_right_device_connect(self, connected):
        if connected:
            self.check_right_connect_Widget.set_valid(text = '已连接')
        else:
            self.check_right_connect_Widget.set_invalid(text = '未连接')
            
    def scan_left_bluetooth(self):
        self.scanbluetooth = scanbluetooth()
        self.scanbluetooth.scanFinished.connect(self.update_Left_ComBox)
        self.scanbluetooth.start()
       
    def update_Left_ComBox(self,devices):
        self.left_device_combobox.clear()
        for device in devices:
            self.left_device_combobox.addItem(f"{device.address}")
            
    def on_connect_left_device(self):
        self.connect_left_device_signal.emit()
       
      
    # def connect_to_left_device(self):
    #     device_address = self.left_device_combobox.currentText()
    #     print(f'选择的左耳蓝牙设备地址:{device_address}')
    #     # 获取 QApplication 的事件循环
    #     loop = asyncio.get_event_loop()
    #     if loop.is_running():
    #         # 如果事件循环正在运行，使用 create_task 启动异步任务
    #         loop.create_task(self.connect_left_device(device_address))
    #     else:
    #         # 如果事件循环没有运行，使用 run_until_complete 启动协程
    #         loop.run_until_complete(self.connect_left_device(device_address))
    #
    # async def connect_left_device(self, device_address):
    #     try:
    #         print("尝试连接到设备...")
    #         self.left_client = BleakClient(device_address, timeout = 5)
    #         await self.left_client.connect()
    #         if self.left_client.is_connected:
    #             self.check_left_connect_Widget.set_valid('蓝牙连接成功')
    #             self.connect_left_device_signal.emit()
    #             print('连接成功')
    #         else:
    #             self.check_left_connect_Widget.set_invalid('蓝牙连接失败')
    #             print('连接失败')
    #     except Exception as e:
    #         self.check_left_connect_Widget.set_invalid('未连接')
    #         print(f'异常: {e}')
    # def disconnect_from_left_device(self):
    #     loop = asyncio.get_event_loop()
    #     if loop.is_running():
    #         loop.create_task(self.disconnect_left_device())
    #     else:
    #         loop.run_until_complete(self.disconnect_left_device())
    #
    # async def disconnect_left_device(self):
    #     try:
    #         if hasattr(self, 'left_client') and self.left_client is not None:
    #             if self.left_client.is_connected:
    #                 print("尝试断开连接...")
    #                 await self.left_client.disconnect()
    #                 self.disconnect_left_device_signal.emit()
    #                 self.check_left_connect_Widget.set_valid('蓝牙连接已断开')
    #                 print('断开连接成功')
    #             else:
    #                 self.check_left_connect_Widget.set_invalid('设备未连接')
    #                 print('设备未连接')
    #         else:
    #             self.check_left_connect_Widget.set_invalid('未初始化连接')
    #             print('未初始化连接')
    #     except Exception as e:
    #         self.check_left_connect_Widget.set_invalid(f'断开连接时发生异常: {str(e)}')
    #         print(f'异常: {e}')

    def scan_right_bluetooth(self):
        self.scanbluetooth = scanbluetooth()
        self.scanbluetooth.scanFinished.connect(self.update_Right_ComBox)
        self.scanbluetooth.start()
        
    def update_Right_ComBox(self,devices):
        self.right_device_combobox.clear()
        for device in devices:
            self.right_device_combobox.addItem(f"{device.address}")
            
    def connect_to_right_device(self):
        device_address = self.right_device_combobox.currentText()
        print(f'选择的左耳蓝牙设备地址:{device_address}')
        # 获取 QApplication 的事件循环
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # 如果事件循环正在运行，使用 create_task 启动异步任务
            loop.create_task(self.connect_right_device(device_address))
        else:
            # 如果事件循环没有运行，使用 run_until_complete 启动协程
            loop.run_until_complete(self.connect_right_device(device_address))
    
    async def connect_right_device(self, device_address):
        try:
            print("尝试连接到设备...")
            self.right_client = BleakClient(device_address, timeout = 5)
            await self.right_client.connect()
            if self.right_client.is_connected:
                self.check_right_connect_Widget.set_valid('蓝牙连接成功')
                self.connect_right_device_signal.emit()
                print('连接成功')
            else:
                self.check_right_connect_Widget.set_valid('蓝牙连接失败')
                print('连接失败')
        except Exception as e:
            self.check_right_connect_Widget.set_valid(f'状态:{str(e)}')
            print(f'异常: {e}')
    
    def disconnect_from_right_device(self):
        asyncio.create_task(self.disconnect_right_device())
    async def disconnect_right_device(self):
        try:
            if hasattr(self, 'right_client') and self.right_client is not None:
                if self.right_client.is_connected:
                    print("尝试断开连接...")
                    await self.right_client.disconnect()
                    self.check_right_connect_Widget.set_valid('蓝牙连接已断开')
                    self.disconnect_right_device_signal.emit()
                    print('断开连接成功')
                else:
                    self.check_right_connect_Widget.set_valid('设备未连接')
                    print('设备未连接')
            else:
                self.check_right_connect_Widget.set_valid('未初始化连接')
                print('未初始化连接')
        except Exception as e:
            self.check_right_connect_Widget.set_valid(f'断开连接时发生异常: {str(e)}')
            print(f'异常: {e}')
            
    def paintEvent(self, a0: QPaintEvent) -> None:
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, painter, self)
    
    
