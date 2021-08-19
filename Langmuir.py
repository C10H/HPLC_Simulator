import numpy as np

"""
Langmuir.py 
生成Langmuir吸附等温索引表
朗格缪尔吸附等温式
生成结果交由nonlinear.py继续处理
朗格缪尔吸附等温式计算, x = qs * b * y / (1 + b * y), y为液相,x为固相
朗格缪尔吸附为单层吸附，理论上会得到拖尾的色谱峰
"""
import numpy as np
import matplotlib.pyplot as plt


class langmuir():
    def __init__(self, qs, b):
        self.y = np.arange(0, 10, 0.01)
        self.x = qs * b * self.y / (1 + b * self.y)


if __name__ == '__main__':
    y = langmuir(1, 1).y
    x = langmuir(1, 1).x
    plt.plot(y, x)
    plt.show()
