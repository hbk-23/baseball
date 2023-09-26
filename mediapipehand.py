import cv2
import glob
import os
import csv
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def fields_name():
    # CSVのヘッダを準備
    fields = []
    fields.append('file_name')
    for i in range(21):
        fields.append(str(i)+'_x')
        fields.append(str(i)+'_y')
        fields.append(str(i)+'_z')
    return fields

if __name__ == '__main__':
    # 元の画像ファイルの保存先を準備
    resource_dir = r'./data'
    # 対象画像の一覧を取得
    file_list = glob.glob(os.path.join(resource_dir, "*.jpg"))

    # 保存先の用意
    save_csv_dir = './result/csv'
    os.makedirs(save_csv_dir, exist_ok=True)
    save_csv_name = 'landmark.csv'
    save_image_dir = 'result/image'
    os.makedirs(save_image_dir, exist_ok=True)

    with mp_hands.Hands(static_image_mode=True,
            max_num_hands=1, # 検出する手の数（最大2まで）
            min_detection_confidence=0.5) as hands, \
        open(os.path.join(save_csv_dir, save_csv_name), 
            'w', encoding='utf-8', newline="") as f:

        # csv writer の用意
        writer = csv.DictWriter(f, fieldnames=fields_name())
        writer.writeheader()

        for file_path in file_list:
            # 画像の読み込み
            image = cv2.imread(file_path)

            # 鏡写しの状態で処理を行うため反転
            image = cv2.flip(image, 1)

            # OpenCVとMediaPipeでRGBの並びが違うため、
            # 処理前に変換しておく。
            # CV2:BGR → MediaPipe:RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # 推論処理
            results = hands.process(image)

            # 前処理の変換を戻しておく。
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if not results.multi_hand_landmarks:
                # 検出できなかった場合はcontinue
                continue

            # ランドマークの座標情報
            landmarks = results.multi_hand_landmarks[0]

            # CSVに書き込み
            record = {}
            record["file_name"] = os.path.basename(file_path)
            for i, landmark in enumerate(landmarks.landmark):
                record[str(i) + '_x'] = landmark.x
                record[str(i) + '_y'] = landmark.y
                record[str(i) + '_z'] = landmark.z
            writer.writerow(record)

            # 元画像上にランドマークを描画
            mp_drawing.draw_landmarks(
                image,
                landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
            # 画像を保存
            cv2.imwrite(
                os.path.join(save_image_dir, os.path.basename(file_path)),
                cv2.flip(image, 1))
