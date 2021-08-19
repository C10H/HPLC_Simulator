"""
BET.py
生成BET吸附等温索引表
BET吸附等温式
生成结果交由nonlinear.py继续处理
BET吸附等温式计算, x = x0 * c * y / (y0 - y) / (1 + (c - 1) * (y / y0)), y为液相,x为固相
"""

import numpy as np
import matplotlib.pyplot as plt


class BET():  # 测试用例, BET的y取值范围0-0.9
    def __init__(self, x0, y0, c):
        self.y = np.arange(0, 0.9, 0.01)
        self.x = x0 * c * self.y / (y0 - self.y) / (1 + (c - 1) * (self.y / y0))


if __name__ == '__main__':
    y = BET(1, 1, 2).y
    x = BET(1, 1, 2).x
    plt.plot(y, x)
    plt.show()
    plt.close()
