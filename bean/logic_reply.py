from numpy import random
from handling import text_tool

'''
Gồm 2 attributes: 
 + keywords: string(vd: 'ăn cơm&chưa|ăn tối&chưa|ăn sáng&chưa|ăn trưa|chưa')
 + replyMessage: list[String](vd: ['bot chưa ăn', 'bot không biết ăn', 'dạ chưa', 'master nấu cho e ăn nhé'])

Mục đích: để tìm kiếm câu trả lời cho một message bằng cách tìm kiếm theo từ khoá có trong message
Vd: như mẫu trên
LogicReply trên sẽ matched với một số câu như: ăn cơm chưa, em ăn tối chưa vậy, alice ăn sáng chưa thế, đã ăn trưa chưa nào...
Áp dụng để tìm câu trả lời theo từ khoá
'''
class LogicReply:
    def __init__(self, keywords, replyMessages=[]):
        self.keywords = keywords #string
        self.replyMessages = replyMessages #list[string]
    
    

    # Kiểm tra mess có khớp với các logic của reply này không hay không
    def checkLogicContain(self, mess):
        listKey = self.keywords.split('|')
        for i in listKey:
            list = i.split('&')
            flag = True
            for key in list:
                if key not in mess:
                    flag = False
                    break
            if flag:
                return True
        return False

    # kiểm tra message có khớp với một trong số logic này không
    def checkLogicEndWith(self, mess):
        listKey = self.keywords.split('|')
        for i in listKey:
            if mess.endswith(i):
                return True
        return False

    # kiểm tra message có khớp với một trong số logic này không
    def checkLogicStartWith(self, mess):
        listKey = self.keywords.split('|')
        for i in listKey:
            if mess.startswith(i):
                return True
        return False

    # Thêm câu trả lời cho reply
    def addAnswer(self, ans):
        list = ans.split('|')
        for i in list:
            data = text_tool.standardReplyForTraining(i)
            if data is not None:
                if data not in self.replyMessages:
                    self.replyMessages.append(data)
    
    # chọn câu trả lời
    def chooseAnswer(self):
        n = len(self.replyMessages)
        if n == 0:
            return None
        rand = random.randint(n)
        result = self.replyMessages[rand]
        return result

    def toString(self):
        result = self.keywords
        result += ']$['
        for i in self.replyMessages:
            result += i + '|'
        return result
    