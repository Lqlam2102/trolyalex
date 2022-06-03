import time

from bean.reply import Reply
from dao import line_file
from object.assistant_info import Assistant
from object.master_info import Master
from bo.reply_bo import ReplyBo
from bo.logic_reply_bo import LogicReplyBo
from dao.word_dao import WordDao
from handling import handling
from util.constant import Constant
from handling import text_tool as TextTool
from . import message_analysis as MessageAnalysis
import GUI_class


class BotSystem:
    # getInputType = 0
    getInputType = 10
    rememberReply = None
    defaultReplyList = None


    def __init__(self, speed_speack: int = 180):
        print(f'{Assistant.name} System Init')
        self.assistant = Assistant(speed_speack)
        self.replyBo = ReplyBo()
        self.logicReplyBo = LogicReplyBo()
        WordDao.load()
        BotSystem.defaultReplyList = line_file.getFileInTrain('default_ans')

    def run(self):
        self.assistant.speak('Xin chào ' + Master.name)
        # BotSystem.getInputType = 0
        BotSystem.getInputType = 10
        while True:
            text = ''

            # lấy tin nhắn
            if BotSystem.getInputType < 3:
                text = handling.listen()
                time.sleep(2)

            elif BotSystem.getInputType == 3:
                self.assistant.speak('Tự động chuyển sang chế độ nhập tin nhắn!')
                BotSystem.getInputType = 10
                text = handling.get_text()

            else:
                text = handling.get_text()

            # kiểm tra tin nhắn
            if not text:
                BotSystem.getInputType += 1
                self.assistant.speak(f'{Assistant.name} không nghe rõ...')
                time.sleep(3)

            else:
                if BotSystem.getInputType < 3:
                    BotSystem.getInputType = 0  # reset
                text = text.lower().strip()
                if len(text) == 0:
                    continue
                # print('Text:['+ text+']')
                if text == 'bye' or text == 'tạm biệt' or text == 'bye bye' or text == 'goodbye':
                    handling.stop(self.assistant)
                    break

                elif text == 'mở nhận dạng giọng nói':
                    BotSystem.getInputType = 0
                    self.assistant.speak('Đã chuyển sang chế độ nhận dạng giọng nói!')

                elif text == 'tắt nhận dạng giọng nói':
                    BotSystem.getInputType = 10
                    self.assistant.speak('Đã chuyển sang chế độ nhập tin nhắn!')

                elif text == 'help' or text == 'trợ giúp':
                    print(Constant.HELP)

                else:
                    if BotSystem.rememberReply is not None:  # đang yêu cầu train thêm dữ liệu
                        if text.startswith('trả lời'):  # master đang train dữ liệu
                            text = text.replace('trả lời ', '')
                            text = text.replace(' hoặc ', '|')  # phân tách thành các câu trả lời riêng biệt
                            BotSystem.rememberReply.addAnswer(text)  # train thêm câu trả lời
                            firstChar = BotSystem.rememberReply.message[0]
                            self.replyBo.saveListMess(TextTool.getUnsignedChar(firstChar))
                            self.assistant.speak(f'Cảm ơn {Master.name}. {Assistant.name} sẽ ghi nhớ!')
                            BotSystem.rememberReply = None  # reset rememberReply
                        else:  # xem như một tin nhắn thông thường
                            BotSystem.rememberReply = None  # reset rememberReply cũ
                            replyMessage = self.answer(text)  # tìm câu trả lời
                            if replyMessage is None:
                                self.assistant.speak(f'{Assistant.name} nên trả lời như thế nào ạ?')
                            else:
                                self.assistant.speak(replyMessage)
                    else:
                        replyMessage = self.answer(text)  # tìm câu trả lời
                        if replyMessage is None:
                            self.assistant.speak(f'{Assistant.name} nên trả lời như thế nào ạ?')
                        else:
                            self.assistant.speak(replyMessage)

    def answer(self, message):
        # type 1: trả lời mặc định
        # type 2: yêu cầu chức năng
        result = MessageAnalysis.functionLogic(message, self.assistant)
        if result is not None:
            return result
        # type 3: trả lời bằng data

        # chuẩn hoá tin nhắn
        message = TextTool.standardMessageForTraining(message)
        message = message.strip()
        reply = self.findAnswerInReplyData(message)  # object type: Reply
        if reply is not None:
            if handling.random(29) == 12:
                BotSystem.rememberReply = reply  # lưu vào rememberReply
                return None
            else:
                result = reply.chooseAnswer()
                return result
        else:
            if handling.random(12) == 2:
                reply = Reply(message, [])  # Tạo mới một Reply
                self.replyBo.addData(reply)  # Lưu vào replyBo
                BotSystem.rememberReply = reply  # lưu lại reply để train
                return None
            else:
                # Tìm kiếm theo từ khoá
                logicAnswer = self.findAnswerInLogicReplyData(message)
                if logicAnswer is not None:  # Tìm thấy kết quả theo từ khoá
                    return logicAnswer.chooseAnswer()
                # Không tìm thấy kết quả theo từ khoá
                if handling.random(6) != 2:
                    defaultListSize = len(BotSystem.defaultReplyList)
                    if defaultListSize > 0:  # Nếu list rep mặc định không rỗng
                        pos = handling.random(defaultListSize)
                        return BotSystem.defaultReplyList[pos]  # Chọn một câu trả lời ngẫu nhiên để phản hồi
                # Xui thì vào đây train thêm dữ liệu...
                reply = Reply(message, [])  # Tạo mới một Reply
                self.replyBo.addData(reply)  # Lưu vào replyBo
                BotSystem.rememberReply = reply  # lưu lại reply để train
                return None

    '''
    Tìm kiếm trong reply list.
    Giới hạn độ dài tìm kiếm là 20 từ. Nếu quá trả về None.
    Trả về 1 Reply hoặc None
    '''

    def findAnswerInReplyData(self, message):
        if len(message.split(' ')) > 20:
            return None
            # tìm kiếm dữ liệu từ replyBo
        result = self.replyBo.search(message)
        return result

    '''
    Tìm kiếm trong logicreply list.
    Giới hạn độ dài tìm kiếm là 20 từ. Nếu quá trả về None.
    Trả về 1 LogicReply hoặc None
    '''

    def findAnswerInLogicReplyData(self, message):
        if len(message.split(' ')) > 20:
            return None
            # tìm kiếm dữ liệu từ logicReplyBo
        result = self.logicReplyBo.search(message)
        return result
