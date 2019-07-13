#!/usr/bin/env python2
# -*- encoding=utf-8 -*-
import sys
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
        card = TextCard('欢迎使用我来查税')
        return {
            'card': card,
            'outputSpeech': r'欢迎使用我来查税'
        }
    

    def ended_request(self):
        """
        关闭技能
        """
        self.wait_answer()
        return {
            'outputSpeech': r'感谢您使用我来查税'
        }

    def __init__(self, request_data):
        super(DuerOSBot, self).__init__(request_data)
        self.add_launch_handler(self.launch_request)
        self.add_session_ended_handler(self.ended_request)
        self.add_intent_handler('inquiry_tax', self.inquiry_tax_intent)
    
    

    def inquiry_tax_intent(self):
        salary=self.get_slots('salaryMonthly')
        if not salary:
            self.nlu.ask('salaryMonthly')
            return{
                'outputSpeech':r'你一个月工资多少？'
            } 

        loc=self.get_slots('Location')
        if not loc:
            self.nlu.ask('Location')
            return{
            'outputSpeech':r'你在哪里上班？'
            }     
        card = TextCard('你的税额是100元')
        return {
            'card': card,
            'outputSpeech': r'你的税额是100元'
        }

def handler(event, context):

    bot = DuerOSBot(event)
    result = bot.run()
    return result
