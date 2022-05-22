import os
import discord

async def main(client, message):
  # 大人の事情でここでいろいろ作っておく
  memo = message.content.replace('/list', '')
  delList = message.channel.history(limit=30)
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
    await message.channel.send('対象が見つからないよ。')
    return
  # 対象ボスを取得、取得失敗時はエラーメッセージ
  targetBoss = os.environ.get(str(message.channel.id))
  if targetBoss is None:
    await message.channel.send('ごめんね、リスト作成中にエラーが起きちゃったみたいだよ。')
    return
  targetBossChannelId = int(os.environ.get(targetBoss))
  # 送信対象のチャンネル
  targetBossChannel = client.get_channel(targetBossChannelId)
  # 呼び出しメッセージ送信
  names = ""
  for member in reversed(memberList):
    names += "●"
    names += str(member.display_name)
    names += "さん\n"
  if not memo:
    await targetBossChannel.send(names)
  else:
    await targetBossChannel.send(memo + '\n\n'+ names)
  # 邪魔なのでコマンドメッセージを消す
  async for delTarget in delList:
    if delTarget.content.startswith('/list'):
      await delTarget.delete()
  return
