import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

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
dominant = input("left of right: ")
real = input("信頼度： ")
save = input("保存する場合は1： ")

real = float(real)
save = int(save)
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
    right_ankle_coordinates.append(Distance.get_joint_coordinates_from_json(file, RAnkle1, RAnkle2, real))
    left_ankle_coordinates.append(Distance.get_joint_coordinates_from_json(file, LAnkle1, LAnkle2, real))
       
"""
# 取得した座標を表示
for i, (neck_coordinates, right_wrist_coordinates) in enumerate(coordinates_list, 0):
    print(f"Frame {i+start}: Neck Coordinates: {neck_coordinates}, Right Wrist Coordinates: {right_wrist_coordinates}")
"""

# リストdisにフレーム番号と右足首と左足首のy差を入れる
dif1 = []
for j in range(len(json_files)):
    dif1.append([0, 0])
    dif1[j][0] = j
    if dominant == "right":
        dif1[j][1] = Difference.Dif(right_ankle_coordinates[j][1], left_ankle_coordinates[j][1])
    if dominant == "left":
        dif1[j][1] = Difference.Dif(left_ankle_coordinates[j][1], right_ankle_coordinates[j][1])
    
#首と右手首
neck1, neck2 = BodyParts.BodyParts(1) #首
if dominant == 'right':
    Wrist1, Wrist2 = BodyParts.BodyParts(4) #手首
    Elbow1, Elbow2 = BodyParts.BodyParts(3) #肘
if dominant == 'left':
    Wrist1, Wrist2 = BodyParts.BodyParts(7) #手首
    Elbow1, Elbow2 = BodyParts.BodyParts(6) #肘    
RShoulder1, RShoulder2 = BodyParts.BodyParts(2) #右肩
LShoulder1, LShoulder2 = BodyParts.BodyParts(5) #左肩

# 各JSONファイルから座標を取得しリストに追加
neck_coordinates=[]
wrist_coordinates=[]
elbow_coordinates=[]
right_shoulder_coordinates=[]
left_shoulder_coordinates=[]
for file in json_files:
    neck_coordinates.append(Distance.get_joint_coordinates_from_json(file, neck1, neck2, real))
    wrist_coordinates.append(Distance.get_joint_coordinates_from_json(file, Wrist1, Wrist2, real))
    elbow_coordinates.append(Distance.get_joint_coordinates_from_json(file, Elbow1, Elbow2, real))
    right_shoulder_coordinates.append(Distance.get_joint_coordinates_from_json(file, RShoulder1, RShoulder2, real))
    left_shoulder_coordinates.append(Distance.get_joint_coordinates_from_json(file, LShoulder1, LShoulder2, real))


# リストdisにフレーム番号と首と右手首の距離を入れる
dis2 = []
for j in range(len(json_files)):
    dis2.append([0, 0])
    dis2[j][0] = j
    dis2[j][1] = Distance.DisTwoPoints(right_shoulder_coordinates[j][0], right_shoulder_coordinates[j][1], wrist_coordinates[j][0], wrist_coordinates[j][1])


# データを定義
x1 = [row[0] for row in dif1]
y1 = [row[1] for row in dif1]
x2 = [row[0] for row in dis2]
y2 = [row[1] for row in dis2]

# データフィルタリング
filtered_x1, filtered_y1 = filtering.fitering(x1, y1)
filtered_x2, filtered_y2 = filtering.fitering(x2, y2)

lmax_x, lmin_x = ex.extremum(filtered_x2, filtered_y2)
if dominant == 'right':
    lmax_xx = judge.distinction(lmax_x, right_shoulder_coordinates, wrist_coordinates)
if dominant == 'left':
    lmax_xx = judge.distinction(lmax_x, wrist_coordinates, left_shoulder_coordinates)

Yzero = PtoN.PtoN(filtered_x1, filtered_y1)
for i in range(len(lmax_xx)):
    if lmax_xx[i] > Yzero:
        release = lmax_xx[i]
        break

SSE.line(left_shoulder_coordinates[release], right_shoulder_coordinates[release], elbow_coordinates[release])

# ウィンドウサイズを指定してfigureオブジェクトを作成
plt.figure(figsize=(10, 7))  # 幅10インチ、高さ7インチ

# 折れ線グラフを描画
plt.subplot(2, 1, 1)
plt.plot(filtered_x1, filtered_y1, label='LAtoRA')
plt.plot(filtered_x2, filtered_y2, label='RWtoN')

# グラフの範囲を設定
# plt.xlim(x_start, x_end)

# 軸ラベルを付ける
plt.xlabel('frame')
plt.ylabel('Distance')

# 極大値
# marker.markAR(lmax_x, y2, plt, 'yellow', 0)
# 条件付き極大値
marker.markAR(lmax_xx, y2, plt, 'lime', 0)
# リリース
marker.mark(release, y2, plt, 'red', 1)
# 正から負
marker.line(Yzero, plt, 'blue', '--', 1)

'''
# リリースフレームにラインを入れる
self_release = TextToArray.arrangement('/Users/hibiki/Documents/openpose/output/' + PlayerName + '/release.txt')
self_release = self_release[0]
plt.axvline(x=self_release, color='r', linestyle='--')
'''
# y=0にラインを入れる
plt.axhline(y=0, color='black', linestyle='-')

# 画像の読み込み
img = mpimg.imread("/Users/hibiki/Documents/openpose/output/" + PlayerName + "/frame/frame_" + str(release) + ".jpg")

# 画像を表示するためのサブプロットを作成
plt.subplot(2, 1, 2)
plt.imshow(img)
# plt.title('frame_' + str(release))
plt.axis('off')  # 軸を表示しない

if(save == 1):
    # 保存
    plt.savefig('/Users/hibiki/Documents/openpose/output/' + PlayerName + '/' + 'ReleaseFrameGraph.png')



# 表示
plt.show()
