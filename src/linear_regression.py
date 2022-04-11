# This program finds a linear fit between rainfall received (in mm) and forest cover (fraction)
# I know that there are inbuilt packages for linear regression
# I wrote the code myself because we were taught how to do this in this course

# Slope: 0.0008587709484891744
# Intercept: -0.17015471066607185
# R^2: 0.9399832140229545

import numpy as np
import os
from matplotlib import pyplot as plt

def get_r_squared(m, c, x, y):
    y_hat = m * x + c
    SSE = np.sum((y - y_hat)**2)
    SST = np.sum((y - np.mean(y))**2)
    r_squared = 1 - (SSE / SST)
    return r_squared

if __name__ == '__main__':
    data = np.transpose(np.loadtxt(os.path.join(os.path.dirname(__file__), "rainfall.txt"), float))
    x, y = data[0], data[1]
    N = len(x)

    Ex, Ey, Exx, Exy = 0, 0, 0, 0

    for xi, yi in zip(x, y):
        Ex += xi
        Ey += yi
        Exx += xi * xi
        Exy += xi * yi

    Ex /= N
    Ey /= N
    Exx /= N
    Exy /= N

    plt.title("Rainfall vs Forest cover")
    plt.xlabel("Rainfall (mm)")
    plt.ylabel("Forest cover (fraction)")
    plt.plot(x, y, "ko")

    m = (Exy - Ex * Ey) / (Exx - Ex * Ex)
    c = (Exx * Ey - Ex * Exy) / (Exx - Ex * Ex)
    r_squared = get_r_squared(m, c, x, y)

    print(f"Slope: {m}")
    print(f"Intercept: {c}")
    print(f"R^2: {r_squared}")

    x_line = np.array(x)
    y_line = m * x_line + c
    plt.plot(x_line, y_line)
    plt.show()