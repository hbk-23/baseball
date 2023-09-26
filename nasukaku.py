import math

def calculate_angle(m1, m2):
    angle = math.atan(abs((m2 - m1) / (1 + m1 * m2)))
    return math.degrees(angle)  # 弧度を度に変換

# 2つの直線の傾きを設定
m1 = 1
m2 = -1

angle = calculate_angle(m1, m2)
print(f"なす角: {angle} 度")
