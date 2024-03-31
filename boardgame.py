'''
Author: Gakki && 739150373@qq.com
Date: 2024-01-15 23:00:08
LastEditors: Gakki
LastEditTime: 2024-03-20 19:26:48
Description: 桌游机器人梨花酱(KOOK版)
联系QQ:739150373
'''

# ================================================================
# =====================此文件为桌游功能的实现======================
# ================================================================


from khl import Bot, Message, Cert, Event,EventTypes
from get_data import *

def init(bot:Bot):

    # 测试功能
    @bot.command(name='hello')
    async def world(msg: Message):
        str = msg.content
        await msg.reply('world!')

    # -----图包查询-----
    @bot.command(regex=r'^(?:图包查询)(.+)')
    async def mod_search(msg: Message, mod_name: str):
        await modsearch(msg,mod_name)

    # 按钮点击事件，如果图包查询按下按钮是传value值的话就用这个发链接到公屏
    # 暂时用的链接，这个就没啥用
    @bot.on_event(EventTypes.MESSAGE_BTN_CLICK)
    async def btn_click_event(b:Bot,e:Event):
        str1 = str(e.body['value'])
        channel = await bot.client.fetch_public_channel(e.body['target_id'])
        await channel.send(str1)