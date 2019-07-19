#!/usr/bin/env python2
# -*- encoding=utf-8 -*-
import sys
import random
import json
from dueros.Bot import Bot
from dueros.card.TextCard import TextCard

reload(sys)
sys.setdefaultencoding('utf8')

#动物列表
ANIMALS = (
    {'name': '老虎', 'features': '最凶猛的哺乳动物是什么'},
    {'name': '鰕虎鱼', 'features': '世界上最小的鱼是什么鱼'},
    {'name': '鸵鸟', 'features': '世界上最大的鸟是什么鸟'},
    {'name': '猎豹', 'features': '世界上短跑最快的动物是什么'},
    {'name': '竹节虫', 'features': '世界上最长的小虫虫是什么'},
    {'name': '大象', 'features': '陆地上最重的动物是什么'},
    {'name': '长颈鹿', 'features': '陆地上最高的动物是什么'},
    {'name': '旗鱼', 'features': '游泳最快的鱼是什么鱼'},
    {'name': '猩猩', 'features': '你知道世界上最聪明的动物是什么'},
    {'name': '雨燕', 'features': '飞得最快的鸟'},
    {'name': '企鹅', 'features': '游水最快的鸟'},
    {'name': '天鹅', 'features': '世界上飞得最高的鸟是什么鸟'},
    {'name': '海蛇', 'features': '毒性最强的蛇是什么蛇'},
    {'name': '北极熊', 'features': '皮毛最保暖的动物'},
    {'name': '海龟', 'features': '世界上寿命最长的动物'},
    {'name': '河马', 'features': '嘴巴最大的动物'},
    {'name': '牦牛', 'features': '生活在最高处的哺乳动物'},
    {'name': '白蚁', 'features': '最会造房子的小动物是什么'},
    {'name': '海马', 'features': '大海里面长相最奇特的生物是什么'},
    {'name': '浣熊', 'features': '最爱干净的小动物是什么'},
    {'name': '树懒', 'features': '最懒的动物'},
    {'name': '眼镜猴', 'features': '眼睛最大的动物'},
    {'name': '蟒蛇', 'features': '体型最大的蛇是什么蛇'},
    {'name': '信天翁', 'features': '翅膀最长的鸟是什么鸟'},
    {'name': '企鹅', 'features': '最能忍耐寒冷的鸟是什么鸟'},
    {'name': '蜗牛', 'features': '牙齿最多的动物是什么'},
    {'name': '蝗虫', 'features': '飞行能力最强的虫'},
    {'name': '蜻蜓', 'features': '眼睛最多的昆虫'},
    {'name': '飞鱼', 'features': '能够飞行并且非得最远的鱼'},
    {'name': '电鳗', 'features': '能够放电并且放电能力最强的鱼'},
    {'name': '变色龙', 'features': '能够变色的蜥蜴是什么'},
    {'name': '睡鼠', 'features': '冬眠时间最长的动物是什么'},
    {'name': '水熊', 'features': '生命力最强的动物是什么'},
)
#每次游戏题目个数
GAME_LENGTH = 5

class DuerOSBot(Bot):

    def launch_request(self):
        """
        打开技能
        """
        self.wait_answer()

        text = r'小朋友，欢迎来到动物之最。我说最什么的动物，你来猜。准备好了吗？请说开始'
        card = TextCard(text)
        return {
            'card': card,
            'outputSpeech': text
        }

    def ended_request(self):
        """
        关闭技能
        """
        self.wait_answer()
        return {
            'outputSpeech': r'<speak>谢谢使用动物之最，现在退出，欢迎下次使用</speak>'
        }

    def __init__(self, request_data):
        super(DuerOSBot, self).__init__(request_data)
        self.add_launch_handler(self.launch_request)
        self.add_session_ended_handler(self.ended_request)
        self.add_intent_handler('game_answer', self.game_answer_intent)
        self.add_intent_handler('game_start', self.game_start_intent)

    def game_answer_intent(self):
        answer = self.get_slots('answer')
        if not answer:
            self.nlu.ask('answer')
            return {
                'outputSpeech': r'请说出你的答案'
            }

        answer = json.loads(answer)
        answer = answer['origin']
        answer_correct = self.get_session_attribute('answer', '')
        if not answer_correct:
            return {
                'outputSpeech': r'要说开始后，才可以开始答题哦'
            }

        counter = int(self.get_session_attribute('counter', 0))
        if counter < GAME_LENGTH:
            self.nlu.ask('answer')
            hint_msg = self.populate_game_question()
        else:
            hint_msg = r'本轮游戏结束，重新开始游戏，请说重新开始'

        score = int(self.get_session_attribute('score', 0))
        if answer_correct.strip() == answer.strip():
            score += 1
            self.set_session_attribute('score', score, 0)
            return {
                'outputSpeech': r'回答正确，加1分，当前得分为{0}，{1}'.format(score, hint_msg)
            }
        else:
            return {
                'outputSpeech': r'回答错误，当前得分为{0}，{1}'.format(score, hint_msg)
            }

    def game_start_intent(self):
        self.nlu.ask('answer')
        self.int_game()
        self.set_session_attribute('score', '0', '0')

        question = self.populate_game_question()
        card = TextCard(question)
        return {
            'card': card,
            'outputSpeech': question
        }

    def int_game(self):
        game_questions = []
        index_list = range(len(ANIMALS))
        i = 0
        while i < GAME_LENGTH:
            index = random.randint(0, len(index_list) - 1)
            game_questions.append(index_list[index])
            del (index_list[index])
            i += 1

        return game_questions

    def populate_game_question(self):
        game_questions = self.get_session_attribute('questions', '')
        if not game_questions:
            game_questions = self.int_game()
        else:
            game_questions = game_questions.split(',')

        counter = int(self.get_session_attribute('counter', 0)) + 1

        index = random.randint(0, len(game_questions) - 1)
        question = ANIMALS[int(game_questions[index])]
        del (game_questions[index])
        self.set_session_attribute('questions', ','.join([str(i) for i in game_questions]), '')
        self.set_session_attribute('counter', str(counter), '1')
        self.set_session_attribute('answer', question['name'], '')

        return r'第{0}题，{1}'.format(counter, question['features'])


def handler(event, context):

    bot = DuerOSBot(event)
    result = bot.run()
    return result
