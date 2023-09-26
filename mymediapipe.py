import cv2
import mediapipe as mp

# Mediapipeの姿勢推定モジュールを初期化
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# カメラからビデオストリームを取得
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    # cap.read()でカメラからのフレームを読み込み、成功するかどうかをretに格納し、フレーム自体をframeに格納
    if not ret:
        continue

    # フレームをRGBに変換
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # cv2.cvtColor()を使用して、BGR形式のカラーチャンネルをRGBに変換

    # 姿勢推定を実行
    results = pose.process(rgb_frame)
    # pose.process()を使用して、姿勢推定を実行し、その結果をresultsに格納

    if results.pose_landmarks:
        for landmark in results.pose_landmarks.landmark:
            ih, iw, _ = frame.shape
            x, y = int(landmark.x * iw), int(landmark.y * ih)
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
    # results.pose_landmarksが存在する場合（つまり、姿勢が検出された場合）、姿勢の各関節の位置を取得し、それに対応する画像上の座標を計算
    # cv2.circle()を使用して、計算された座標に緑色の円を描画

        # ランドマークのリストのインデックスに基づいて特定のランドマークを選択
        left_shoulder_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        
        # フレームの高さと幅を取得
        ih, iw, _ = frame.shape
        
        # ランドマークの相対座標を絶対座標に変換
        x = int(left_shoulder_landmark.x * iw)
        y = int(left_shoulder_landmark.y * ih)
        
        # 座標を表示
        print("Left Shoulder Coordinates (x, y):", x, y)

    cv2.imshow('Pose Estimation', frame)
    # cv2.imshow()で描画されたフレームを表示

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # cv2.waitKey()でキーボード入力を待ち、"q"キーが押されるとループを終了

cap.release()
cv2.destroyAllWindows()
# ビデオストリームを解放し、ウィンドウを閉じる
