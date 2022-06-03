import glob
import os
import smtplib
import subprocess
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import speech_recognition as sr
from selenium.webdriver.common.by import By
# from object.master_info import Master
from dao import line_file
from object.assistant_info import Assistant
from object.master_info import Master
from numpy import random as rd
from selenium.webdriver.chrome.options import Options
import webbrowser as wb
from util.constant import Constant
import wikipedia as wiki
from selenium import webdriver
import datetime
from pywikihow import WikiHow as wikihow
from . import text_tool as TextTool


# region Xử lý đầu vào
def get_audio() -> str:
    """
    Xử lý âm thanh sang văn bản - Speech to text - sử dụng speech_recognition.
    Tài liệu về speech_recognition: https://pypi.org/project/SpeechRecognition/2.1.3/
    """
    print(Assistant.name + ": \tĐang kết nối với Microphone \t --__-- ")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(
            source)  # lắng nghe trong 1 giây để hiệu chỉnh ngưỡng năng lượng cho mức độ tiếng ồn xung quanh
        print("\nMaster: ", end='')
        audio = r.listen(source,phrase_time_limit=5)
        try:
            text = r.recognize_google(audio, language="vi-VN")
            print(text)
            return text.lower()
        except:
            print("...")
            return ""


def time_sleep() -> str:
    time = datetime.datetime.now()
    t = datetime.timedelta(hours=1, minutes=44)
    space = datetime.timedelta(hours=1, minutes=30)
    s = time + t
    result = s
    rs = f'''Chào {Master.name}, bây giờ là {time.hour}:{time.minute}. Nếu bạn đi ngủ ngay bây giờ,
     bạn nên cố gắng thức dậy vào một trong những thời điểm sau: '''
    for i in range(4):
        rs += f'{result.hour}:{result.minute} hoặc '
        result += space
    rs += f'''{result.hour}:{result.minute}
    (Thức dậy giữa một chu kỳ giấc ngủ khiến bạn cảm thấy mệt mỏi, 
    nhưng khi thức dậy vào giữa chu kỳ tỉnh gấc sẽ làm bạn cảm thấy tỉnh táo và minh mẫn)'''
    return rs


def listen() -> str:
    """
    Xử lý văn bản. Chuyển văn bản về dạng chữ thường không in hoa.
    """
    text = get_audio()
    if text:
        return text.lower()
    else:
        return ""


def get_text() -> str:
    text = input('\n' + Master.name + ':')
    return text


def stop(Assistant):
    Assistant.speak("Hẹn gặp lại " + Master.name)
    time.sleep(1)


# endregion

# region Xử lý chức năng
# KHỞI TẠO
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
wiki.set_lang('vi')


def chromeDriverInit():
    # Khởi tạo đối tượng dùng chromedriver
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path=Constant.CHROME_DRIVER)

    return driver


def random(range: int):
    result = rd.randint(range)
    return result


def getTime():
    result = datetime.datetime.now().strftime("%I:%M %p")
    return result


def wikipedia(text: str) -> str:
    '''
    Trả về kết quả tìm kiếm thông tin từ wikipedia. Nếu không tìm thấy kết quả trả về null.
    '''
    try:
        contents = wiki.summary(text).split('\n')
        return contents[0].split(".")[0]
    except:
        return f'{Assistant.name} không định nghĩa được từ ' + text
    return None


def searchGoogle(query):
    '''
    Mở google bằng trình duyệt với một truy vấn
    '''
    url = "https://www.google.com/search?q=" + query
    openLink(url)
    return 'Đã tìm kiếm kết quả bằng google cho từ khoá: ' + query


def openLink(link):
    wb.open(link, new=2)
    return 'Đã mở link: {}'.format(link)


def howTo(text):  # Wiki
    listResult = wikihow.search(text, lang='vn')
    result = ''
    dem = 1
    for how_to in listResult:
        result += TextTool.decode(how_to.title) + '\n'
        result += how_to.intro + '\n'
        for s in how_to.steps:
            result += str(dem) + '. ' + s.summary + '\n'
            dem = dem + 1
        break
    return result


