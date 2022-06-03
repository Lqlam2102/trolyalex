from handling import text_tool as TextTool
from numpy import random


'''
Gồm 2 attributes: 
 + message: string(vd: 'em ăn cơm chưa')
 + replyMessage: list[String](vd: ['e chưa ăn', 'e không biết ăn', 'dạ chưa', 'master nấu cho e ăn nhé'])

Mục đích: để tìm kiếm câu trả lời cho một message bằng cách tìm kiếm theo từ khoá có trong message
Vd: như mẫu trên
LogicReply trên sẽ matched với đúng câu em ăn cơm chưa
Áp dụng để train dữ liệu nhanh với tập dữ liệu có sẵn
'''
class Reply:
    #constructor
    def __init__(self, message, replyMessages=[]):
        self.message = message #string
        self.replyMessages = replyMessages #list[String]

    
    #methods
    def addAnswer(self, ans):
        """đọc dữ liệu để trả lời"""
        list = ans.split('|')
        for i in list:
            data = TextTool.standardReplyForTraining(i)
            data = data.strip()
            if data is not None and data not in self.replyMessages:
                self.replyMessages.append(data)


    # chọn câu trả lời
    def chooseAnswer(self):
        """random câu trả lời cho linh hoạt"""
        n = len(self.replyMessages)
        #print('Reply size:', n)
        if n == 0:
            return None
        rand = random.randint(n)
        #print('Rand:', rand)
        result = self.replyMessages[rand]
        return result

    # tạo thành chuỗi để lưu vào file data
    def toString(self):
        result = self.message
        for i in self.replyMessages:
            result += '|' + i
        return result
