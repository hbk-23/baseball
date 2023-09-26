import numpy as np
import matplotlib.pyplot as plt
import RWtoNDisGraphMarkEx as RWtoN

# データ点の生成（法則のないデータ）
x = RWtoN.filtered_x
y = RWtoN.filtered_y

# 多項式フィッティング
degree = 10  # 多項式の次数
coefficients = np.polyfit(x, y, degree)
poly = np.poly1d(coefficients)
x_fit = np.linspace(RWtoN.x_start, RWtoN.x_end, 100)
y_fit = poly(x_fit)

# データとフィット結果のプロット
plt.scatter(x, y, label='Data')
plt.plot(x_fit, y_fit, color='red', label='Fitted Curve')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()