def weather(query):
    driver = chromeDriverInit()
    url = "https://www.google.com/search?q={}".format(query)
    driver.get(url)
    # time.sleep(3)
    elements0 = driver.find_elements(by=By.CSS_SELECTOR, value="#wob_loc")
    position = [el.text for el in elements0]
    if position:
        # vt = position[0].split("[,]")
        # if len(vt) <= 2:
        location = position
        # else: location = "Vị trí:" + vt[1] +","+vt[2]
        elements1 = driver.find_elements(by=By.CSS_SELECTOR, value="#wob_dts")
        dateOfWeek = [el.text for el in elements1]

        elements2 = driver.find_elements(by=By.CSS_SELECTOR, value="#wob_tm")
        temperature = [el.text for el in elements2]

        elements3 = driver.find_elements(by=By.CSS_SELECTOR, value="#wob_dc")
        status = [el.text for el in elements3]

        elements4 = driver.find_elements(by=By.CSS_SELECTOR, value="#wob_pp")
        precipitation = [el.text for el in elements4]

        elements5 = driver.find_elements(by=By.CSS_SELECTOR, value="#wob_hm")
        humidity = [el.text for el in elements5]

        elements6 = driver.find_elements(by=By.CSS_SELECTOR, value="#wob_ws")
        windspeed = [el.text for el in elements6]
        content = """
        Thông tin thời tiết:
        Vị trí {location}
        Thời điểm {dateOfWeek}
        Nhiệt độ{temperature}
        Dự báo {status}
        Khả năng có mưa {precipitation}
        Độ ẩm {humidity}
        Sức gió {windspeed}""".format(location=location, dateOfWeek=dateOfWeek, temperature=temperature, status=status,
                                      precipitation=precipitation, humidity=humidity, windspeed=windspeed)
        return content
    elif not position:
        openLink("https://www.google.com/search?q={}".format(query))
        return f"{Assistant.name} không thể truy xuất nhanh thông tin thời tiết vào hiện tại. Alice sẽ mở trình duyệt giúp Master!\n"


def openRandomMusic():
    pa = Constant.MUSIC_PATH
    listMusic = glob.glob(os.path.join(pa, '*.mp3')) + glob.glob(os.path.join(pa, '*.flac'))
    if listMusic is None or len(listMusic) == 0:
        return 'Không tìm được bài hát nào trong thư mục ' + pa
    rand = random(len(listMusic))
    st = listMusic[rand]

    subprocess.call(st, shell=True)  # mở bài hát đưa về
    return 'Mở 1 bài hát ngẫu nhiên!'






def lyric(musicName):
    driver = chromeDriverInit()
    url = "https://www.nhaccuatui.com/tim-kiem?q=" + musicName
    driver.get(url)
    try:
        data = line_file.getLineInCssSelector('lyric')
        if data is None:
            return 'Chức năng lyric hiện không thể hoạt động!'
        selector = data.split('|')
        searchList = driver.find_elements(by=By.CSS_SELECTOR, value=(selector[0]))
        bestResult = searchList[0]
        urlMusic = bestResult.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
        print('Url Song:', urlMusic)
        lyricDoc = chromeDriverInit()
        lyricDoc.get(urlMusic)
        songName = lyricDoc.find_elements(by=By.CSS_SELECTOR, value=selector[1])
        composer = lyricDoc.find_elements(by=By.CSS_SELECTOR, value=selector[2])
        result = "Thông tin:\n" + songName + composer
        lyricElement = lyricDoc.find_element(by=By.ID, value=selector[3])
        lyric = lyricElement.text
        result += lyric
        return result

    except Exception as e:
        # print(e)
        pass
    searchGoogle('Lời bài hát ' + musicName)
    return 'Tìm kiếm lời bài hát online!'


