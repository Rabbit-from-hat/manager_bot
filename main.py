import os
import traceback

import discord
from discord.ext import commands

from modules.grouping import MakeTeam

token = os.environ['DISCORD_BOT_TOKEN']
bot = commands.Bot(command_prefix='/')

"""起動処理"""
@bot.event
async def on_ready():
    print('-----Logged in info-----')
    print(bot.user.name)
    print(bot.user.id)
    print(discord.__version__)
    print('------------------------')

"""メンバー参加退出処理"""
# 参加時
@bot.event
async def on_member_join(member):
    # ロビーチャンネルへ送付
    CHANNEL_ID = 448692957848141824
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(str(member.mention)+'\n'
                       +str(member.display_name)+'さん！当サーバにようこそ！\n'
                       +'以下の対応をお願いします。\n'
                       +'【対応内容】\n'
                       +'・「id置き場」に適宜idの記載\n'
                       +'・「サーバのルール」の一読\n'
                       +'【注意点】\n'
                       +'当サーバの通知は、どのチャンネルも全通知となっております。\n'
                       +'お手数ですが、非通知の設定は適宜お願いいたします。')
    
    # 管理者用チャンネルへメッセージ送付
    REPORT_CANNEL_ID = 673165147891695616
    channel = bot.get_channel(REPORT_CANNEL_ID)
    await channel.send(str(member.display_name)+'さんが、サーバに入室しました。')

    # ロール付与
    role = discord.utils.get(member.guild.roles, name="部員")
    await member.add_roles(role)

# 退出時
@bot.event
async def on_member_remove(member):
    # 管理者用チャンネルへメッセージ送付
    REPORT_CANNEL_ID = 673165147891695616
    channel = bot.get_channel(REPORT_CANNEL_ID)
    await channel.send(str(member.display_name)+'さんが、サーバから退出しました。')

"""VC参加メンバー全員宛てのメンション作成"""
# ちょっとした不具合があるため、使用を停止
# 理由 => https://rabbitfromhat.qrunch.io/entries/uxQNABJJQr4wXTNI
#@bot.event
#async def on_voice_state_update(member, before, after):
#    if not before.channel and after.channel:
#        set_mention_name = after.channel.name
#        role = discord.utils.get(member.guild.roles, name=set_mention_name)
#        await member.add_roles(role)
#    elif before.channel and not after.channel:
#        remove_mention_name = before.channel.name
#        role = discord.utils.get(member.guild.roles, name=remove_mention_name)
#        await member.remove_roles(role)

"""コマンド実行"""
# メンバー数が均等になるチーム分け(未指定時、デフォルトで2)
@bot.command()
async def team(ctx, specified_num=2):
    make_team = MakeTeam()
    remainder_flag = 'true'
    msg = make_team.make_party_num(ctx,specified_num,remainder_flag)
    await ctx.channel.send(msg)

# メンバー数が均等にはならないチーム分け(未指定時、デフォルトで2)
@bot.command()
async def team_norem(ctx, specified_num=2):
    make_team = MakeTeam()
    msg = make_team.make_party_num(ctx,specified_num)
    await ctx.channel.send(msg)

# メンバー数を指定してチーム分け(未指定時、デフォルトで1)
@bot.command()
async def group(ctx, specified_num=1):
    make_team = MakeTeam()
    msg = make_team.make_specified_len(ctx,specified_num)
    await ctx.channel.send(msg)

"""botの接続と起動"""
bot.run(token)