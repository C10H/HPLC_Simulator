"""
BiLangmuir.py
手性拆分色谱图线模拟
双朗格缪尔吸附等温方程，分为非手性吸附位点与手性吸附位点
两相分配池平衡机制
入:液相R型，液相S型，固相R型，固相S型
出:平衡后的液相R型，液相S型，固相R型，固相S型
平衡过程中，R构型样品总量与S构型样品总量不变
使用scipy.optimize.fsolve求取平衡结果
我们认定R构型与S构型的紫外光谱图线相同的
后期考虑将插值求解改成多项式拟合/泰勒公式求解
"""

from scipy.optimize import fsolve
import numpy as np
import matplotlib.pyplot as plt
import math


class BiLangmuir:
    def __init__(self, qns, kns, qs1, ks1, qs2, ks2,  # 吸附数据
                 theoretical_plate_number,  # USP理论塔板数
                 column_length,  # 柱管长度（cm）
                 column_diameter,  # 柱管直径（mm）
                 flow,  # 流速（ml/min）
                 dead_time,  # 死时间（min）假定死时间是流动相刚好充满空色谱柱所需的时间
                 inject_time,  # 进样时间（min）如果是瞬间进样则进样时间为0
                 inject_volume,  # 进样体积,消旋进样体积
                 duration,  # 分析总时长（min）
                 savepath='BiLangmuir.png'
                 ):
        def equilibrium(s1, f1, s2, f2, p):
            total_r = s1 * p + f1 * (1 - p)
            total_s = s2 * p + f2 + (1 - p)

            def solve_function(unsolved_value):
                s1_equ, f1_equ, s2_equ, f2_equ = unsolved_value[0], unsolved_value[1], unsolved_value[2], \
                                                 unsolved_value[3]
                return [
                    s1_equ * p + f1_equ * (1 - p) - total_r,
                    s2_equ * p + f2_equ + (1 - p) - total_s,
                    qns * kns * (f1_equ + f2_equ) / (1 + kns * (f1_equ + f2_equ))
                    + qs1 * ks1 * f1_equ / (1 + ks1 * f1_equ) - s1_equ,
                    qns * kns * (f1_equ + f2_equ) / (1 + kns * (f1_equ + f2_equ))
                    + qs2 * ks2 * f2_equ / (1 + ks2 * f1_equ) - s2_equ
                ]

            solved = fsolve(solve_function, [s1, f1, s2, f2])
            s1_final, f1_final, s2_final, f2_final = solved[0], solved[1], solved[2], solved[3]
            return s1_final, f1_final, s2_final, f2_final

        # step1:预处理色谱数据
        self.name = 'Bi-Langmuir'
        self.volume = (column_length / 100) * math.pi * (column_diameter / 1000) ** 2 * 0.25  # 计算柱管体积后
        self.packing_fraction = dead_time * flow / 1e6 / self.volume
        # packing fraction为充填率，指固相材料占据整根色谱柱的体积比率
        self.freq = (flow / 1e6) / ((self.volume / theoretical_plate_number) * (
                1 - self.packing_fraction))  # 每分钟通过多少塔板
        # 进样量暂时按照进1个塔板的体积来处理
        status_flow_r = np.zeros(theoretical_plate_number)
        status_flow_s = np.zeros(theoretical_plate_number)
        # 流动相初始化，在未进样的状态下，每个色谱塔板的y均为0
        status_solid_r = np.zeros(theoretical_plate_number)
        status_solid_s = np.zeros(theoretical_plate_number)
        # 流动相初始化，在未进样的状态下，每个色谱塔板的x均为0
        detector_r = []
        detector_s = []
        # 虚拟的分别检测R,S构型含量检测器，记录某时间下最后一块理论塔板的流动相浓度
        inject_volume_r = inject_volume / 2  # 消旋体中，R，S构型摩尔分数分别为50%
        inject_volume_s = inject_volume / 2
        turns = int(duration * self.freq)

        # step3 循环计算
        # 循环计算轮数，也可以认为是流动相通过的"两相分配池数"，等于采样时间*每分钟通过多少塔板.由于算法限制，需要将循环计算轮数设置为整数
        if inject_time != 0 and theoretical_plate_number > 100:  # 进样时间不可忽略
            inject_turns = int(inject_time * self.freq)
            # 进样轮数，也可以认为是流动相通过的"两相分配池数"，等于采样时间*每分钟通过多少塔板.由于算法限制，需要将循环计算轮数设置为整数
            inject_volume_per_turn = inject_volume / inject_turns / 2  # 平均到每块塔板上各自消旋体分别的进样量
            # 分配  持续进样
            for i in range(turns):
                # 仿真时间，即为流动相流过多少个理论塔板的时间，range内的数值按需更改
                for j in range(theoretical_plate_number):
                    status_solid_r[j], status_flow_r[j], status_solid_s[j], status_flow_s[j] = equilibrium(
                        status_solid_r[j], status_flow_r[j], status_solid_s[j], status_flow_s[j],
                        p=self.packing_fraction
                    )  # 双Langmuir拆分情况
                if i <= inject_turns:  # 进样阶段,先流过带有样品浓度一致的流动相
                    status_flow_r = np.concatenate(([inject_volume_per_turn], status_flow_r))
                    status_flow_s = np.concatenate(([inject_volume_per_turn], status_flow_s))
                else:  # 进样结束,此时开始流过不带样品的流动相
                    status_flow_r = np.concatenate(([0], status_flow_r))
                    status_flow_s = np.concatenate(([0], status_flow_s))
                detector_r.append(status_flow_r[theoretical_plate_number - 1])  # 检测器，记录某时间下最后一块理论塔板的流动相浓度
                detector_s.append(status_flow_s[theoretical_plate_number - 1])  # 检测器，记录某时间下最后一块理论塔板的流动相浓度
        else:
            # 分配  瞬间进样
            status_flow_r[0] = inject_volume_r / (
                    self.volume * self.packing_fraction / theoretical_plate_number)  # 假定瞬间进样，样品在第一个样品池，求得的两相分配池浓度
            status_flow_s[0] = inject_volume_s / (
                    self.volume * self.packing_fraction / theoretical_plate_number)  # 假定瞬间进样，样品在第一个样品池，求得的两相分配池浓度
            for i in range(turns):
                # 仿真时间，即为流动相流过多少个理论塔板的时间，range内的数值按需更改
                for j in range(theoretical_plate_number):
                    status_solid_r[j], status_flow_r[j], status_solid_s[j], status_flow_s[j] = equilibrium(
                        status_solid_r[j], status_flow_r[j], status_solid_s[j], status_flow_s[j],
                        p=self.packing_fraction
                    )  # 双Langmuir拆分情况
                detector_r.append(status_flow_r[theoretical_plate_number - 1])
                detector_s.append(status_flow_s[theoretical_plate_number - 1])
                # 检测器，记录某时间下最后一块理论塔板的流动相浓度
                status_flow_r = np.concatenate(([0], status_flow_r))
                status_flow_s = np.concatenate(([0], status_flow_s))
        self.detector = np.array(detector_r) + np.array(detector_s)

        plt.plot(np.arange(0, turns) / self.freq, self.detector)
        plt.savefig(savepath)
        plt.close()


if __name__ == '__main__':  # 测试用例
    BiLangmuir(0.5, 0.5, 0.6, 0.6, 0.4, 0.4,
               theoretical_plate_number=150,
               column_length=25,
               column_diameter=5,
               flow=1.000,
               dead_time=2.454,
               inject_time=0.2,
               inject_volume=5,
               duration=7.5
               )
