import json
import math
import glob

# JSONファイルから首と手首の座標を取得する関数
def get_joint_coordinates_from_json(file):
    with open(file, "r") as f:
        data = json.load(f)
    if len(data['people']) == 0:
        neck_coordinates = [0, 0]
        right_wrist_coordinates = [0, 0]
    else:
        keypoints = data["people"][0]["pose_keypoints_2d"]
        neck_coordinates = keypoints[3:5]
        right_wrist_coordinates = keypoints[12:14]
    return neck_coordinates, right_wrist_coordinates

# 手首と首の距離を測る
def ReleasePoint(x1, y1, x2, y2):
    if x1!=0 and y2!=0 and x2!=0 and y2!=0:
        dis = math.sqrt(((x1-x2)**2) + ((y1-y2)**2))
        return dis
    else:
        return 0

# ユーザーに文字の入力を求める
PlayerName = input("名前を入力してください: ")
JsonType = input("jsonファイル名を入力: ")
start = input("フレームの始まりを入力: ")
display = input("全表示なら0,上位10なら10: ")

# JSONファイルが格納されているディレクトリパス
directory_path = '/Users/hibiki/Documents/openpose/output/' + PlayerName + '/' + JsonType

# ディレクトリ内のJSONファイルのパスを取得
json_files = glob.glob(directory_path + '/*.json')

# 首と手首の座標を格納するリスト
coordinates_list = []

# 各JSONファイルから座標を取得しリストに追加
for file in json_files:
    neck_coordinates, right_wrist_coordinates = get_joint_coordinates_from_json(file)
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
    dis[j][1] = ReleasePoint(coordinates_list[j][0][0], coordinates_list[j][0][1], coordinates_list[j][1][0], coordinates_list[j][1][1])

# 距離に注目して昇順にソート
dis = sorted(dis, reverse=True, key=lambda x: x[1])

# ソートしたものを表示
start = int(start)
if(display == '0'):
    for k in range(len(json_files)):
        print(f"{k+1}\tFrame: {dis[k][0]+start}\tDistance: {dis[k][1]}")
else:
    for k in range(int(display)):
        print(f"{k+1}\tFrame: {dis[k][0]+start}\tDistance: {dis[k][1]}")

