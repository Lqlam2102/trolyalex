import pyttsx3
from object import master_info

class Assistant:
    """Thông tin cá nhân của trợ lý"""
    name = 'Alex'
    alias = ['alex', 'tro ly', 'trợ lý', 'bot']
    gender = 'Nam'
    birthday = '21-3-2022'

    def __init__(self, v_p=170,):
        self.voice_speed = v_p

    # Text - to - speech: Chuyển đổi văn bản thành giọng nói
    def speak(self, text: str) -> str:
        """
        Sử lý văn bản sang âm thanh - Text to speech - Dùng pyttsx3.
        Tài liệu tham khảo: https://pypi.org/project/pyttsx3/
        Hướng dẫn tham khỏa: https://www.youtube.com/watch?v=qVMHoCtjLag
        """
        if (len(text.split(' ')) > 100):
            print(Assistant.name + ": {}".format(text))
            text = f'{master_info.Master.name} xem nội dung bên trên nhé!'

        print(Assistant.name + ": {}".format(text))
        engine = pyttsx3.init()
        newVoiceRate = self.voice_speed  # Tốc độ nói
        engine.setProperty('rate', newVoiceRate)
        voice = engine.getProperty("voices")
        engine.setProperty("voice", voice[1].id)
        engine.say(text)
        engine.runAndWait()
