'''
Attribute:
+ static listData: list[string]
Methods:
+ static load(): Lấy dữ liệu từ file synonym để vào listData
+ static similarMessages(text): Tạo ra các câu đồng nghĩa
Áp dụng: Tạo ra các câu đồng nghĩa
'''
class WordDao:
    listData = [] #list[string]
    def __init__(self):
        pass

    @staticmethod
    def load():
        WordDao.listData = []
        file = open('./file/train/synonym.txt', 'r', encoding='utf-8')
        if file is None:
            print('Mở file synonym thất bại!')
            return
        
        # duyệt từng dòng dữ liệu
        for line in file:
            if len(line) > 0:
                line = line.replace('\n', '') #lúc test bị lỗi xuống dòng nên phải bổ sung dòng này
                synonyms = line.split('|')
                WordDao.listData.append(synonyms)
        file.close()

    '''
    synonym: list[string] vd: ['như vậy', 'vậy thì']
    '''
    @staticmethod
    def addSimilar(result,text, synonyms):
        base = []
        for string in result:
            WordDao.baseSimilarReply(base, string, synonyms)
        
        for string in base:
            result.append(string)

        for string in base:
            WordDao.baseSimilarReply(result, string, synonyms)

    # Tạo các câu tương tự của 1 câu.
    @staticmethod
    def similarMessages(text):
        result = []
        result.append(text)
        
        for synonyms in WordDao.listData:
            WordDao.addSimilar(result, text, synonyms)
        return result
    
    
    
    '''
    Tạo ra các câu đồng nghĩa từ 1 đoạn text.
    listSynonym: list[string] vd: ['như vậy', 'vậy thì']
    '''
    @staticmethod
    def baseSimilarReply(result, text, synonyms):
        n = len(synonyms) # lấy số lượng của list synonym
        for i in range(0, n):
            if synonyms[i] in text: # nếu từ này có trong text
                for j in range(0, n): # duyệt các từng đồng nghĩa của synonym[i]
                    if i != j and WordDao.checkRepeatWord(text, synonyms[i], synonyms[j]):
                        data = text.replace(synonyms[i], synonyms[j])
                        if data not in result:
                            result.append(data)


    '''
    Kiểm tra khi thay rem1 bằng rem2 có gây ra lỗi trùng lặp từ hay không 
    Ex:như vậy thì đi chơi thôi 
    rem1: vậy thì 
    rem2: như vậy 
    => loại các trường hợp: như như vậy thì, vậy thì thì
    '''
    @staticmethod
    def checkRepeatWord(text, word1, word2):
        rem = word2.split(' ')
        giao = rem[0] + ' ' + word1
        
        if giao in text:
            return False
        
        giao = word1 + ' ' + rem[len(rem)-1]

        if giao in text:
            return False

        return True