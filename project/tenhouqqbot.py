from qqbot import QQBotSlot as qqbotslot, QQBot
from tenhoubot import main as starttenhou
import threading
import re
import random
import time
is_playing = False
qq_group = None

class BotConnector(object):

    def __init__(self, qqbot):
        self.qbot = qqbot
        self.stop_wait = False
        self.first_time = True

    def on_receive_message(self, message):
        if 'WAIT_READY' in message:
            self.qbot.SendTo(qq_group, '我排好了，你们赶紧的')
        if 'WAIT_TO_END' in message:
            self.qbot.SendTo(qq_group, '操你们妈啊，喊3缺1叫我，然后又没人来')
        if 'FINAL_RESULT' in message:
            result_list = re.search(r'FINAL_RESULT\s*(.*)', message).group(1)
            self.qbot.SendTo(qq_group, '刚刚跟你们这群菜鸡打了一局，结果感人')
            result = re.search(r'\[(.*)\((.*)\) (.*), (.*)\((.*)\) (.*), (.*)\((.*)\) (.*), (.*)\((.*)\) (.*)\]', result_list)
            for i in [1, 4, 7, 10]:
                name = result.group(i)
                point = result.group(i+1)
                score = result.group(i+2)
                if name == 'Lattish':
                    name = '老子我'
                formatted_result = '%s: %s (%s)' % (name, score, point)
                time.sleep(0.3)
                self.qbot.SendTo(qq_group, formatted_result)
            if result.group(10) == 'Lattish' and float(result.group(12).replace(' ', '')) < 0:
                time.sleep(1)
                self.qbot.SendTo(qq_group, '你们竟然敢打飞我？？？烟了，全都烟了！！！')
                members = [x for x in self.qbot.List(qq_group) if x.role == '普通成员']
                self.qbot.GroupShut(qq_group, members, t=60)


class TenhouThread (threading.Thread):
    def __init__(self, connector):
        threading.Thread.__init__(self)
        self.connector = connector

    def run(self):
        global is_playing
        starttenhou(self.connector)
        is_playing = False
        botConnector.stop_wait = False

@qqbotslot
def onQQMessage(bot, contact, member, content):
    global qq_group
    global botConnector
    global is_playing
    if contact.qq == '625219436':
        qq_group = contact
        if "Lattish" in content or "@ME" in content or "yunini" in content or 'lattish' in content:
            if "在吗" in content or "zaima" in content:
                bot.SendTo(contact,'buzai cmn')
            elif "缺人" in content:
                if not is_playing:
                    bot.SendTo(contact, '3缺1再叫我，谢谢，你说缺人谁他妈知道你缺几个')
                else:
                    bot.SendTo(contact, '我正在跟别人干着呢，叫也没用')
            elif "3缺1" in content or "三缺一" in content:
                if not is_playing:
                    is_playing = True
                    bot.SendTo(contact, '你群打个麻将都贵阳，知道了，这就上线')
                    tenhou_thread = TenhouThread(botConnector)
                    tenhou_thread.start()
                else:
                    bot.SendTo(contact, '我正在跟别人干着呢，叫也没用')
            elif "别排" in content:
                if is_playing:
                    bot.SendTo(contact, '你他妈遛我玩呢？下回缺人别JB找我')
                    botConnector.stop_wait = True
                else:
                    bot.SendTo(contact, '你他妈是不是傻，老子本来也没排啊')
            elif "地址" in content or "链接" in content:
                bot.SendTo(contact, '不会自己看群公告啊，傻逼')
                bot.SendTo(contact, '网页版：http://tenhou.net/3/?L2587')
                bot.SendTo(contact, 'Flash 版：http://tenhou.net/0/?L2587')
            else:
                if random.random() > 0.5:
                    bot.SendTo(contact, '操你妈要求真多')
                else:
                    bot.SendTo(contact, '哎呀人家不懂了啦')
        elif random.random() > 0.98:
            bot.SendTo(contact, content)

        if '烟' in content or '🚬' in content:
            if random.random() < 0.3:
                if member.role == '普通成员':
                    bot.GroupShut(qq_group, [member], t=60)
                    bot.SendTo(qq_group, '还真当我不懂啊，智障')
            elif random.random() < 0.35:
                if member.role == '普通成员':
                    bot.GroupShut(qq_group, [member], t=3600)
                    bot.SendTo(qq_group, '还真当我不懂啊，智障')
            else:
                bot.SendTo(qq_group, "烟？什么意思？完全不懂啊")
if __name__ == '__main__':
    bot = QQBot()
    botConnector = BotConnector(bot)
    bot.Login(qq='2913658983')
    bot.Run()
