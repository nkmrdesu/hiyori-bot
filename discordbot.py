from discord.ext import commands
from discord.ext import tasks
from datetime import datetime
from typing import Union
from discord_buttons_plugin import *
import requests
import os
import traceback
import discord
import videoAnalyze
import omikuji
import CalcCarryOverTime
import FuncList
import SendPreparationMessage
import SendStartMessage
import SendListMessage

# 接続に必要なオブジェクトを生成
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
token = os.environ['DISCORD_BOT_TOKEN']
# 環境変数を変更することで起動チャンネルを変更（Windmuleの場合雑談でOK？）
zatu_channel_id = int(os.environ['TEST_CHANNEL'])
guild_id = int(os.environ['GUILD_ID'])
role_id = int(os.environ['ROLE_ID'])
analyze_channel_category = int(os.environ['ANALYZE_CHANNEL_CATEGORY'])
# emojiたち
emoji_one = '\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}'
emoji_two = '\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}'
emoji_three = '\N{DIGIT THREE}\N{COMBINING ENCLOSING KEYCAP}'
emoji_four = '\N{DIGIT FOUR}\N{COMBINING ENCLOSING KEYCAP}'
emoji_five = '\N{DIGIT FIVE}\N{COMBINING ENCLOSING KEYCAP}'
emoji_six = '\N{DIGIT SIX}\N{COMBINING ENCLOSING KEYCAP}'
emoji_seven = '\N{DIGIT SEVEN}\N{COMBINING ENCLOSING KEYCAP}'
emoji_eight = '\N{DIGIT EIGHT}\N{COMBINING ENCLOSING KEYCAP}'
emoji_star = '\N{WHITE MEDIUM STAR}'


# 起動時の処理
@client.event
async def on_ready():
    channel = client.get_channel(zatu_channel_id)
    # テスト時に起動確認するためだけのメッセージ1
#     await channel.send('やっほー騎士くん！ヒヨリぼっとが再起動したよ。')
    guild = client.get_guild(guild_id)
#     await client.change_presence(activity=discord.Game("ウマ娘プリティーダービー"))
    await client.change_presence(activity=discord.Game("クラバト本戦"))
    #ループで永続起動させる
    loop.start()

