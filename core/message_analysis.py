from time import strftime
from handling import text_tool as TextTool
from handling import handling as Function
from object import master_info as Master

'''
Kiểm tra tin nhắn có phải là tin nhắn yêu cầu chức năng không.
Nếu phải thì trả về 1 kết quả. Nếu không có kết quả thì trả về null.
Nếu ko phải yêu cầu chức năng thì trả về null.
'''


def functionLogic(message,Assistant):
    starts = ['vậy thì', 'thế thì', 'vậy cứ ', 'thế ', 'thử ', 'vậy ', 'thì ']
    for word in starts:
        if message.startswith(word):
            message = message.replace(word, '')

    if 'mấy giờ' in message:
        return 'Bây giờ là ' + Function.getTime()

    if f'chào {Assistant.name.lower()}' in message or f'chào {Assistant.alias}'.lower() in message:
        day_time = int(strftime('%H'))
        if day_time < 12:
            return "Chào buổi sáng {}. Chúc {} một ngày tốt lành.".format(Master.Master.name, Master.Master.name)
        elif 12 <= day_time < 18:
            return "Chào buổi chiều {}. {} đã dự định gì cho chiều nay chưa.".format(Master.Master.name, Master.Master.name)
        else:
            return "Chào buổi tối {}. {} đã ăn tối chưa nhỉ.".format(Master.Master.name, Master.Master.name)

    if message.startswith('thông tin của'):
        for alias in Master.Master.alias:
            if alias.lower() in message:
                return f"Tên: {Master.Master.name}, tuổi: {Master.Master.age}, giới tính: {Master.Master.gender}"
        for alias in Assistant.alias:
            if alias.lower() in message:
                return f"Tên: {Assistant.name}, sinh ngày: {Assistant.birthday}, giới tính: {Assistant.gender}"
        rem = message.split(' ')
        if len(rem) >= 4:  # rem phải từ 4 từ trở lên
            message = message.replace('thông tin của', '')
            result = Function.wikipedia(message)
            return result
    if 'giờ đi ngủ' in message or 'thời gian đi ngủ' in message:
        return Function.time_sleep()

    if message.startswith('cách') or message.startswith('làm cách nào để') or message.startswith('làm sao để'):
        message.replace('mình', 'bạn')
        rem = message.split(' ')
        if (message.startswith('cách') and len(rem) >= 3) or len(rem) >= 5:  # rem phải từ 3 từ trở lên
            result = Function.howTo(message)
            return result

    if message.startswith('tìm kiếm') or message.startswith('search'):
        if TextTool.cauXungHo2(message):
            return None
        message = message.replace('tìm kiếm', '')
        message = message.replace('search', '')

        result = Function.searchGoogle(message)
        return result

    if message.startswith('thời tiết') or 'dự báo thời tiết' in message:
        message = message.replace("có tốt không", "như thế nào")
        message = message.replace('tốt không', 'như thế nào')

        passedKey = ['hôm qua', 'ngày qua', 'ngày trước', 'tuần trước', 'tháng trước', 'năm trước', 'năm ngoái']
        for word in passedKey:
            if word in message:
                return Assistant.name + ' không có dữ liệu của quá khứ ạ!'

        farFutureKey = ['tuần sau', 'tuần tới', 'tuần kế tiếp', 'mùa sau', 'tháng sau', 'năm sau']
        for word in farFutureKey:
            if word in message:
                return Assistant.name + ' chỉ có dữ liệu thời tiết trong tuần này thôi ạ!'

        legalKey = ['ngày', 'hôm nay', 'thứ ', 'chủ nhật', 'thế nào']
        for word in legalKey:
            if word in message:
                return Function.weather(message)

        if message == 'thời tiết':
            return Function.weather(message)
        return None

    if (message == 'mở nhạc' or message == 'play music' or message == 'bật nhạc'
            or message == 'open music' or message == 'chuyển bài' or message == 'next music'
            or message == 'bật bài khác' or message == 'đổi bài hát' or message == 'bài hát khác'):
        filedir = Function.openRandomMusic()
        if filedir == None:
            return 'không tìm thấy bài hát trong thư mục nhạc! Master hãy vào setting để kiểm tra lại!'
        return 'Mở bài hát: ' + filedir

    if message.startswith('tìm bài hát'):
        message = message.replace('tìm bài hát ', '')
        listKey = message.split(' ')
        size = len(listKey)
        query = ''
        if size != 0:
            if size > 10:  # chỉ lấy tối đa 10 từ
                size = 10
            for i in range(0, size):
                query += listKey[i] + ' '
            query = query.strip()
            Function.openMusicOnline(query)
        return 'Tìm kiếm bài hát theo từ khoá: ' + message

    if message.startswith('lời bài hát') or message.startswith('tìm lời bài hát'):
        message = message.replace('tìm lời bài hát ', '')
        message = message.replace('lời bài hát ', '')
        listKey = message.split(' ')
        size = len(listKey)
        query = ''
        if size != 0:
            if size > 10:  # chỉ lấy tối đa 10 từ
                size = 10
            for i in range(0, size):
                query += listKey[i] + ' '
            query = query.strip()
            Function.lyric(query)
        return 'Tìm kiếm lời bài hát theo từ khoá: ' + message

    if message.startswith('mở online bài hát') or message.startswith('bật online bài hát'):
        message = message.replace('mở online bài hát ', '')
        message = message.replace('bật online bài hát ', '')
        Function.openMusicOnline(message)
        return 'Mở online bài hát: ' + message

    # Tìm bài hát offline theo yêu cầu để mở, nếu không có thì tìm kiếm online
    if message.startswith('mở bài hát') or message.startswith('bật bài hát'):
        message = message.replace('mở bài hát ', '')
        message = message.replace('bật bài hát ', '')
        Function.openMusic(message)
        return 'Mở bài hát: ' + message

    if message == 'mở máy tính' or message == 'mở calculator':
        return Function.openCalculator()

    if message == 'mở chrome' or message == 'mở trình duyệt' or message == 'mở google chrome':
        return Function.openChrome()

    if message == 'mở word':
        return Function.openWord()

    if message == 'mở excel':
        return Function.openExcel()

    if message == 'mở bản đồ':
        return Function.openMap()

    if 'mở mail' in message or 'mở mail' in message:
        return Function.openMail()


    if 'gửi mail' in message:
        Assistant.speak('Master muốn gửi mail đến ai ạ?')
        mailto = Function.get_text()
        Assistant.speak('Master muốn đặt tiêu đề là gì ạ?')
        title = Function.get_text()
        Assistant.speak('Master muốn gửi với nội dung thế nào ạ?')
        content = Function.get_text()
        return Function.sendMail(mailto, title, content)

    if message.startswith('mở '):
        result = Function.openBookMark(message.replace('mở ', ''))
        return result

    # Tìm kiếm thông tin từ wikipedia
    if 'là gì' in message:
        if TextTool.cauXungHo2(message):
            return None
        rem = message.split(' ')
        if len(rem) >= 3:  # rem phải từ 3 từ trở lên
            message = message.replace('là gì', '')
            result = Function.wikipedia(message)
            return result

    if 'là ai' in message:
        if TextTool.cauXungHo(message):
            return None
        rem = message.split(' ')
        if len(rem) >= 3:  # rem phải từ 3 từ trở lên
            message = message.replace('là ai', '')
            result = Function.wikipedia(message)
            return result

    if message.startswith('khái niệm') or message.startswith('định nghĩa'):
        rem = message.split(' ')
        if len(rem) >= 3:  # rem phải từ 3 từ trở lên
            result = Function.wikipedia(message)
            return result

    if message.startswith('tiểu sử'):
        rem = message.split(' ')
        if len(rem) >= 3:  # rem phải từ 3 từ trở lên
            result = Function.wikipedia(message.replace('tiểu sử', ' '))
            return result

    return None
