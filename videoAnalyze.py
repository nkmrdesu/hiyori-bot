import os
import requests
import json

def main(msg):
    # リクエストURIを生成
    getUri = 'https://prilog.jp/rest/analyze?Url={key1}&Token={key2}'
    apiToken = os.environ['PRILOG_TOKEN']
    requestUri = getUri.format(key1 = msg, key2= apiToken)
    # リクエスト送信
    requestResult = requests.get(requestUri)
    # 文字コードを直してJSON形式に変換
    requestResult.encoding = requestResult.apparent_encoding
    resultJson = requestResult.json()
    # 結果を作成
    statusCode = resultJson['status']
    print(statusCode)
    if statusCode == 200 or statusCode == 201:
        title = json.dumps(resultJson['result']['title'], ensure_ascii=False)
        print(title)
        timeline = json.dumps(resultJson['result']['timeline_enemy'], ensure_ascii=False)
        damage = json.dumps(resultJson['result']['total_damage'], ensure_ascii=False)
        result = []
        result.append('おまたせ騎士くん、解析結果だよ。\n```総ダメージ ：')
        result.append(damage.replace('"', ''))
        result.append('\n')
        result.append(timeline.replace(',', '\n').replace('"', '').replace('[', '').replace(']', '').replace(' ', ''))
        result.append('```')
        resultStr = ('').join(result)
        return resultStr
    elif statusCode == 424:
        resultMsg = '解析できる動画は10分までなんだ、ごめんね騎士くん。'
        return resultMsg
    else:
        resultMsg = 'ごめんね、解析に失敗しちゃった。時間をおいてからもう一度試すか質問コーナーで聞いてみてね。'
        return resultMsg
