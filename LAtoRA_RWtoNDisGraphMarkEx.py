import glob
import matplotlib.pyplot as plt

import BodyParts
import Distance
import TextToArray
import filtering
import extremum as ex
import Difference
import marker
import judge
import SSE
import PositiveToNegative as PtoN

# ユーザーに文字の入力を求める
PlayerName = input("名前を入力してください: ")
'''
x_start = input("x軸の始まりを入力: ")
x_end = input("x軸の終わりを入力: ")
x_start = int(x_start)
x_end = int(x_end)
'''

# JSONファイルが格納されているディレクトリパス
directory_path = '/Users/hibiki/Documents/openpose/output/' + PlayerName + '/Json'

# ディレクトリ内のJSONファイルのパスを取得
json_files = glob.glob(directory_path + '/*.json')

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
RAnkle1, RAnkle2 = BodyParts.BodyParts(11) #右足首
LAnkle1, LAnkle2 = BodyParts.BodyParts(14) #左足首

# 各JSONファイルから座標を取得しリストに追加
right_ankle_coordinates = []
left_ankle_coordinates = []
for file in json_files:
    right_ankle_coordinates.append(Distance.get_joint_coordinates_from_json(file, RAnkle1, RAnkle2))
    left_ankle_coordinates.append(Distance.get_joint_coordinates_from_json(file, LAnkle1, LAnkle2))
       
"""
# 取得した座標を表示
for i, (neck_coordinates, right_wrist_coordinates) in enumerate(coordinates_list, 0):
    print(f"Frame {i+start}: Neck Coordinates: {neck_coordinates}, Right Wrist Coordinates: {right_wrist_coordinates}")
"""

# リストdisにフレーム番号と首と右手首の距離を入れる
dif1 = []
for j in range(len(json_files)):
    dif1.append([0, 0])
    dif1[j][0] = j
    dif1[j][1] = Difference.Dif(right_ankle_coordinates[j][1], left_ankle_coordinates[j][1])

    
#首と右手首
neck1, neck2 = BodyParts.BodyParts(1) #首
RWrist1, RWrist2 = BodyParts.BodyParts(4) #右手首

RElbow1, RElbow2 = BodyParts.BodyParts(3) #右肘
RShoulder1, RShoulder2 = BodyParts.BodyParts(2) #右肩
LShoulder1, LShoulder2 = BodyParts.BodyParts(5) #左肩

# 各JSONファイルから座標を取得しリストに追加
neck_coordinates=[]
right_wrist_coordinates=[]
right_elbow_coordinates=[]
right_shoulder_coordinates=[]
left_shoulder_coordinates=[]
for file in json_files:
    neck_coordinates.append(Distance.get_joint_coordinates_from_json(file, neck1, neck2))
    right_wrist_coordinates.append(Distance.get_joint_coordinates_from_json(file, RWrist1, RWrist2))
    right_elbow_coordinates.append(Distance.get_joint_coordinates_from_json(file, RElbow1, RElbow2))
    right_shoulder_coordinates.append(Distance.get_joint_coordinates_from_json(file, RShoulder1, RShoulder2))
    left_shoulder_coordinates.append(Distance.get_joint_coordinates_from_json(file, LShoulder1, LShoulder2))


# リストdisにフレーム番号と首と右手首の距離を入れる
dis2 = []
for j in range(len(json_files)):
    dis2.append([0, 0])
    dis2[j][0] = j
    dis2[j][1] = Distance.DisTwoPoints(neck_coordinates[j][0], neck_coordinates[j][1], right_wrist_coordinates[j][0], right_wrist_coordinates[j][1])


# データを定義
x1 = [row[0] for row in dif1]
y1 = [row[1] for row in dif1]
x2 = [row[0] for row in dis2]
y2 = [row[1] for row in dis2]

# データフィルタリング
filtered_x1, filtered_y1 = filtering.fitering(x1, y1)
filtered_x2, filtered_y2 = filtering.fitering(x2, y2)

lmax_x, lmin_x = ex.extremum(filtered_x2, filtered_y2)
lmax_xx = judge.distinction(lmax_x, neck_coordinates, right_wrist_coordinates)

Yzero = PtoN.PtoN(filtered_x1, filtered_y1)

SSE.line(left_shoulder_coordinates[lmax_xx[0]], right_shoulder_coordinates[lmax_xx[0]], right_elbow_coordinates[lmax_xx[0]])

# 折れ線グラフを描画
plt.plot(filtered_x1, filtered_y1, label='LAtoRA')
plt.plot(filtered_x2, filtered_y2, label='RWtoN')

# グラフの範囲を設定
# plt.xlim(x_start, x_end)

# 軸ラベルを付ける
plt.xlabel('frame')
plt.ylabel('Distance')

# 極大値
marker.mark(lmax_x, y2, plt, 'yellow', 0)
# 極小値
marker.mark(lmin_x, y2, plt, 'blue', 0)
# 条件付き極大値
marker.mark(lmax_xx, y2, plt, 'red', 0)
#正から負
plt.axvline(x=Yzero, color='green', linestyle='--')

# リリースフレームにラインを入れる
release = TextToArray.arrangement('/Users/hibiki/Documents/openpose/output/' + PlayerName + '/release.txt')
release = release[0]
plt.axvline(x=release, color='r', linestyle='--')

# グラフを保存
# plt.savefig('/Users/hibiki/Documents/openpose/output/' + PlayerName + '/' + 'ReleaseGraph.png')

# グラフを表示
plt.show()
