import json
import math

# JSONファイルから各座標を取得する関数
def get_joint_coordinates_from_json(file, a1, a2, trust):
    with open(file, "r") as f:
        data = json.load(f)
    if len(data['people']) == 0:
        point1 = [0, 0]
    else:
        keypoints = data["people"][0]["pose_keypoints_2d"]
        if keypoints[a2] > trust:
            point1 = keypoints[a1:a2]
        else:
            point1 = [0, 0]
    return point1

# 距離を求める
def DisTwoPoints(x1, y1, x2, y2):
    if x1!=0 and y2!=0 and x2!=0 and y2!=0:
        dis = math.sqrt(((x1-x2)**2) + ((y1-y2)**2))
        return dis
    else:
        return 0
