import numpy as np
import matplotlib.pyplot as plt
import cv2
import mediapipe as mp
import pandas as pd

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# 動画ファイルのパスを指定
input_filename = 'Aoyagi01.mp4'  

# 動画データを読み込む
video_data = cv2.VideoCapture(input_filename)
video_width = int(video_data.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(video_data.get(cv2.CAP_PROP_FRAME_HEIGHT))
video_fps = int(video_data.get(cv2.CAP_PROP_FPS))

print('FPS:', video_fps)
print('Dimensions:', video_width, video_height)

video_data_array = []

print("VideoFrame:", int(video_data.get(cv2.CAP_PROP_FRAME_COUNT)))

# ファイルが正常に読み込めている間ループする
while video_data.isOpened():
    # 1フレームごとに読み込み
    success, image = video_data.read()
    if success:
        # フレームの画像を追加
        video_data_array.append(image)
    else:
        break
video_data.release()
print('Frames Read:', len(video_data_array))

with mp_pose.Pose(
    static_image_mode=False,
    model_complexity=2,
    enable_segmentation=True,
    min_detection_confidence=0.1) as pose:

    # 動画データをループ処理
    for loop_counter, image_data in enumerate(video_data_array):

        # 画像解析
        results = pose.process(cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB))
        # pose.processメソッドは、画像データを受け取り、ポーズ推定を行う
        # cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)を使用して、OpenCVのBGR形式の画像をRGB形式に変換
        # resultsオブジェクトには、Mediapipeポーズ推定の結果が含まれています。以下にresultsオブジェクトが持つ主な属性とそれぞれの意味を示します。
        # results.pose_landmarks: これは推定されたポーズのランドマーク情報を含むオブジェクトです。各特徴点の座標が含まれており、ランドマークごとに以下のような情報が提供されます。
        # x: 特徴点のX座標（0から1の範囲）
        # y: 特徴点のY座標（0から1の範囲）
        # z: 特徴点のZ座標（カメラからの距離、3Dポーズ推定時のみ）
        # results.segmentation_mask: セグメンテーションマスクのデータが含まれます。セグメンテーションは人物のシルエットを分割するためのもので、オプションで有効にされている場合に利用できます。
        # results.pose_world_landmarks: 3D空間座標でのポーズのランドマーク情報を含むオブジェクトです。各特徴点の3D座標が含まれています。

        if not results.pose_landmarks:
            continue

        # 解析結果から右ひじの座標を取得
        right_elbow_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
        right_elbow_x = right_elbow_landmark.x * video_width
        right_elbow_y = right_elbow_landmark.y * video_height

        # 右ひじの座標をターミナルに表示
        print(f"Frame {loop_counter}: Right Elbow - X: {right_elbow_x:.2f}, Y: {right_elbow_y:.2f}")

        # 解析結果を動画に描画
        mp_drawing.draw_landmarks(
            image_data,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())


plt.imshow(cv2.cvtColor(video_data_array[0], cv2.COLOR_BGR2RGB))
plt.tight_layout()

output_filename = 'output_movie_aoyagi.mp4'
# 出力形式を指定する
output_file = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc(*'MP4V'), video_fps, (video_width, video_height))
# 動画出力処理
for video_data in video_data_array:
    output_file.write(video_data)

output_file.release()
