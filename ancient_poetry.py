#!/usr/bin/env python2
# -*- encoding=utf-8 -*-
import sys
import random
from dueros.Bot import Bot
from dueros.card.TextCard import TextCard

reload(sys)
sys.setdefaultencoding('utf8')

#问题列表
QUESTIONS=[
    {'content': '远上还山石径斜，白云深处有人家', 'title': '山行', 'options': ['杜牧', '杜甫', '白居易', '李白', ]},
    {'content': '离离原上草，一岁一枯荣', 'title': '草/赋得古原草送别', 'options': ['白居易', '杜甫', '韩俞', '李白', ]},
    {'content': '举头望明月，低头思故乡', 'title': '静夜思', 'options': ['李白', '杜甫', '白居易', '秦观', ]},
    {'content': '锄禾日当午 汗滴禾下土', 'title': '闵农', 'options': ['李绅', '杜甫', '白居易', '李白', ]},
    {'content': '白日依山尽，黄河入海流', 'title': '登鹳雀楼', 'options': ['王之焕', '杜甫', '白居易', '李白', ]},
    {'content': '李白乘舟将欲行，忽闻岸上踏歌声', 'title': '赠汪伦', 'options': ['王伦', '杜甫', '白居易', '李白', ]},
    {'content': '横看成岭侧成峰，远近高低各不同', 'title': '题西林壁', 'options': ['苏轼', '杜甫', '白居易', '李白', ]},
    {'content': '人生自古谁无死，留取丹心照汗青', 'title': '过零丁洋', 'options': ['文天祥', '杜甫', '白居易', '李白', ]},
]
#定义一轮问答中的问题数量
GAME_LENGTH = 5
#定义每个问题的答案数量
ANSWER_COUNT = 4

class DuerOSBot(Bot):

    def launch_request(self):
        """
        打开技能
        """
        self.wait_answer()
        welcome = r'欢迎来到古诗问答。我将念两句古诗并给你四个诗人的名字。需要你告诉我哪一个是正确的作者。'
        card = TextCard(welcome)
        return {
            'card': card,
            'outputSpeech': welcome + r'是否现在开始答题？'
        }

    def ended_request(self):
        """
        关闭技能
        """
        self.wait_answer()
        return {
            'outputSpeech': r'感谢您的使用'
        }

    def __init__(self, request_data):
        super(DuerOSBot, self).__init__(request_data)
        self.add_launch_handler(self.launch_request)
        self.add_session_ended_handler(self.ended_request)
        self.add_intent_handler('answer_intent', self.answer_intent_intent)
        self.add_intent_handler('newGame_intent', self.new_game_intent_intent)

    def answer_intent_intent(self):
        answer = self.get_slots('theAnswer')
        if not answer:
            self.nlu.ask('theAnswer')
            return {
                'outputSpeech': r'请说出你的答案'
            }

        answer = int(answer)
        answer_correct = self.get_session_attribute('position', 1)
        if not answer_correct:
            return {
                'outputSpeech': r'要说开始后，才可以开始答题'
            }

        counter = int(self.get_session_attribute('counter', 0))
        if counter < GAME_LENGTH:
            self.nlu.ask('theAnswer')
            hint_msg = self.populate_game_question()
        else:
            hint_msg = r'本轮游戏结束，重新开始游戏，请说重新开始'
            
        answer_correct = int(answer_correct)
        score = int(self.get_session_attribute('score', 0))
        if answer_correct == answer:
            score += 1
            self.set_session_attribute('score', score, 0)
            return {
                'outputSpeech': r'回答正确，加1分，当前得分为{0}，{1}'.format(score, hint_msg)
            }
        else:
            return {
                'outputSpeech': r'回答错误，当前得分为{0}，{1}'.format(score, hint_msg)
            }

    def new_game_intent_intent(self):

        self.nlu.ask('theAnswer')
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
        index_list = range(len(QUESTIONS))
        i = 0
        while i < GAME_LENGTH:
            index = random.randint(0, len(index_list)-1)
            game_questions.append(index_list[index])
            del(index_list[index])
            i += 1

        return game_questions

    def populate_game_question(self):
        game_questions = self.get_session_attribute('questions', '')
        if not game_questions:
            game_questions = self.int_game()
        else:
            game_questions = game_questions.split(',')

        counter = int(self.get_session_attribute('counter', 0))+1

        index = random.randint(0, len(game_questions)-1)
        question = QUESTIONS[int(game_questions[index])]
        del(game_questions[index])
        self.set_session_attribute('questions', ','.join([str(i) for i in game_questions]), '')
        self.set_session_attribute('counter', str(counter), '1')
        
        answers = self.populate_game_answers(question['options'])
        
        return r'第{0}题，{1}，的作者是？{2}中的第几个？'.format(counter, question['content'], ','.join(answers))

    def populate_game_answers(self, options):

        answers = options[:]
        random.shuffle(answers)
        answer_position = answers.index(options[0])+1
        self.set_session_attribute('position', str(answer_position), '')
        
        return answers


def handler(event, context):

    bot = DuerOSBot(event)
    result = bot.run()
    return result
