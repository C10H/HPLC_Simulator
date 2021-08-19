"""
Toth.py
生成Toth吸附等温索引表
Toth吸附等温式
生成结果交由nonlinear.py继续处理
Toth吸附等温式计算, x = VL * b * y / (1 + b ^ n * y) ^ (1 / n), y为液相,x为固相
"""

import numpy as np
import matplotlib.pyplot as plt


class toth():
    def __init__(self, Vl, b, n):
        self.y = np.arange(0, 10, 0.01)
        self.x = Vl * b * self.y / (1 + b ** n * self.y) ** (1 / n)


if __name__ == '__main__':
    y = toth(1, 1, 2).y
    x = toth(1, 1, 2).x
    plt.plot(y, x)
    plt.show()
    plt.close()
