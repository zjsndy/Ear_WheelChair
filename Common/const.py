from typing import Union

TAB_NAME_LIST = ['配置页面', '可视化页面', '实验页面', '控制页面']
INIT_TAB_INDEX = 0

TAB_BUTTON_SIZE = TAB_BAR_WIDTH = 60
ELECTRODE_BUTTON_SIZE = 48

TOP_BAR_HEIGHT = 65

EAR_MAX_CH_NUM = 2
EAR_ELECTRODE_NAMES = ['E1', 'E2']


MAX_TIME_WINDOW = 10
MIN_TIME_WINDOW = 2

MAX_CHANNEL_SCALE = 10000
MIN_CHANNEL_SCALE = 1

MAX_FILTER = 100.0
MIN_FILTER = 0.1

TRANS_RATE = 10
REFRESH_RATE = 10

CHANNEL_CURVE_COLORS = ['#4ee07c','#454d67', '#f9ad00',  '#2cc6c8', '#a780f3',
                        '#e9cc40', '#a1a1a1', '#5cb1ee', '#f8c094', '#a8f0be',
                        '#cab3f8', '#81ddde', '#9acff5']

SAMPLE_RATE = 500

CUE_TIME = 2

DEFAULT_CONFIG = {
    "left_channel_num": 1,
    "left_channel_name": [
        "E1"
    ],
    
    "right_channel_num":1,
    "right_channel_name":[
        "E2"
    ],
    
    "left_device_address":"49:91:A5:0A:90:22",
    "right_device_address":" FA:95:1C:6A:F2:2B",
    "plot_twindow": 5,
    "channel_scale": 100,
    "filter": False,
    "fmin": 4.0,
    "fmax": 40.0,

    "trial": 10,
    "session": 1,
    "paradigm": 0,
    "rest_time": 2,
    "perform_time": 4,
}

PARADIGMS = [
    {
        'paradigm': 'grit_tooth',
        'movements': ['grit_tooth_move', 'no_move']
    },
    
    {
        'paradigm': 'open_eye',
        'movements': ['open_eye_move','no_move']
    },
    
    {
        'paradigm': 'close_eye',
        'movements': ['close_eye_move', 'no_move']
    }
]

DESCRIPTION = {
    'grit_tooth': '咬牙运动',
    'grit_tooth_move': '咬牙运动',
    
    'open_eye': '睁眼运动',
    'open_eye_move': '睁眼运动',
    
    'close_eye': '闭眼运动',
    'close_eye_move': '闭眼运动',
    
    'no_move': '静息',
}

SERVICE_UUID = "0000fff0-0000-1000-8000-00805f9b34fb"
NOTIFY_UUID = "0000fff1-0000-1000-8000-00805f9b34fb"

WHEELCHAIR = {
    'port': 'COM10',
    'baudrate': 9600,
}

BLE_DATA_OFFSET = 4
BLE_DATA_BYTE_LEN = 30
BLE_DATA_MILLI_VOLT = 5000
BLE_DATA_FULL_RANGE = 16777215
BLE_DATA_AMP_RATE = 24

def parse_earphone_data_frame(data_bytes: Union[bytes, bytearray]):
    if data_bytes[:4] != bytearray([0xff, 0xff, 0x01, 0x1f]):
        print("帧头不正确，丢弃数据")
        return None  # 丢弃该数据包
    
    if type(data_bytes) is bytes:
        data_bytes = bytearray(data_bytes)
    
    pt_list = []
    for i in range(BLE_DATA_OFFSET, BLE_DATA_OFFSET + BLE_DATA_BYTE_LEN, 3):
        sub_bytes = data_bytes[i:i + 3]
        data_value = (sub_bytes[0] << 16) + (sub_bytes[1] << 8) + sub_bytes[2]
        if data_value & (1 << 23):
            data_value -= (2 ** 24)  # 将数据转换为负数表示
        
        # 数据运算
        processed_value = float(data_value) * 2500000 / ((2 ** 23) - 1) / 24
        pt_list.append(processed_value)
    # print(processed_value)
    return pt_list