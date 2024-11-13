import os
import sys

from PyQt5.QtGui import QFont
from scipy.signal import filtfilt, butter


def band_pass_filter(data, axis, fs, fmin, fmax):
    b, a = butter(2, [fmin * 2 / fs, fmax * 2 / fs], 'bandpass')
    filtered_data = filtfilt(b, a, data, axis=axis)
    return filtered_data
def get_abs_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception as e:
        # print(f'get_abs_path error: {e}')
        base_path = os.path.abspath(".")
    return os.path.abspath(os.path.join(base_path, relative_path)).replace("\\", "/")

def get_plot_font():
    font = QFont()
    font.setFamily('Baloo 2')
    font.setPixelSize(18)
    font.setWeight(600)
    return font