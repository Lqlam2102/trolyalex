from bean.logic_reply import LogicReply
from bean.list_logic_data import ListLogicData


'''
Attribute:
+ listData: list[ListData]
Methods:

'''
class LogicReplyDao:
    listFile = ['contain_order','contain', 'startwith', 'endwith']
    def __init__(self):
        self.listData = [] #list[ListLogicData]

    # load toàn bộ dữ liệu từ các file
    def load(self):
        self.listData = [] #reset
        for i in LogicReplyDao.listFile:
            filename = i
            childList = self.getData(filename)
            self.listData.append(childList)


    #get data từ ./file/train/[filename].txt
    # trả về 1 ListLogicData
    def getData(self, filename):
        result = ListLogicData([]) # phải khởi tạo list rỗng []...Nếu không dữ liệu gây lỗi dữ liệu add hết vào một list
        file = open('./file/train/' + filename + '.txt', 'r', encoding='utf-8')
        if file is None:
            #print('Mở file ' + filename + ' thất bại!')
            return result
        
        # duyệt từng dòng dữ liệu
        for line in file:
            list = line.split(']$[') # Tách dữ liệu của mỗi dòng thành 2 phần
            if list is None or len(list) != 2:
                continue

            # Phân tích dữ liệu thành hai phần keywords và answer
            keywords = list[0]
            answers = list[1].split('|')
            replyList = []
            n = len(answers)
            for i in range(1,n):
                if answers[i] is not None:
                    replyList.append(answers[i])
            result.addData(LogicReply(keywords, replyList))
        file.close()

        return result
    

    # lưu tất cả thông tin của một list vào file
    def saveListMess(self, filename, replyList):
        #print('Save list to:', filename)
        file = open('./file/train/' + filename + '.txt', 'w', encoding='utf-8')
        for i in replyList:
            if len(i.replyMessages) > 0:
                #print(i.toString())
                file.write(i.toString())
        file.close()
    
    # cập nhật tất cả file
    def saveAll(self):
        for i in range(0, len(LogicReplyDao.listFile)):
            self.saveListMess(LogicReplyDao.listFile[i], self.listData[i].getList())

    # lưu thông tin của 1 LogicReply vào file filename
    def saveMess(self, filename, reply):
        file = open('./file/train/' + filename + '.txt', 'a', encoding='utf-8')
        file.write(reply.toString())
        file.close()

    # Thêm một logicReply vào list và cập nhật file data
    def addData(self, reply, filename):
        pos = 0
        for i in range(0, len(LogicReplyDao.listFile)):
            if filename == LogicReplyDao.listData[i]:
                pos = i
                break
        if reply.keywords is not None and len(reply.replyMessages) > 0: # nếu dữ liệu có ít nhất một câu trả lời
            self.saveMess(filename, reply)
        self.listData[pos].addData(reply)
    
    # Trả về kết quả tìm kiếm là một LogicReply hoặc None
    def search(self, message):
        for i in range(0, len(LogicReplyDao.listFile)):
            search_type = LogicReplyDao.listFile[i]
            rs = self.listData[i].search(message, search_type) #type: LogicReply
            if rs is not None:
                return rs
        return None
