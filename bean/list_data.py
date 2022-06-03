from handling import text_tool as TextTool
from dao.word_dao import WordDao

'''
Attribute:
+ data: list[Reply]
Methods:
+ addData(reply): Thêm một reply mới vào danh sách
+ search(message): Tìm kiếm reply theo message. Sinh ra thêm các message tương đồng để tìm kiếm được tốt hơn
+ size(): lấy số lượng phần tử của list data
+ getList(): lấy list data
+ get(i): lấy phần tử thứ i
Áp dụng: Để lưu trữ danh sách các Reply
'''
class ListData:
    def __init__(self, listReply=[]):
        self.data = listReply #list[Reply]
    
    # Thêm một reply vào list
    def addData(self, reply):
        if self.data is None:
            self.data = []
        else:
            self.data.append(reply)
    
    # Tìm kiếm một message trong list
    def search(self, message):
        message = TextTool.getOrigin(TextTool.standardMessageForTraining(message))
        message = message.strip()
        similarMessages = WordDao.similarMessages(message) # tạo các câu đồng nghĩa
        for reply in self.data:
            # kiểm tra message có giống với  reply.message không
            #print('Compare: ' + '[' + reply.message.lower() + ']' + ':[' + message.lower() + ']')
            if reply.message.lower() == message.lower():
                # print('Compare: ' + '[' + reply.message.lower() + ']' + ':[' + message.lower() + ']')
                # print('Matched!')
                return reply
            
            # kiểm tra các câu tương đồng của message
            for i in similarMessages:
                if i.lower() == reply.message.lower():
                    # print('Compare: ' + '[' + reply.message.lower() + ']' + ':[' + message.lower() + ']')
                    # print('Matched!')
                    return reply
        return None
    
    def size(self):
        return len(self.data)

    def getList(self):
        return self.data
    
    def get(self, i):
        return self.data[i]