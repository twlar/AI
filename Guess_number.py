#!/usr/bin/env python2
# -*- encoding=utf-8 -*-
import sys
import random
from dueros.Bot import Bot
from dueros.card.TextCard import TextCard

reload(sys)
sys.setdefaultencoding('utf8')

class DuerOSBot(Bot):

    def launch_request(self):
        """
        打开技能
        """
        self.wait_answer()
        card = TextCard('欢迎使用技能')
        return {
            'card': card,
            'outputSpeech': r'欢迎使用数字魔法，游戏开始后，需要在5次内猜中，准备好后，请说开始...'
        }

    def ended_request(self):
        """
        关闭技能
        """
        self.wait_answer()
        return {
            'outputSpeech': r'感谢使用数字魔法'
        }

    def __init__(self, request_data):
        super(DuerOSBot, self).__init__(request_data)
        self.add_launch_handler(self.launch_request)
        self.add_session_ended_handler(self.ended_request)
        self.add_intent_handler('game_guess', self.game_guess_intent)
        self.add_intent_handler('game_start', self.game_start_intent)

    def game_guess_intent(self):
        answer = self.get_slots('answer')
        if not answer:
            self.nlu.ask('answer')
            return {
                'outputSpeech': r'请说出你的答案'
            }

        answer = int(answer)
        goal = int(self.get_session_attribute('goal', 0))
        counter = int(self.get_session_attribute('counter', 0))+1
        if answer == goal:
            return{
                'outputSpeech': r'猜对了，用了{0}次机会，继续游戏，请说重新开始。退出游戏，请说退出'.format(counter)
            }
        else:
            if counter<5:
                self.set_session_attribute('counter', str(counter), 0)
                if answer > goal:
                    hints = r'太大了'
                else:
                    hints = r'猜小了一点'

                self.nlu.ask('answer')
                return{
                    'outputSpeech': r'{0}，还有{1}次机会，接着猜...'.format(hints, 5-counter)
                }
            else:
                self.init_game()
                return {
                    'outputSpeech': r'已经猜错5次了，本轮游戏结束，继续游戏，请说重新开始'
                }

    def game_start_intent(self):

        flag = self.request.get_query();
        if r'开始' == flag or r'重新开始' == flag:
            self.init_game()
            self.nlu.ask('answer')
            return {
                'outputSpeech': r'小度已经准备好了一个0到100的数字，猜猜看是多少？计时开始...',
            }
        else:
            return {
                'outputSpeech': r'继续游戏，请说开始，不想玩了，请说退出',
            }

    def init_game(self):
        goal = random.randint(0, 100)
        self.set_session_attribute('goal', str(goal), str(goal))
        self.set_session_attribute('counter', '0', '0')
        return

def handler(event, context):

    bot = DuerOSBot(event)
    result = bot.run()
    return result
