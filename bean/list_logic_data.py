from handling import text_tool as TextTool
from dao.word_dao import WordDao

'''
Attribute:
+ data: list[LogicReply]
Methods:
+ addData(logicReply): Thêm một logicReply mới vào danh sách
+ search(message): Tìm kiếm reply theo message. Sinh ra thêm các message tương đồng để tìm kiếm được tốt hơn
+ size(): lấy số lượng phần tử của list data
+ getList(): lấy list data
+ get(i): lấy phần tử thứ i
Áp dụng: để lưu danh sách các LogicReply
'''
class ListLogicData:
    def __init__(self, listLogicData=[]):
        self.data = listLogicData
    
    # Thêm một reply vào list
    def addData(self, logicReply):
        if self.data is None:
            self.data = []
        else:
            self.data.append(logicReply)
    
    # Tìm kiếm một message trong list
    def search(self, message, search_type):
        message = TextTool.getOrigin(TextTool.standardMessageForTraining(message))
        message = message.strip()
        similarMessages = WordDao.similarMessages(message)
        if search_type == 'contain_order':
            for logicReply in self.data:
                # kiểm tra message có giống với logic của logicReply.keyword không
                
                if logicReply.checkLogicContain(message.lower()):
                    #print('Compare: ' + '[' + logicReply.keywords.lower() + ']' + ':[' + message.lower() + ']')
                    #print('Matched!')
                    return logicReply
                
                # kiểm tra các câu tương đồng của message
                for i in similarMessages:
                    if logicReply.checkLogicContain(i.lower()):
                        #print('Compare: ' + '[' + logicReply.keywords.lower() + ']' + ':[' + message.lower() + ']')
                        #print('Matched!')
                        return logicReply
        if search_type == 'contain':
            for logicReply in self.data:
                # kiểm tra message có giống với logic của logicReply.keyword không
                
                if logicReply.checkLogicContain(message.lower()):
                    #print('Compare: ' + '[' + logicReply.keywords.lower() + ']' + ':[' + message.lower() + ']')
                    #print('Matched!')
                    return logicReply
                
                # kiểm tra các câu tương đồng của message
                for i in similarMessages:
                    if logicReply.checkLogicContain(i.lower()):
                        #print('Compare: ' + '[' + logicReply.keywords.lower() + ']' + ':[' + message.lower() + ']')
                        #print('Matched!')
                        return logicReply
        elif search_type == 'endwidth':
            for logicReply in self.data:
                # kiểm tra message có giống với logic của logicReply.keyword không
                if logicReply.checkLogicEndWith(message.lower()):
                    #print('Compare: ' + '[' + logicReply.keywords.lower() + ']' + ':[' + message.lower() + ']')
                    #print('Matched!')
                    return logicReply
                
                # kiểm tra các câu tương đồng của message
                for i in similarMessages:
                    if logicReply.checkLogicEndWith(i.lower()):
                        #print('Compare: ' + '[' + logicReply.keywords.lower() + ']' + ':[' + message.lower() + ']')
                        #print('Matched!')
                        return logicReply
        elif search_type == 'startwith':
            for logicReply in self.data:
                # kiểm tra message có giống với logic của logicReply.keyword không
                if logicReply.checkLogicStartWith(message.lower()):
                    # print('Compare: ' + '[' + logicReply.keywords.lower() + ']' + ':[' + message.lower() + ']')
                    # print('Matched!')
                    return logicReply
                
                # kiểm tra các câu tương đồng của message
                for i in similarMessages:
                    if logicReply.checkLogicStartWith(i.lower()):
                        # print('Compare: ' + '[' + logicReply.keywords.lower() + ']' + ':[' + message.lower() + ']')
                        # print('Matched!')
                        return logicReply
        return None
    
    def size(self):
        return len(self.data)

    def getList(self):
        return self.data
    
    def get(self, i):
        return self.data[i]