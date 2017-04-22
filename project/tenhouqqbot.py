from qqbot import QQBotSlot as qqbotslot, QQBot
from qqbot.qcontactdb import QContact
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
            self.qbot.SendTo(qq_group, '我排好了，你们赶紧的', reSendOn1202=False)
        if 'WAIT_TO_END' in message:
            self.qbot.SendTo(qq_group, '操你们妈啊，喊3缺1叫我，然后又没人来', reSendOn1202=False)
        if 'FINAL_RESULT' in message:
            result_list = re.search(r'FINAL_RESULT\s*(.*)', message).group(1)
            self.qbot.SendTo(qq_group, '刚刚跟你们这群菜鸡打了一局，结果感人', reSendOn1202=False)
            result = re.search(r'\[(.*)\((.*)\) (.*), (.*)\((.*)\) (.*), (.*)\((.*)\) (.*), (.*)\((.*)\) (.*)\]',
                               result_list)
            for i in [1, 4, 7, 10]:
                name = result.group(i)
                point = result.group(i+1)
                score = result.group(i+2)
                if name == 'Lattish':
                    name = '老子我'
                formatted_result = '%s: %s (%s)' % (name, score, point)
                time.sleep(0.3)
                self.qbot.SendTo(qq_group, formatted_result, reSendOn1202=False)
            if result.group(10) == 'Lattish' and float(result.group(12).replace(' ', '')) < 0:
                time.sleep(1)
                self.qbot.SendTo(qq_group, '你们竟然敢打飞我？？？烟了，全都烟了！！！', reSendOn1202=False)
                members = [x for x in self.qbot.List(qq_group) if x.role == '成员']
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

my_names = ["@ME", "Lattish", "yunini", "lattish"]


@qqbotslot
def onQQMessage(bot, contact, member, content):
    global qq_group
    global botConnector
    global is_playing
    if contact.qq == '625219436':
        qq_group = contact
        if '烟' in content or '🚬' in content:
            if member.role == '成员':
                if '烟呢' in content:
                    shut_seconds = random.randint(1, 10) * 60
                    bot.GroupShut(contact, [member], t=shut_seconds)
                    bot.SendTo(contact, '这呢，成全你这个抖 M', reSendOn1202=False)
                else:
                    num = random.random()
                    if num < 0.2:
                        bot.GroupShut(contact, [member], t=60)
                        bot.SendTo(contact, '还真当我不懂啊，智障', reSendOn1202=False)
                    elif num < 0.22:
                        bot.GroupShut(contact, [member], t=3600)
                        bot.SendTo(contact, '今天试试这电子烟怎么样？', reSendOn1202=False)
                    else:
                        bot.SendTo(contact, "烟？什么意思？完全不懂啊", reSendOn1202=False)
            else:
                bot.SendTo(contact, '渣渣管理员别跟我提烟', reSendOn1202=False)
        if '麻吗' in content or "麻？" in content or "棍吗" in content or "棍？" in content:
            num = random.random()
            if num < 0.5:
                bot.SendTo(contact, '搞事搞事搞事', reSendOn1202=False)
            else:
                bot.SendTo(contact, '来啊，来屁胡啊', reSendOn1202=False)
        elif '机器人' in content or 'AI' in content or 'bot' in content:
            bot.SendTo(contact, '操你妈别以为我不知道你在说我', reSendOn1202=False)
        elif 'latish' in content or 'Latish' in content:
            bot.SendTo(contact, '智障能把我名字打对吗？？？', reSendOn1202=False)
        elif any([x in content for x in my_names]):  # being mentioned
            if "在吗" in content or "zaima" in content:
                if not is_playing:
                    num = random.random()
                    if num < 0.5:
                        bot.SendTo(contact, '摸了', reSendOn1202=False)
                    else:
                        bot.SendTo(contact, 'buzai cmn', reSendOn1202=False)
                else:
                    bot.SendTo(contact, '我正堇业着呢，叫也没用')
            elif "缺人" in content:
                if not is_playing:
                    bot.SendTo(contact, '3缺1再叫我，谢谢，你说缺人谁他妈知道你缺几个', reSendOn1202=False)
                else:
                    bot.SendTo(contact, '我正在跟别人干着呢，叫也没用', reSendOn1202=False)
            elif "3缺1" in content or "三缺一" in content:
                if not is_playing:
                    is_playing = True
                    bot.SendTo(contact, '你群打个麻将都贵阳，知道了，这就上线', reSendOn1202=False)
                    tenhou_thread = TenhouThread(botConnector)
                    tenhou_thread.start()
                else:
                    bot.SendTo(contact, '我正在跟别人干着呢，叫也没用', reSendOn1202=False)
            elif "别排" in content:
                if is_playing:
                    bot.SendTo(contact, '你他妈遛我玩呢？下回缺人别JB找我', reSendOn1202=False)
                    botConnector.stop_wait = True
                else:
                    bot.SendTo(contact, '你他妈是不是傻，老子本来也没排啊', reSendOn1202=False)
            elif "地址" in content or "链接" in content:
                bot.SendTo(contact, '不会自己看群公告啊，傻逼', reSendOn1202=False)
                bot.SendTo(contact, '网页版：http://tenhou.net/3/?L2587', reSendOn1202=False)
                bot.SendTo(contact, 'Flash 版：http://tenhou.net/0/?L2587', reSendOn1202=False)
            elif "傻逼" in content or "真蠢" in content:
                bot.SendTo(contact, '信不信我烟你', reSendOn1202=False)
            elif "疯了" in content or "可爱" in content:
                bot.SendTo(contact, '嘻嘻', reSendOn1202=False)
            elif "闭嘴" in content or "好吵" in content:
                bot.SendTo(contact, '哦，那你可以烟我啊', reSendOn1202=False)
            elif "吃" in content:
                bot.SendTo(contact, '不吃', reSendOn1202=False)
            elif "飞了" in content:
                bot.SendTo(contact, '丢人，你退群吧', reSendOn1202=False)
            else:
                num = random.random()
                if num < 0.3:
                    bot.SendTo(contact, '操你妈要求真多', reSendOn1202=False)
                elif num < 0.66:
                    bot.SendTo(contact, '人家不懂，不然先抽烟？', reSendOn1202=False)
                else:
                    bot.SendTo(contact, '哎呀人家不懂了啦', reSendOn1202=False)
        elif random.random() > 0.98:
            bot.SendTo(contact, content, reSendOn1202=False)


if __name__ == '__main__':
    bot = QQBot()
    botConnector = BotConnector(bot)
    bot.Login(user='Lattish')
    bot.Run()
