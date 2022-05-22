import random
import time

def main(msg):
    # 回線弱者対策
    time.sleep(3)
    # 許可したチャンネルでない場合NGメッセージを返して終了する
    msgCh = msg.channel.id
    channelList = []
    channelList.append(909271387854741534)  # 雑談
    channelList.append(694481950190338114)  # 神社
    channelList.append(806172678347817030)  # 自鯖テスト用
    if msgCh not in channelList:
        return "ごめんね、ここでのおみくじは禁止されちゃったみたいだよ。許可された場所でもう一度試してみてね。"
    
    # おみくじ
    omikuji = ["hime", "dai", "tyu", "kiti", "sue", "kyou", "daikyou", "dai", "tyu", "kiti", "sue"]
    # 抽選
    result = random.choice(omikuji)
    print(result)
    if result == "hime":
        return "やったね、大当たり！姫吉だよー！"
    elif result == "dai":
        return "やったね、大吉だよ！"
    elif result == "tyu":
        return "やったね、中吉だよ"
    elif result == "kiti":
        return "吉だよ！"
    elif result == "sue":
        return "末吉だよー"
    elif result == "kyou":
        return "ごめんね、凶だよ"
    elif result == "daikyou":
        return "あわわ、大凶だよ。今日はおとなしくしてたほうがいいかも・・・"
