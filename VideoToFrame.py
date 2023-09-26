import cv2
import os

def video_to_frames(video_path, output_path):
    # 動画の読み込み
    video = cv2.VideoCapture(video_path)

    # フレーム数の取得
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # 出力先のフォルダを作成
    os.makedirs(output_path, exist_ok=True)

    # フレームごとに処理
    for frame_number in range(total_frames):
        # フレームの読み込み
        ret, frame = video.read()

        if ret:
            # 出力ファイル名の生成
            output_filename = os.path.join(output_path, f"frame_{frame_number:04d}.jpg")

            # フレーム画像の保存
            cv2.imwrite(output_filename, frame)

    # メモリの解放
    video.release()

# 動画のパスとフレーム画像の出力先パスを指定
# video_path = input("動画パス入力: ")
# output_path = input("保存先パス入力: ")

video_path = "C:/Users/hibiki/Documents/output_movie_aoyagi.mp4"
output_path = "C:/Users/hibiki/Documents"

# 作成するフォルダのパス
folder_path = output_path + "/frame2"

# 動画をフレーム画像に分解
video_to_frames(video_path, folder_path)

print("フレーム画像の生成が完了しました。")
