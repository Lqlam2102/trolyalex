from dao.reply_dao import ReplyDao


class ReplyBo:
    def __init__(self):
        self.dao = ReplyDao()
        self.dao.load() #load dữ liệu từ file
    
    def saveListMess(self, filename):
        self.dao.saveListMess(filename)

    def saveAll(self):
        self.dao.saveAll()
    
    # Thêm một reply vào list và cập nhật file data
    def addData(self, reply):
        self.dao.addData(reply)
    
    # Tìm kiếm câu trả lời từ danh sách reply
    def search(self, message):
        return self.dao.search(message)
        