import numpy as np
import pyqtgraph as pg


from Common import *


class DataPlotItem(pg.PlotItem):
    def __init__(self, channel_num, channel_names, sample_rate, time_window, channel_scale):
        super().__init__()
        self.sample_rate = sample_rate
        self.sample_cnt = 0
        self.time_window = time_window  #   5
        self.refresh_rate = REFRESH_RATE
        self.channel_scale = channel_scale
        self.channel_curves = []
        self.channel_offsets = []
        self.channel_num = channel_num
        if isinstance(channel_names, str):
            self.channel_names = [f'{channel_names + str(i)}' for i in range(1, channel_num + 1)]
        else:
            assert len(channel_names) == self.channel_num
            self.channel_names = channel_names
        self.channel_names = channel_names

        self.x_labels = []
        self.x_indices = []
        self.x_ticks = []
        self.y_labels = []
        self.y_index = []
        self.y_ticks = []
        self.line = None
        self.data_buffer = None
        self.scanline_pos = 0
        self.__init_ui()

    def __init_ui(self):
        self.setMouseEnabled(x=False, y=False)
        self.hideButtons()
        self.showGrid(x=False, y=False, alpha=0.2)
        # 添加各个导联的曲线以及导联的偏移量
        self.__set_channel_offsets()
        self.__set_channel_curves()
        # 添加扫描线
        self.__set_scanline()
        # 设置XY轴范围
        self.setXRange(0, self.sample_rate * self.time_window)
        self.setYRange(0, self.channel_num)
        # 设置x轴坐标刻度标签
        self.getAxis('bottom').setStyle(tickTextOffset=10, tickFont=get_plot_font())
        self.getAxis('bottom').setHeight(30)
        self.getAxis('bottom').setPen(color='#757575', width=2)
        self.__set_x_ticks()
        # 设置y轴坐标刻度标签
        self.getAxis('left').setStyle(tickTextOffset=10, tickLength=0, tickFont=get_plot_font())
        self.getAxis('left').setWidth(75)
        self.getAxis('left').setPen(color='#ffffff')

        self.__set_y_labels()
        self.__set_y_ticks()
        self.data_buffer = np.zeros((self.channel_num, MAX_TIME_WINDOW * self.sample_rate))

    def __set_channel_curves(self):
        for i in range(self.channel_num):
            self.channel_curves.append(
                pg.PlotDataItem(pen=pg.mkPen(color=CHANNEL_CURVE_COLORS[i % len(CHANNEL_CURVE_COLORS)], width=1.5)))
            self.addItem(self.channel_curves[i])
            self.channel_curves[i].setData(np.zeros(self.time_window * self.sample_rate) + self.channel_offsets[i])

    def __set_scanline(self):
        self.line = pg.InfiniteLine(pen=pg.mkPen(color='#1967d2', width=1.5), pos=self.scanline_pos)
        self.addItem(self.line)

    def __set_channel_offsets(self):
        self.channel_offsets = []
        for i in range(self.channel_num):
            self.channel_offsets.append((self.channel_num - i - 1) + 1.0 / 2)

    def __set_y_labels(self):
        self.y_labels = []
        for channel_name in self.channel_names:
            self.y_labels.append(channel_name)
        self.y_labels.reverse()

    def __set_y_ticks(self):
        self.y_index = np.arange(1.0 / 2, self.channel_num, 1)
        self.y_ticks = [(i, j) for i, j in zip(self.y_index, self.y_labels)]
        self.getAxis('left').setTicks([self.y_ticks])

    def __set_x_ticks(self):
        self.x_indices = []
        self.x_labels = []
        index = self.time_window * self.sample_rate
        while index >= 0:
            self.x_indices.append(index)
            self.x_labels.append('')
            index -= self.sample_rate
        self.x_ticks = [(idx, lb) for idx, lb in zip(self.x_indices, self.x_labels)]
        self.getAxis('bottom').setTicks([self.x_ticks])

    # 更新数据的方法：为了不让已经显示过的数据改变（尤其是滤波之后会影响之前的数据），
    # 使用局部更新的方法，即已经显示过的数据不变，只改变新传过来的数据
    def plot_data(self, data):
        self.data_buffer = data.transpose()
        self.data_buffer /= self.channel_scale
        sample_num = self.sample_rate // self.refresh_rate
        window_sample_num = self.time_window * self.sample_rate
        for i in range(self.channel_num):
            plot_data = self.channel_curves[i].getData()[1]
            if self.scanline_pos + sample_num > window_sample_num:
                # |--sample_a----||*********||---sample_b---|
                sample_a_num = self.scanline_pos + sample_num - window_sample_num
                plot_data[self.scanline_pos:] = self.data_buffer[-sample_num:-sample_a_num] + self.channel_offsets[i]
                plot_data[:sample_a_num] = self.data_buffer[-sample_a_num:] + self.channel_offsets[i]
            else:
                plot_data[self.scanline_pos:self.scanline_pos + sample_num] = (
                        self.data_buffer[i][-sample_num:] + self.channel_offsets[i])
            self.channel_curves[i].setData(plot_data)
        self.scanline_pos = (self.scanline_pos + sample_num) % window_sample_num
        self.line.setPos(self.scanline_pos)
        self.sample_cnt += sample_num
        

    def on_channel_scale_changed(self, channel_scale):
        # 如果在这里设置Y的范围，那么会导致在下一次画图之前设置了Y的范围，通道的数据瞬间下移
        # 暂时的解决办法：画图函数里面每次都设置X Y轴的配置
        # 更新: 通过改变当前所有通道的数据偏移
        for i in range(self.channel_num):
            plot_data = (self.channel_curves[i].getData()[1] - self.channel_offsets[i]) \
                        * self.channel_scale / channel_scale + self.channel_offsets[i]
            self.channel_curves[i].setData(plot_data)
        self.channel_scale = channel_scale
        self.__set_y_ticks()

    def on_plot_twindow_changed(self, time_window):
        # 当时间窗口修改时，可能需要用到之前的数据，data_buffer就是这个功能，存下最长时间窗口的样本
        window_sample_num = self.sample_rate * time_window
        # 首先修改X轴的范围
        self.setXRange(0, window_sample_num, padding=0.02)
        self.scanline_pos = self.sample_cnt % window_sample_num
        self.line.setPos(self.scanline_pos)
        for i in range(self.channel_num):
            plot_data = np.zeros(window_sample_num) + self.channel_offsets[i]
            if self.scanline_pos:
                plot_data[:self.scanline_pos] = self.data_buffer[i][-self.scanline_pos:]
                plot_data[self.scanline_pos:] = self.data_buffer[i][-window_sample_num:-self.scanline_pos]
            else:
                plot_data = self.data_buffer[i][-window_sample_num:]
            self.channel_curves[i].setData(plot_data + self.channel_offsets[i])
        self.time_window = time_window
        self.__set_x_ticks()

    def on_channel_changed(self, channel_num, channel_names):
        self.channel_num = channel_num
        self.channel_names = channel_names
        self.reset()

    def reset(self):
        self.sample_cnt = 0
        self.data_buffer = np.zeros((self.channel_num, MAX_TIME_WINDOW * self.sample_rate))
        self.scanline_pos = self.sample_cnt % (self.sample_rate * self.time_window)
        self.setXRange(0, self.sample_rate * self.time_window, padding=0.02)
        self.setYRange(0, self.channel_num, padding=0.02)
        self.__set_x_ticks()
        self.__set_y_labels()
        self.__set_y_ticks()
        self.__set_channel_offsets()
        self.__remove_plot_items()
        self.__set_channel_curves()
        self.__set_scanline()

    def __remove_plot_items(self):
        for i in range(len(self.channel_curves)):
            self.removeItem(self.channel_curves[i])
        self.channel_curves = []
        self.removeItem(self.line)


class DataPlotWidget(pg.PlotWidget):
    def __init__(self, channel_num, channel_names, sample_rate, time_window, channel_scale):
        super().__init__(plotItem=DataPlotItem(channel_num, channel_names, sample_rate, time_window, channel_scale))
        self.setBackground('#ffffff')
