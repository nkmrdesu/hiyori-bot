import os
import discord

async def main(client, message):
  # 大人の事情でここでメモを取得
  memo = message.content.replace('/call', '')
  # チェックが入ったメンバー名のリストを作成
  messageList = message.channel.history(limit=30)
  memberList = []
  async for message in messageList:
    reactions = message.reactions
    for reaction in reactions:
      if reaction.emoji == '\N{PUSHPIN}':
        memberList.append(message.author)
  # 呼び出し対象なし
  if len(memberList) == 0:
    await message.channel.send('呼び出し対象が見つからないよ。')
    return
  # 対象ボスを取得、取得失敗時はエラーメッセージ
  targetBoss = os.environ.get(str(message.channel.id))
  if targetBoss is None:
    await message.channel.send('ごめんね、呼び出し中にエラーが起きちゃったみたいだよ。')
    return
  targetBossChannelId = int(os.environ.get(targetBoss))
  # 送信対象のチャンネル
  targetBossChannel = client.get_channel(targetBossChannelId)
  # 呼び出しメッセージ送信
  mentionName = ""
  for member in reversed(memberList):
    mentionName += "<@"
    mentionName += str(member.id)
    mentionName += "> "
  if not memo:
    await targetBossChannel.send(mentionName + '\nもうすぐ凸が始まるみたいだよ。準備をして待っててね。')
  else:
    await targetBossChannel.send(mentionName + '\nもうすぐ凸が始まるみたいだよ。準備をして待っててね。進行さんからのメモも預かっているから確認してね！\n「' + memo + '」')
  return
