from cv2 import destroyAllWindows

import GUI_class
import time
import pyttsx3
import speech_recognition as sr
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
from core import message_analysis as MessageAnalysis

window = GUI_class.GUI()
global img_win

rememberReply = None
defaultReplyList = None
img_win = 0
assistant = Assistant(180)
replyBo = ReplyBo()
logicReplyBo = LogicReplyBo()
WordDao.load()
defaultReplyList = line_file.getFileInTrain('default_ans')


def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        window.set_status("Listening...", "green")
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 0.5
        audio = r.listen(source)
        window.set_status("Processing...", "red")

    try:
        q = r.recognize_google(audio, language='vi-VN')
        window.msg_box.delete('1.0', GUI_class.END)
        window.msg_box.update()
        print("You said :", q)
        window.set_msg(f"You said :{q}")
        process(q)


    except Exception as e:
        return "none"
    return q


def take():
    assistant.speak("Xin chào Master")
    window.set_msg("Alex Online...")
    while True:
        takeCommand()


def process(text):
    global window
    global img_win
    global rememberReply
    text = text.lower()

    if text == 'bye' or text == 'tạm biệt' or text == 'bye bye' or text == 'goodbye':
        handling.stop(assistant)
        window.set_msg("Tạm biệt Master")
        destroyAllWindows()
        window.destroy()


    elif text == 'help' or text == 'trợ giúp':
        print(Constant.HELP)
        window.set_msg(Constant.HELP)
    else:
        if rememberReply is not None:  # đang yêu cầu train thêm dữ liệu
            if text.startswith('trả lời'):  # master đang train dữ liệu
                text = text.replace('trả lời ', '')
                text = text.replace(' hoặc ', '|')  # phân tách thành các câu trả lời riêng biệt
                rememberReply.addAnswer(text)  # train thêm câu trả lời
                firstChar = rememberReply.message[0]
                replyBo.saveListMess(TextTool.getUnsignedChar(firstChar))
                assistant.speak(f'Cảm ơn {Master.name}. {Assistant.name} sẽ ghi nhớ!')
                window.set_msg(f'Cảm ơn {Master.name}. {Assistant.name} sẽ ghi nhớ!')
                rememberReply = None  # reset rememberReply
            else:  # xem như một tin nhắn thông thường
                rememberReply = None  # reset rememberReply cũ
                replyMessage = answer(text)  # tìm câu trả lời
                if replyMessage is None:
                    assistant.speak(f'{Assistant.name} nên trả lời như thế nào ạ?')
                else:
                    assistant.speak(f'{assistant.name}:{replyMessage}')
        else:
            replyMessage = answer(text)  # tìm câu trả lời
            if replyMessage is None:
                assistant.speak(f'{Assistant.name} nên trả lời như thế nào ạ?')
                window.set_msg(f'{assistant.name}:{Assistant.name} nên trả lời như thế nào ạ?')
            else:
                assistant.speak(replyMessage)
                window.set_msg(f'{assistant.name}: {replyMessage}')


def answer(message):
    global rememberReply
    global defaultReplyList
    # type 1: trả lời mặc định
    # type 2: yêu cầu chức năng
    result = MessageAnalysis.functionLogic(message, assistant)
    if result is not None:
        return result
    # type 3: trả lời bằng data

    # chuẩn hoá tin nhắn
    message = TextTool.standardMessageForTraining(message)
    message = message.strip()
    reply = findAnswerInReplyData(message)  # object type: Reply
    if reply is not None:
        if handling.random(29) == 12:
            rememberReply = reply  # lưu vào rememberReply
            return None
        else:
            result = reply.chooseAnswer()
            return result
    else:
        if handling.random(12) == 2:
            reply = Reply(message, [])  # Tạo mới một Reply
            replyBo.addData(reply)  # Lưu vào replyBo
            rememberReply = reply  # lưu lại reply để train
            return None
        else:
            # Tìm kiếm theo từ khoá
            logicAnswer = findAnswerInLogicReplyData(message)
            if logicAnswer is not None:  # Tìm thấy kết quả theo từ khoá
                return logicAnswer.chooseAnswer()
            # Không tìm thấy kết quả theo từ khoá
            if handling.random(6) != 2:
                defaultListSize = len(defaultReplyList)
                if defaultListSize > 0:  # Nếu list rep mặc định không rỗng
                    pos = handling.random(defaultListSize)
                    return defaultReplyList[pos]  # Chọn một câu trả lời ngẫu nhiên để phản hồi
            # Xui thì vào đây train thêm dữ liệu...
            reply = Reply(message, [])  # Tạo mới một Reply
            replyBo.addData(reply)  # Lưu vào replyBo
            rememberReply = reply  # lưu lại reply để train
            return None


'''
Tìm kiếm trong reply list.
Giới hạn độ dài tìm kiếm là 20 từ. Nếu quá trả về None.
Trả về 1 Reply hoặc None
'''


def findAnswerInReplyData(message):
    if len(message.split(' ')) > 20:
        return None
        # tìm kiếm dữ liệu từ replyBo
    result = replyBo.search(message)
    return result


'''
Tìm kiếm trong logicreply list.
Giới hạn độ dài tìm kiếm là 20 từ. Nếu quá trả về None.
Trả về 1 LogicReply hoặc None
'''


def findAnswerInLogicReplyData(message):
    if len(message.split(' ')) > 20:
        return None
        # tìm kiếm dữ liệu từ logicReplyBo
    result = logicReplyBo.search(message)
    return result


if __name__ == "__main__":
    window_width = 590  # width of window
    window_height = 728  # height of window

    window.geometry(f"{window_width}x{window_height}")
    window.title("Alex - Trợ lý của sinh viên")

    b1 = GUI_class.Button(window.background_label, text="Invoke Alex", command=take)
    b1.pack()

    window.create_statusbar_msgbox()
    window.set_status("Ready", "blue")

    window.mainloop()
