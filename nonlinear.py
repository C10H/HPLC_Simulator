"""
by C10H15N
2021.8.14
nonlinear.py
为本模拟器中负责非线性情况的模块
非线性情况下,进样量会对色谱图线形状作出改变,因此有必要对进样量进行考察
实验数据的质量会对模拟结果产生较大影响
输入数据包括色谱柱参数，吸附脱附曲线和模拟条件三大类
假定吸附和脱附曲线重合，根据相律，两相分配池内总样品量与平衡时固相量与液相量一一对应
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import interpolate


class Nonlinear():
    def __init__(self,
                 theoretical_plate_number,  # USP理论塔板数
                 column_length,  # 柱管长度（cm）
                 column_diameter,  # 柱管直径（mm）
                 flow,  # 流速（ml/min）
                 dead_time,  # 死时间（min）假定死时间是流动相刚好充满空色谱柱所需的时间
                 inject_time,  # 进样时间（min）如果是瞬间进样则进样时间为0
                 inject_volume,  # 进样体积
                 duration,  # 分析总时长（min）
                 sheet,  # 实验所得数据
                 savepath='nonlinear.png'
                 ):
        def sheet_processing(sheet_init, p):
            total = sheet_init['x'] * p + sheet_init['y'] * (1 - p)
            return {
                'x': sheet_init['x'],
                'y': sheet_init['y'],
                'px+(1-p)y': total
            }

        def equilibrium(y, x, sheet, p):
            total = x * p + y * (1 - p)
            y_end = np.interp(total, sheet['px+(1-p)y'], sheet['y'])
            x_end = np.interp(total, sheet['px+(1-p)y'], sheet['x'])
            return [x_end, y_end]

        self.name = 'linear'
        self.volume = (column_length / 100) * math.pi * (column_diameter / 1000) ** 2 * 0.25  # 计算柱管体积后
        self.packing_fraction = dead_time * flow / 1e6 / self.volume
        # packing fraction为充填率，指固相材料占据整根色谱柱的体积比率
        self.freq = (flow / 1e6) / ((self.volume / theoretical_plate_number) * (
                1 - self.packing_fraction))  # 每分钟通过多少塔板
        # 进样量暂时按照进1个塔板的体积来处理
        status_flow = np.zeros(theoretical_plate_number)
        # 流动相初始化，在未进样的状态下，每个色谱塔板的y均为0
        status_solid = np.zeros(theoretical_plate_number)
        # 流动相初始化，在未进样的状态下，每个色谱塔板的x均为0
        detector = []
        # 检测器，记录某时间下最后一块理论塔板的流动相浓度
        turns = int(duration * self.freq)
        # 循环计算轮数，也可以认为是流动相通过的"两相分配池数"，等于采样时间*每分钟通过多少塔板.由于算法限制，需要将循环计算轮数设置为整数
        sheet = sheet_processing(sheet, self.packing_fraction)
        if inject_time != 0:  # 进样时间不可忽略
            inject_turns = int(inject_time * self.freq)
            # 进样轮数，也可以认为是流动相通过的"两相分配池数"，等于采样时间*每分钟通过多少塔板.由于算法限制，需要将循环计算轮数设置为整数
            inject_volume_per_turn = inject_volume / inject_turns  # 平均到每块塔板上的进样量
            # 分配  持续进样
            for i in range(turns):
                # 仿真时间，即为流动相流过多少个理论塔板的时间，range内的数值按需更改
                for j in range(theoretical_plate_number):
                    status_solid[j], status_flow[j] = equilibrium(y=status_flow[j], x=status_solid[j], sheet=sheet,
                                                                  p=self.packing_fraction)  # 线性情况
                if i <= inject_turns:  # 进样阶段,先流过带有样品浓度一致的流动相
                    detector.append(status_flow[theoretical_plate_number - 1])  # 检测器，记录某时间下最后一块理论塔板的流动相浓度
                    status_flow = np.concatenate(([inject_volume_per_turn], status_flow))
                else:  # 进样结束,此时开始流过不带样品的流动相
                    detector.append(status_flow[theoretical_plate_number - 1])  # 检测器，记录某时间下最后一块理论塔板的流动相浓度
                    status_flow = np.concatenate(([0], status_flow))
        elif inject_time == 0:
            # 分配  瞬间进样
            status_flow[0] = inject_volume / (
                        self.volume * self.packing_fraction / theoretical_plate_number)  # 假定瞬间进样，样品在第一个样品池，求得的两相分配池浓度
            for i in range(turns):
                # 仿真时间，即为流动相流过多少个理论塔板的时间，range内的数值按需更改
                for j in range(theoretical_plate_number):
                    status_solid[j], status_flow[j] = equilibrium(y=status_flow[j], x=status_solid[j], sheet=sheet,
                                                                  p=self.packing_fraction)  # 非线性情况
                detector.append(status_flow[theoretical_plate_number - 1])
                # 检测器，记录某时间下最后一块理论塔板的流动相浓度
                status_flow = np.concatenate(([0], status_flow))
        self.detector = detector

        plt.plot(np.arange(0, turns) / self.freq, detector)
        plt.savefig(savepath)
        plt.close()


if __name__ == '__main__':  # 测试用例
    qs = 1
    b = 1
    y = np.arange(0, 10, 0.01)
    x = qs * b * y / (1 + b * y)
    sheet = {
        'px+(1-p)y': np.array([0]),
        'x': x,
        'y': y
    }
    Nonlinear(theoretical_plate_number=150,
              column_length=25,
              column_diameter=5,
              flow=1.000,
              dead_time=2.454,
              inject_time=0.2,
              inject_volume=5,
              duration=7.5,
              sheet=sheet)  # 测试用例1
