import sys

def arrangement(file):
    array = []
    with open(file, 'r', encoding='utf-8') as fin:  # ファイルを開く
        for line in fin.readlines():  # 行を読み込んでfor文で回す
            try:
                num = int(line)  # 行を整数（int）に変換する
            except ValueError as e:
                print(e, file=sys.stderr)  # エラーが出たら画面に出力
                continue

            array.append(num)  # 変換した整数をリストに保存する
    
    return array
