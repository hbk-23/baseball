import glob
import matplotlib.pyplot as plt

import BodyParts
import Distance
import TextToArray
import filtering

# ユーザーに文字の入力を求める
PlayerName = input("名前を入力してください: ")
x_start = input("x軸の始まりを入力: ")
x_end = input("x軸の終わりを入力: ")
x_start = int(x_start)
x_end = int(x_end)

# JSONファイルが格納されているディレクトリパス
directory_path = '/Users/hibiki/Documents/openpose/output/' + PlayerName + '/Json'

# ディレクトリ内のJSONファイルのパスを取得
json_files = glob.glob(directory_path + '/*.json')

# 首と手首の座標を格納するリスト
coordinates_list = []

#距離を求める部位を指定
'''
 0: 鼻
 1: 首
 2: 右肩
 3: 右肘
 4: 右手首
 5: 左肩
 6: 左肘
 7: 左手首
 8: 腰
 9: 右尻
10: 右膝
11: 右足首
12: 左尻
13: 左膝
14: 左足首
15: 右目
16: 左目
17: 右耳
18: 左耳
19: 左親指
20: 左小指
21: 左かかと
22: 右親指
23: 右小指
24: 右かかと
'''
a1, a2 = BodyParts.BodyParts(1) #首
b1, b2 = BodyParts.BodyParts(4) #右手首

# 各JSONファイルから座標を取得しリストに追加
for file in json_files:
    neck_coordinates, right_wrist_coordinates = Distance.get_joint_coordinates_from_json(file, a1, a2, b1, b2)
    coordinates_list.append((neck_coordinates, right_wrist_coordinates))
   
"""
# 取得した座標を表示
for i, (neck_coordinates, right_wrist_coordinates) in enumerate(coordinates_list, 0):
    print(f"Frame {i+start}: Neck Coordinates: {neck_coordinates}, Right Wrist Coordinates: {right_wrist_coordinates}")
"""

# リストdisにフレーム番号と首と右手首の距離を入れる
dis = []
for j in range(len(json_files)):
    dis.append([0, 0])
    dis[j][0] = j
    dis[j][1] = Distance.DisTwoPoints(coordinates_list[j][0][0], coordinates_list[j][0][1], coordinates_list[j][1][0], coordinates_list[j][1][1])

# データを定義
x = [row[0] for row in dis]
y = [row[1] for row in dis]

# データフィルタリング
filtered_x, filtered_y = filtering.fitering(x, y)

'''
# 折れ線グラフを描画
plt.plot(filtered_x, filtered_y)

# グラフの範囲を設定
plt.xlim(x_start, x_end)

# 軸ラベルを付ける
plt.xlabel('frame')
plt.ylabel('Distance')

"""
# 極大値
lmax_x = TextToArray.arrangement('/Users/hibiki/Documents/openpose/output/' + PlayerName + '/RWtoN_lmax.txt')
lmax_y = []
for i in range(len(lmax_x)):
    lmax_y.append(y[lmax_x[i]])
for j in range(len(lmax_x)):
    plt.scatter(lmax_x[j], lmax_y[j], color='yellow', marker='o')
    plt.text(lmax_x[j], lmax_y[j], 'frame' + str(lmax_x[j]))

# 極小値
lmin_x = TextToArray.arrangement('/Users/hibiki/Documents/openpose/output/' + PlayerName + '/RWtoN_lmin.txt')     
lmin_y = []
for i in range(len(lmin_x)):
    lmin_y.append(y[lmin_x[i]])
for j in range(len(lmin_x)):
    plt.scatter(lmin_x[j], lmin_y[j], color='blue', marker='o')
    plt.text(lmin_x[j], lmin_y[j], 'frame' + str(lmin_x[j]))
"""

# リリースフレーム
release = TextToArray.arrangement('/Users/hibiki/Documents/openpose/output/' + PlayerName + '/release.txt')
release = release[0]
# マーカーをつける
marker_x = release
marker_y = y[release]
plt.scatter(marker_x, marker_y, color='red', marker='o')
plt.text(marker_x, marker_y, 'frame' + str(release))

# グラフを保存
plt.savefig('/Users/hibiki/Documents/openpose/output/' + PlayerName + '/' + 'RWtoNgraphExtremum_' + str(x_start) + '-' + str(x_end) + '.png')

# グラフを表示
plt.show()
'''
