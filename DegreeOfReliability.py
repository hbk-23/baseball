import glob
import BodyParts
import json

PlayerName = input("名前を入力してください: ")
keynumber = input("キーナンバーを入力してください: ")

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

# JSONファイルが格納されているディレクトリパス
directory_path = '/Users/hibiki/Documents/openpose/output/' + PlayerName + '/Json'

# ディレクトリ内のJSONファイルのパスを取得
json_files = glob.glob(directory_path + '/*.json')

a, b= BodyParts.BodyParts(int(keynumber))

x = []
y = []
real =[]

for file in json_files:
    with open(file, "r") as f:
            data = json.load(f)
    if len(data['people']) == 0:
        real.append(0)
    else:
        keypoints = data["people"][0]["pose_keypoints_2d"]
        x.append(keypoints[a])
        y.append(keypoints[a+1])    
        real.append(keypoints[b])

for i in range(len(real)):
        print(i, ':\t', 'x/', x[i], '\ty/', y[i], '\treal/', real[i])

# 出力用のデータを文字列として整形します
output_data = ""
for i in range(len(real)):
    output_data += f"{i}:\t x/{x[i]}\t y/{y[i]}\t real/{real[i]}\n"

# テキストファイルにデータを書き込みます
with open(directory_path + '/json_'+keynumber+'.txt', "w") as output_file:
    output_file.write(output_data)

# 出力完了メッセージ
print("保存完了")
