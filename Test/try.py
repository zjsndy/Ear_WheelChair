from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QComboBox, QLabel
from bleak import BleakClient
import asyncio

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 左耳设备
        self.left_device_combobox = QComboBox()
        self.left_device_combobox.addItems(["Device_L1", "Device_L2"])  # 示例设备地址
        self.connect_left_button = QPushButton("Connect to Left Ear Device")
        self.check_left_connect_widget_left = QLabel("Left Status: Not Connected")

        # 右耳设备
        self.right_device_combobox = QComboBox()
        self.right_device_combobox.addItems(["Device_R1", "Device_R2"])  # 示例设备地址
        self.connect_right_button = QPushButton("Connect to Right Ear Device")
        self.check_left_connect_widget_right = QLabel("Right Status: Not Connected")

        # 同时连接按钮
        self.connect_both_button = QPushButton("Connect Both Devices")
        self.both_status_label = QLabel("Both Status: Not Connected")

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Left Ear:"))
        layout.addWidget(self.left_device_combobox)
        layout.addWidget(self.connect_left_button)
        layout.addWidget(self.check_left_connect_widget_left)

        layout.addWidget(QLabel("Right Ear:"))
        layout.addWidget(self.right_device_combobox)
        layout.addWidget(self.connect_right_button)
        layout.addWidget(self.check_left_connect_widget_right)

        layout.addWidget(self.connect_both_button)
        layout.addWidget(self.both_status_label)

        self.setLayout(layout)

        # 连接按钮到槽函数
        self.connect_left_button.clicked.connect(lambda: self.connect_to_device(self.left_device_combobox.currentText(), "Left"))
        self.connect_right_button.clicked.connect(lambda: self.connect_to_device(self.right_device_combobox.currentText(), "Right"))
        self.connect_both_button.clicked.connect(self.connect_both_devices)

    def connect_to_device(self, device_address, side):
        """单独连接某一耳机设备"""
        asyncio.create_task(self.connect_device_async(device_address, side))

    async def connect_device_async(self, device_address, side):
        """异步连接单个蓝牙设备"""
        try:
            print(f"尝试连接到 {side} 设备: {device_address}")
            client = BleakClient(device_address, timeout=5)
            await client.connect()

            if client.is_connected:
                self.update_status(f"{side} Bluetooth Connected", side)
                print(f"{side} 连接成功")
            else:
                self.update_status(f"{side} Bluetooth Failed", side)
                print(f"{side} 连接失败")
        except Exception as e:
            self.update_status(f"{side} Error: {str(e)}", side)
            print(f"{side} 异常: {e}")
        finally:
            if client and client.is_connected:
                await client.disconnect()

    async def connect_both_devices_async(self):
        """并行连接左右耳设备"""
        left_address = self.left_device_combobox.currentText()
        right_address = self.right_device_combobox.currentText()

        tasks = [
            self.connect_device_async(left_address, "Left"),
            self.connect_device_async(right_address, "Right")
        ]
        await asyncio.gather(*tasks)

    def connect_both_devices(self):
        """启动并行连接任务"""
        asyncio.create_task(self.connect_both_devices_async())

    def update_status(self, message, side):
        """更新状态标签"""
        if side == "Left":
            self.check_left_connect_widget_left.setText(message)
        elif side == "Right":
            self.check_left_connect_widget_right.setText(message)
        elif side == "Both":
            self.both_status_label.setText(message)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
