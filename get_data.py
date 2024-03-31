'''
Author: Gakki && 739150373@qq.com
Date: 2024-03-17 19:16:10
LastEditors: Gakki
LastEditTime: 2024-03-20 19:28:08
Description: 桌游机器人梨花酱(KOOK版)
联系QQ:739150373
'''

# ================================================================
# ===================此文件为数据读取功能的实现=====================
# ================================================================


from khl.card import Card, CardMessage, Module, Types, Element, Struct
from khl import Bot, Message, Cert, Event,EventTypes
from pathlib import Path
import os
import sqlite3

# ====================================所有的非异步函数=================================
#查询图包信息，返回参数为图包所有属性
def get_modname(mod_name):
    data = []
    msg_list = []
    # 连接数据库
    conn = sqlite3.connect(
       Path(os.path.join(os.path.dirname(__file__), "data"))/"zhuoyou.db")
    # 创建游标
    #conn = sqlite3.connect(r'D:\Github\LihuaBot\nb2\LihuaBot\src\plugins\nonebot_plugin_zhuoyouchaxun\resource\zhuoyou.db')
    cur = conn.cursor()
    # 通过cur.execute执行sql语句，操作数据库
    '''cursor = cur.execute(
        f"SELECT tubao_id,tubao_name, file_name ,display from tubao WHERE ((tubao_name like '%{mod_name}%' or file_name like '%{mod_name}%') and display like 'True') "
    )'''

    cursor = cur.execute(
        f"SELECT * from tubao WHERE ((tubao_name like '%{mod_name}%' or file_name like '%{mod_name}%') and display like 'True') "
    )
    # 得到查询结果
    db_data = cur.fetchall()

    # 断开数据库连接
    conn.close()

    try:
        if db_data == []:
            data.append(False)
            data.append(f"图书馆里中没有搜到关于《{mod_name}》的信息啦~请告诉梨花其他的名字或英文~")
            return data
        else:
            data.append(True)
            for i in range(len(db_data)):
                msg_list = []
                msg_list.append(str(db_data[i][2]))
                msg_list.append(str(db_data[i][3]))
                data.append(msg_list)
            return data
    except:
        return [False,f"查询失败啦！是不是命令记得不清楚呀？发送“梨花命令”这四个字查看所有命令哦~"]



# ====================================所有的异步函数===================================
# 图包查询的实施函数
async def modsearch(msg: Message, mod_name: str):
    # 把mod_name里左边那个空格删除，然后得到图包的所有属性
    # 开黑啦的消息感觉不需要图包id这个属性，但是为了保留nonebot2的东西还是使用这个函数名
    mod_name = mod_name.strip()
    mod_idname = get_modname(mod_name)
    
    # await msg.reply(f"{mod_idname}")

    # 初始化一个卡片消息
    # 一个卡片消息可以发5个卡片，每个卡片最多50个模块
    cm = CardMessage()

    # 尝试发送
    try:
        # 进行图包信息的判定
        # 如果没有值就直接说没查到
        if mod_idname[0] == False:
            await msg.reply(mod_idname[1])
        else:
            c2 = Card()
            for i in range (len(mod_idname)-1):
                c2.append(Module.Section(
                    Element.Text(str(mod_idname[i+1][0]), type=Types.Text.KMD),
                    Element.Button("链接",value=str(mod_idname[i+1][1]),click=Types.Click.RETURN_VAL,theme=Types.Theme.SUCCESS,),)
                )
            cm.append(c2)
            await msg.reply(cm)
    except:
        await msg.reply('不听不听，图包查询失败啦！')