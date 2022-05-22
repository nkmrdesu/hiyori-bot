import datetime

def main(msg):
    # コマンド横の数字（持ち越し時間）を抜き出す処理
    delCommandMsg = msg.replace('/time', '')
    # ２桁持ち越し秒数か判定
    carryOverTime = 0
    errMsg1 = "持ち越し時間の指定がおかしいよ。コマンドを確認してみてね。"
    try:
        carryOverTime = int(delCommandMsg[:2])
    except ValueError:
        return errMsg1
    # 持ち越し時間の変換チェック
    if 20 < carryOverTime < 90:
        # 改行コードごとにリスト格納
        lines = msg.split('\n')
        result = []
        # １行ずつ処理
        for line in lines:
            msgs = line.split()
            resultmsg = []
            isFirst = True
            for msg in msgs:
                if isFirst:
                    try:
                        # 最初の文字列ブロックを変換
                        datetimeObj = datetime.datetime.strptime(msg, '%M:%S') 
                        # 持ち越し時間のオブジェクト
                        carryOverTimeObj = datetime.timedelta(seconds=carryOverTime)
                        # 基準時間（90秒）のオブジェクト
                        standardTime = datetime.timedelta(seconds=90)
                        # 実際に引く時間を算出
                        minusTime = standardTime - carryOverTimeObj
                        # TL時間を計算
                        resultTimeObj = datetimeObj - minusTime
                        # バトル終了している時間の場合0000に置き換え
                        if resultTimeObj.strftime('%Y') == '1899':
                            resultTime = '00:00'
                        else:
                            resultTime = resultTimeObj.strftime('%M:%S') 
                        resultmsg.append(resultTime)
                        isFirst = False
                    except ValueError:
                        # 変換できない文字列はTL行でないとみなしてそのまま
                        if '/time' in msg:
                            resultmsg.append('持ち越し用にTLを変換したよ。')
                        else:
                            resultmsg.append(msg)
                        isFirst = False
                else:
                    resultmsg.append(msg)
            resultmsgStr = ' '.join(resultmsg)
            result.append(resultmsgStr)
        return '\n'.join(result)
    else:
        return errMsg1