# 現在の凸状況を算出して雑談に投稿する
async def countAttack():
    guild = client.get_guild(guild_id)
    target_channel = discord.utils.get(guild.text_channels, name='凸報告（ヒヨリぼっと）')
    if target_channel is None:
        await client.get_channel(zatu_channel_id).send('報告用チャンネルが見つからないよ。')
        return
    # カウント対象メッセージの取得
    async for msg in target_channel.history():
        if msg.content.startswith('おはよう騎士くん。今日の凸報告はここだよ'):
            # 指定のロールを持つBot以外のリストを作成
            guildMemberList = client.get_guild(guild_id).members
            clanMember = []
            for guildMember in guildMemberList:
                    if guildMember.bot == bool(False):
                        for role in guildMember.roles:
                            if role.id == role_id:
                                clanMember.append(guildMember)

            # リアクションごとのリストを作成
            reactionList = msg.reactions
            reactionOneList = []
            reactionTwoList = []
            reactionThreeList = []
            reactionFourList = []
            reactionFiveList = []
            reactionSixList = []
            reactionSevenList = []
            reactionEightList = []
            reactionStarList = []
            # 持ち越し除いた総凸数
            resultCnt = 0
            for reaction in reactionList:
                strList = list(reaction.emoji)
                codeList =[]
                for st in strList:
                    codeList.append((hex(ord(st))))
                strEmoji = ''.join(codeList)
                if strEmoji in '0x2b50':
                    async for reactionUser in reaction.users():
                        reactionStarList.append(reactionUser)
                if strEmoji in '0x380x20e3':
                    async for reactionUser in reaction.users():
                        reactionEightList.append(reactionUser)
                if strEmoji in '0x370x20e3':
                    async for reactionUser in reaction.users():
                        reactionSevenList.append(reactionUser)
                if strEmoji in '0x360x20e3':
                    async for reactionUser in reaction.users():
                        reactionSixList.append(reactionUser)
                if strEmoji in '0x350x20e3':
                    async for reactionUser in reaction.users():
                        reactionFiveList.append(reactionUser)
                if strEmoji in '0x340x20e3':
                    async for reactionUser in reaction.users():
                        reactionFourList.append(reactionUser)   
                if strEmoji in '0x330x20e3':
                    async for reactionUser in reaction.users():
                        reactionThreeList.append(reactionUser)
                if strEmoji in '0x320x20e3':
                    async for reactionUser in reaction.users():
                        reactionTwoList.append(reactionUser)
                if strEmoji in '0x310x20e3':
                    async for reactionUser in reaction.users():
                        reactionOneList.append(reactionUser)
                        
            # 星を押しているユーザーは完凸としてメンバーリストから取り除く
            for reactionStarUser in reactionStarList:
                if reactionStarUser in clanMember:
                    resultCnt += 3
                    clanMember.remove(reactionStarUser)
            
            # 結果出力用リスト
            oneMember = []
            twoMember = []
            threeMember = []
            fourMember = []
            fiveMember = []
            sixMember = []
            sevenMember = []
            eightMember = []
                        
            for reactionEightUser in reactionEightList:
                # 残り持ち越しのメンバーリストの作成
                if reactionEightUser in clanMember:
                    resultCnt += 3
                    eightMember.append(reactionEightUser)
                    clanMember.remove(reactionEightUser)
            for reactionSevenUser in reactionSevenList:
                # 残り持ち越し＋持ち越しのメンバーリストの作成
                if reactionSevenUser in clanMember:
                    resultCnt += 3
                    sevenMember.append(reactionSevenUser)
                    clanMember.remove(reactionSevenUser)
            for reactionSixUser in reactionSixList:
                # 残り持ち越し＋持ち越し＋持ち越しのメンバーリストの作成
                if reactionSixUser in clanMember:
                    resultCnt += 3
                    sixMember.append(reactionSixUser)
                    clanMember.remove(reactionSixUser)
            for reactionFiveUser in reactionFiveList:
                # 残り１凸のメンバーリストの作成
                if reactionFiveUser in clanMember:
                    resultCnt += 2
                    fiveMember.append(reactionFiveUser)
                    clanMember.remove(reactionFiveUser)
            for reactionFourUser in reactionFourList:
                # 残り１凸＋持ち越しのメンバーリストの作成
                if reactionFourUser in clanMember:
                    resultCnt += 2
                    fourMember.append(reactionFourUser)
                    clanMember.remove(reactionFourUser)
            for reactionThreeUser in reactionThreeList:
                # 残り１凸＋持ち越し＋持ち越しのメンバーリストの作成
                if reactionThreeUser in clanMember:
                    resultCnt += 2
                    threeMember.append(reactionThreeUser)
                    clanMember.remove(reactionThreeUser)
            for reactionTwoUser in reactionTwoList:
                # 残り２凸のメンバーリストの作成
                if reactionTwoUser in clanMember:
                    resultCnt += 1
                    twoMember.append(reactionTwoUser)
                    clanMember.remove(reactionTwoUser)
            for reactionOneUser in reactionOneList:
                # 残り２凸＋持ち越しのメンバーリストの作成
                if reactionOneUser in clanMember:
                    resultCnt += 1
                    oneMember.append(reactionOneUser)
                    clanMember.remove(reactionOneUser)
                
            # 結果メッセージの送信
            result =['今日の残凸状況だよ。名前のない人は３凸済だよ、おつかれさま！\n```【残り３凸】\n']
            for mem in clanMember:
                result.append(mem.display_name)
                result.append('さん\n')
            result.append('\n')
            result.append('【残り２凸＋持ち越し】\n')
            for mem in oneMember:
                result.append(mem.display_name)
                result.append('さん\n')
            result.append('\n')
            result.append('【残り２凸】\n')
            for mem in twoMember:
                result.append(mem.display_name)
                result.append('さん\n')
            result.append('\n')
            result.append('【残り１凸＋持ち越し＋持ち越し】\n')
            for mem in threeMember:
                result.append(mem.display_name)
                result.append('さん\n')
            result.append('\n')
            result.append('【残り１凸＋持ち越し】\n')
            for mem in fourMember:
                result.append(mem.display_name)
                result.append('さん\n')
            result.append('\n')
            result.append('【残り１凸】\n')
            for mem in fiveMember:
                result.append(mem.display_name)
                result.append('さん\n')
            result.append('\n')
            result.append('【残り持ち越し＋持ち越し＋持ち越し】\n')
            for mem in sixMember:
                result.append(mem.display_name)
                result.append('さん\n')
            result.append('\n')
            result.append('【残り持ち越し＋持ち越し】\n')
            for mem in sevenMember:
                result.append(mem.display_name)
                result.append('さん\n')
            result.append('\n')
            result.append('【残り持ち越し】\n')
            for mem in eightMember:
                result.append(mem.display_name)
                result.append('さん\n')
            result.append('```')
            result.append('\n\n持ち越し除いて ' + str(resultCnt) + ' 凸完了')
            resultStr = ('').join(result)
            channel = client.get_channel(zatu_channel_id)
            await channel.send(resultStr)
            # 問題なくカウントできたらループ終了(一番最新のメッセージ対象の為基本１回でループ終了)
            break
    
# 60秒に一回ループ
@tasks.loop(seconds=60)
async def loop():
    guild = client.get_guild(guild_id)
    # ５時に報告用メッセージを送信
    target_msg = ''
#     if datetime.now().strftime('%H%M') == '2030':
    if datetime.now().strftime('%H%M') == '0500':