def openMusicOnline(musicName):
    driver = chromeDriverInit()
    url = "https://www.nhaccuatui.com/tim-kiem?q=" + musicName
    # url = "https://zingmp3.vn/tim-kiem/tat-ca?q=" + musicName
    driver.get(url)
    try:
        data = line_file.getLineInCssSelector('lyric')
        if data is None:
            return 'Chức năng lyric hiện không thể hoạt động!'
        selector = data.split('|')
        searchList = driver.find_elements(by=By.CSS_SELECTOR, value=selector[0])
        bestResult = searchList[0]
        urlMusic = bestResult.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
        print('Url Song:', urlMusic)
        openLink(urlMusic)
        return 'Mở bài hát ' + musicName
    except Exception as e:
        pass
    return 'Mở chức năng mở bài hát online!'


def openMusic(musicName):
    pa = Constant.MUSIC_PATH
    # t = input()
    t = musicName.upper()

    # open file .mp3
    for filename in glob.glob(os.path.join(pa, '*.mp3')):
        # print(filename)
        if len(filename) < 1:
            continue
        rem = TextTool.chuanHoaTenFile(filename)
        # thêm 1 ký tự '\' vào trước tên file để thành ...\\tenFile.mp3
        fn = rem.split('[\]')
        # cắt đường dẫn đang lõi thành 2 phần đường dẫn file_cha và tên_file_nhạc
        fn1 = fn[0].split('\\')
        st = fn1[0] + '/' + fn1[1]  # nối thành đường dẫn hợp lệ
        st1 = str(st)
        tam = st1.split('/')
        x = len(tam)
        temp = fn1[len(fn1) - 1].split('.')  # cắt lấy tên file
        nameSong = temp[0]

        if (t in nameSong.upper()):
            subprocess.call(filename, shell=True)  # mở bài hát đưa về
            return 'Đã mở bài hát ' + musicName

    # open file .raw
    for filename in glob.glob(os.path.join(pa, '*.flac')):

        if len(filename) < 1:
            continue
        rem = TextTool.chuanHoaTenFile(filename)
        # thêm 1 ký tự '\' vào trước tên file để thành ...\\tenFile.mp3
        fn = rem.split('[\]')
        # cắt đường dẫn đang lõi thành 2 phần đường dẫn file_cha và tên_file_nhạc
        fn1 = fn[0].split('\\')
        st = fn1[0] + '/' + fn1[1]  # nối thành đường dẫn hợp lệ
        st1 = str(st)
        tam = st1.split('/')
        x = len(tam)
        temp = fn1[len(fn1) - 1].split('.')  # cắt lấy tên file
        nameSong = temp[0]

        if (t in nameSong.upper()):
            subprocess.call(filename, shell=True)  # mở bài hát đưa về
            return 'Đã mở bài hát ' + musicName

    # open music online
    openMusicOnline(musicName)
    return 'Mở chức năng mở bài hát!'


def openCalculator():
    os.system('start calc')
    return 'Mở calculator'


def openChrome():
    os.system('start chrome')
    return 'Mở chrome'


def openMap():
    openLink('https://www.google.com/maps')
    return 'Mở chức năng open map'


def openMail():
    openLink('https://mail.google.com/mail/u/0/#inbox')
    return 'Mở chức năng open mail'


def openWord():
    os.system("start winword")
    return 'Mở chức năng mở word'


def openExcel():
    os.system("start excel")
    return 'Mở chức năng open excel'


def openBookMark(title):
    listBookmark = line_file.getBookmarkInAddress('bookmark')
    if listBookmark is None:
        return None
    for bookmark in listBookmark:
        if bookmark['title'].lower() == title:
            openLink(bookmark['link'])
            return 'Mở ' + bookmark['title']
    return None


def sendMail(mailto, subject, content):
    msg = MIMEMultipart()
    msg['From'] = Constant.MAIL_ADDRESS
    msg['To'] = mailto
    msg['Subject'] = subject
    body = content
    msg.attach(MIMEText(body, 'plain'))
    try:
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login(Constant.MAIL_ADDRESS, Constant.MAIL_PASS)  # Username + Password
        text = msg.as_string()
        mail.sendmail(Constant.MAIL_ADDRESS,
                      mailto, text.encode('utf-8'))  # mailto là địa chỉ người nhận
        mail.close()
        return 'Đã gửi mail có nội dung ' + content + ' đến ' + mailto
    except:

        return 'Chức năng gửi mail tạm thời không hoạt động!'

# endregion
