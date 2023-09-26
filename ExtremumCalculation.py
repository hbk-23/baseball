import RWtoNDisGraphMarkEx as RWtoN
import TextToArray
import matplotlib.pyplot as plt

x = RWtoN.filtered_x
y = RWtoN.filtered_y

def LocalMaximum(y, w):
    Rating = []
    for i in range(len(y)):
        Rating.append(0)

    for i in range(len(y)):
        try:
            if y[i]-y[i-1] > w or y[i]-y[i+1] > w:
                    if y[i] > y[i-1]:
                        Rating[i] += 1
                        try:
                            if y[i] > y[i+1]:
                                Rating[i] += 1
                        except:
                            continue
        except:
            continue
            
    maxl = []
    for i in range(len(Rating)):
        if Rating[i] == 2:
            maxl.append(i)
    return maxl


def LocalMinimum(y, w):
    Rating = []
    for i in range(len(y)):
        Rating.append(0)

    for i in range(len(y)):
        try:
            if y[i-1]-y[i] > w or y[i+1]-y[i] > w:
                    if y[i] < y[i-1]:
                        Rating[i] += 1
                        try:
                            if y[i] < y[i+1]:
                                Rating[i] += 1
                        except:
                            continue
        except:
            continue
            
    minl = []
    for i in range(len(Rating)):
        if Rating[i] == 2:
            minl.append(i)
    return minl

w = 0
Rating1=LocalMaximum(y, w)
print(Rating1)
Rating2=LocalMinimum(y, w)
print(Rating2)

# 折れ線グラフを描画
plt.plot(x, y)


# グラフの範囲を設定
plt.xlim(RWtoN.x_start, RWtoN.x_end)


# 軸ラベルを付ける
plt.xlabel('frame')
plt.ylabel('Distance')


# 極大値
lmax_x = Rating1
lmax_y = []
for i in range(len(lmax_x)):
    lmax_y.append(y[lmax_x[i]])
for j in range(len(lmax_x)):
    plt.scatter(lmax_x[j], lmax_y[j], color='yellow', marker='o')
    # plt.text(lmax_x[j], lmax_y[j], 'frame' + str(lmax_x[j]))

# 極小値
lmin_x = Rating2     
lmin_y = []
for i in range(len(lmin_x)):
    lmin_y.append(y[lmin_x[i]])
for j in range(len(lmin_x)):
    plt.scatter(lmin_x[j], lmin_y[j], color='blue', marker='o')
    # plt.text(lmin_x[j], lmin_y[j], 'frame' + str(lmin_x[j]))

# リリースフレーム
release = TextToArray.arrangement('/Users/hibiki/Documents/openpose/output/' + RWtoN.PlayerName + '/release.txt')
release = release[0]
# マーカーをつける
marker_x = release
marker_y = y[release]
plt.scatter(marker_x, marker_y, color='red', marker='o')
plt.text(marker_x, marker_y, 'frame' + str(release))  

# グラフを保存
# plt.savefig('/Users/hibiki/Documents/openpose/output/' + PlayerName + '/' + 'LAtoRAgraphExtremum_' + str(x_start) + '-' + str(x_end) + '.png')

# グラフを表示
plt.show()