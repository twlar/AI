#!/usr/bin/env python2
# -*- encoding=utf-8 -*-
import sys
import random
from dueros.Bot import Bot
from dueros.card.TextCard import TextCard
from dueros.directive.Display.Hint import Hint

reload(sys)
sys.setdefaultencoding('utf8')

quotations = ['一个人的死，对于这个世界来说不过是多了一座坟墓，但对于相依为命的人来说，却是整个世界都被坟墓掩埋',
            '艾斯：为什么遇到如此强大的敌人你也不愿逃跑？—— 那是因为身后，有至爱之人',
            '索隆：我不管这个世上的人怎么说我，我只想依照我的信念做事，绝不后悔，不管现在将来都一样！',
            '山治：不要随随便便同情失败者，这会伤了他的自尊心',
            '雷利：不知所措，才是人生',
            '索隆：灾难总是接踵而至，这正是世间的常理。你以为只要解释一下，就有谁会来救你吗？要是死了，就只能说明我不过是如此程度的男人',
            '人生充满了起起落落。关键在于，在顶端时好好享受；在低谷时不失勇气',
            '山治：能原谅女人谎言的才是真正的男人',
            '历史虽然会一再重演，但人类却无法回到过去。',
            '路飞：我不是英雄，我只做我想做的事，保护我想要保护的人而已',
            '路飞：你没听过这句伟大的名言么？“肚子饿了就要吃！”',
            '如果一直想着麻烦的事，只会更麻烦',
            '胜利和败北都要品尝、经历过四处逃窜的辛酸、痛苦和悲伤的回忆、这样才能独当一面、就算痛哭流涕也没关系！',
            '按照自己的喜好去做,得不到别人的赞赏也没关系',
            '谁也没有办法把过去发生的事情一笔勾销，要记住教训，勇敢的活下去',
            '艾斯：所有人都知道，自由并不是放纵，那是火一般的梦想',
            '娜美：遇到迷茫时，任何人都会变得软弱。 一旦坚信自己可以帮到别人，他们就会变得很强大',
            '路飞：我不是天生的王者，但我骨子里流动着不让我低头的血液',
            '索隆：人生中有些事你不竭尽所能去做，你永远不知道你自己有多出色',
            '蒂奇：只管把目标定在高峰，人家要笑就让他去笑！',
            '沙克洛克达尔：所谓理想，只是同时拥有实力的人才能说的“现实”。所谓弱就是一种罪',
            '路飞：将过去和羁绊全部丢弃,不要吝惜那为了梦想流下的泪水',
            '罗宾：历史虽然会一再重演，但人类却无法回到过去',
            '索隆：既然已经决定做一件事，那么除了当初决定做这件事的我之外，没人可以叫我傻瓜',
            '布鲁克：让我存活于这世上的力量既不是内脏也不是肌肉，没错，是灵魂',
            '索隆：受尽苦难而不厌，此乃修罗之道',
            '斯摩格：在这片海洋中，若无法向上攀游，就只有往下沉沦，是要前进或是溺死，就得看自己的选择。 既然这么不甘心，就变的更强！']

class DuerOSBot(Bot):

    def launch_request(self):
        """
        打开技能
        """
        self.wait_answer()
        card = TextCard('欢迎来到动漫语录')
        return {
            'card': card,
            'outputSpeech': r'欢迎来到动漫语录'
        }

    def ended_request(self):
        """
        关闭技能
        """
        self.wait_answer()
        return {
            'outputSpeech': r'感谢您的使用动漫语录'
        }

    def __init__(self, request_data):
        super(DuerOSBot, self).__init__(request_data)
        self.add_launch_handler(self.launch_request)
        self.add_session_ended_handler(self.ended_request)
        self.add_intent_handler('ai.dueros.common.next_intent', self.ai_dueros_common_next_intent_intent)

    def ai_dueros_common_next_intent_intent(self):

        index = random.randint(0, len(quotations))
        content = quotations[index]
        card = TextCard(content)

        hint = Hint(['再来一个', '换一个', '换个', '再来一个'])
        return {
            'card': card,
            'directives': [hint],
            'outputSpeech': content
        }

def handler(event, context):

    bot = DuerOSBot(event)
    result = bot.run()
    return result