#     if datetime.now().strftime('%H%M') == '9999':
#     if datetime.now().strftime('%H%M') == '1200':
        target_channel = discord.utils.get(guild.text_channels, name='凸報告（ヒヨリぼっと）')
        if target_channel is None:
            await client.get_channel(zatu_channel_id).send('報告用チャンネルが見つからないよ。')
        else:
            target_msg = await target_channel.send('おはよう騎士くん。今日の凸報告はここだよ。\n凸状況に合わせてスタンプを押してね！\n:one:　⇒　残り２凸＋持ち越し\n:two:　⇒　残り２凸\n:three:　⇒　残り１凸＋持ち越し＋持ち越し\n:four:　⇒　残り１凸＋持ち越し\n:five:　⇒　残り１凸\n:six:　⇒　残り持ち越し＋持ち越し＋持ち越し\n:seven:　⇒　残り持ち越し＋持ち越し\n:eight:　⇒　残り持ち越し\n:star:　⇒　３凸完了')
            await target_msg.add_reaction(emoji_one)
            await target_msg.add_reaction(emoji_two)
            await target_msg.add_reaction(emoji_three)
            await target_msg.add_reaction(emoji_four)
            await target_msg.add_reaction(emoji_five)
            await target_msg.add_reaction(emoji_six)
            await target_msg.add_reaction(emoji_seven)
            await target_msg.add_reaction(emoji_eight)
            await target_msg.add_reaction(emoji_star)
#     if datetime.now().strftime('%H%M') == '0000':
#         await client.get_channel(zatu_channel_id).send('クランバトル終了だよー。騎士くん、今年も一年間お疲れ様！')


    
        
# 発言したチャンネルのカテゴリ内にチャンネルを作成する
async def create_channel(message, channel_name):
    category_id = message.channel.category_id
    category = message.guild.get_channel(category_id)
    new_channel = await category.create_text_channel(name=channel_name)
    return new_channel

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 報告・確認用チャンネルを作成する
    if message.content == '/botsetup':
        # 既に同名のチャンネルがあるときは作成しないで警告メッセージを飛ばす
        guild_id = message.guild.id
        guild = client.get_guild(guild_id)
        kizon_channel =  discord.utils.get(guild.text_channels, name='凸報告（ヒヨリぼっと）')
        if kizon_channel is None:
            new_channel = await create_channel(message, channel_name='凸報告（ヒヨリぼっと）')
            await message.channel.send('凸報告用チャンネルを作成したよ。')
        else:
            await message.channel.send('凸報告用チャンネルがもうあるみたいだよ。削除してからもう一回試してね。')
    # ついているリアクションから現在の凸状況を算出する
    if message.content == '/count':
        await message.channel.send('残凸数を数えてみるね。')
        await countAttack()
    # 使用できるコマンド一覧
    if message.content == 'ヒヨリママ':
        await message.channel.send('はーいママですよーよちよち')
    if message.content == '困ったときは':
        await message.channel.send('お互いさまさま！')
    if message.content == '/reboot':
        guild_id = int(os.environ['GUILD_ID'])
        guild = client.get_guild(guild_id)
        target_channel = discord.utils.get(guild.text_channels, name='凸報告（ヒヨリぼっと）')
        if target_channel is None:
            await client.get_channel(zatu_channel_id).send('報告用チャンネルが見つからないよ。')
        else:
            target_msg = await target_channel.send('おはよう騎士くん。今日の凸報告はここだよ。\n凸状況に合わせてスタンプを押してね！\n:one:　⇒　残り２凸＋持ち越し\n:two:　⇒　残り２凸\n:three:　⇒　残り１凸＋持ち越し＋持ち越し\n:four:　⇒　残り１凸＋持ち越し\n:five:　⇒　残り１凸\n:six:　⇒　残り持ち越し＋持ち越し＋持ち越し\n:seven:　⇒　残り持ち越し＋持ち越し\n:eight:　⇒　残り持ち越し\n:star:　⇒　３凸完了')
            await target_msg.add_reaction(emoji_one)
            await target_msg.add_reaction(emoji_two)
            await target_msg.add_reaction(emoji_three)
            await target_msg.add_reaction(emoji_four)
            await target_msg.add_reaction(emoji_five)
            await target_msg.add_reaction(emoji_six)
            await target_msg.add_reaction(emoji_seven)
            await target_msg.add_reaction(emoji_eight)
            await target_msg.add_reaction(emoji_star)
    if message.content.startswith('https'):
        if message.channel.category_id == analyze_channel_category:
            await message.channel.send('TLを解析してみるね。')
            analyzeResult = videoAnalyze.main(message.content)
            await message.channel.send(analyzeResult)
    if message.content == "おみくじ":
        omikujiResult = omikuji.main(message)
        await message.channel.send(omikujiResult)
    if message.content.startswith('/time'):
        calcResult = CalcCarryOverTime.main(message.content)
        await message.channel.send(calcResult)
    if message.content == '/funclist':
        func = FuncList.main(message.content)
        await message.channel.send(func)
    if message.content.startswith('/call'):
        await SendPreparationMessage.main(client, message)
    if message.content.startswith('/start'):
        await SendStartMessage.main(client, message)
    if message.content.startswith('/list'):
        await SendListMessage.main(client, message)
            
#     if message.content.startswith('/test'):
#         t = await message.channel.send('tesutodayo.:star: ')
#         ms = message.content.replace('/test', '')
#         for m in ms:
#             print(hex(ord(m)))
#         await t.add_reaction(emoji_star)

#botの起動
client.run(token)
