from bean.reply import Reply
from bean.list_data import ListData
from handling import text_tool as TextTool

'''
Attribute:
+ listData: list[ListData]
Methods:

'''
class ReplyDao:
    def __init__(self):
        self.listData = [] #list[ListData]

    # load toàn bộ dữ liệu từ các file
    def load(self):
        self.listData = [] #reset
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        for i in range(0, 26):
            filename = alphabet[i]
            childList = self.getData(filename) #type: ListData
            #print('File:', alphabet[i])
            #print('SL:', len(childList.getList()))
            self.listData.append(childList)
        self.listData.append(self.getData('khac'))


    #get data từ ./file/train/[filename].txt
    # trả về 1 ListData
    def getData(self, filename):
        result = ListData([]) # phải khởi tạo list rỗng []...Nếu không dữ liệu gây lỗi dữ liệu add hết vào một list
        file = open('./file/train/' + filename + '.txt', 'r', encoding='utf-8')
        if file is None:
            #print('Mở file ' + filename + ' thất bại!')
            return result
        
        # duyệt từng dòng dữ liệu
        for line in file:
            list = line.split('|') # Tách dữ liệu của mỗi dòng
            if list is None or len(list) < 2:
                continue

            # Phân tích dữ liệu thành hai phần message và replyList
            message = list[0]
            replyList = []
            n = len(list)
            for i in range(1,n):
                if list[i] is not None:
                    replyList.append(list[i])
            result.addData(Reply(message, replyList))
        file.close()

        return result
    

    # lưu tất cả thông tin của một list vào file
    def saveListMess(self, filename):
        # lấy vị trí của list cần lưu
        pos = 26 #khac
        if filename >= 'a' and filename <= 'z':
            pos = ord(filename)-ord('a')

        #Lấy list
        replyList = self.listData[pos].getList()
        #print('Save list to:', filename)
        file = open('./file/train/' + filename + '.txt', 'w', encoding='utf-8')
        for i in replyList:
            if len(i.replyMessages) > 0:
                #print(i.toString())
                file.write(i.toString())
        file.close()
    
    # cập nhật tất cả file
    def saveAll(self):
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        for i in range(0, 26):
            self.saveListMess(alphabet[i], self.listData[i].getList())
        self.saveListMess('khac', self.listData[26].getList())

    # lưu thông tin của 1 reply vào file filename
    def saveMess(self, filename, reply):
        file = open('./file/train/' + filename + '.txt', 'a', encoding='utf-8')
        file.write(reply.toString())
        file.close()

    # Thêm một reply vào list và cập nhật file data
    def addData(self, reply):
        filename = TextTool.getUnsignedChar(reply.message[0].lower()) #lấy ký tự đầu tiên của reply.message
        pos = 26 #khac
        if filename >= 'a' and filename <= 'z':
            if reply.message is not None and len(reply.replyMessages) > 0: # nếu dữ liệu có ít nhất một câu trả lời
                self.saveListMess(filename)
            pos = ord(filename)-ord('a')
        else:
            if reply.message is not None and len(reply.replyMessages) > 0: # nếu dữ liệu có ít nhất một câu trả lời
                self.saveListMess('khac')
        self.listData[pos].addData(reply)
    
    #
    def search(self, message):
        firstchar = TextTool.getUnsignedChar(message[0].lower())
        pos = 26 #khac
        if firstchar >= 'a' and firstchar <= 'z':
            pos = ord(firstchar)-ord('a')
        
        #print('Tìm kiếm theo ký tự:', firstchar)
        
        #DEBUG
        # print('Tại phần tử', pos, ' trong listdata!')
        # for i in self.listData:
        #     print(len(i.getList()))
        return self.listData[pos].search(message)
