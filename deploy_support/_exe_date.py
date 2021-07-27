import codecs
import re
def Date_to_word(sentence):
    dict_start = ["từ", "đến", "ngày", "lúc", "hôm", "hồi", "chiều", "sáng", "đợt", "tháng"]
    pattern_ddmm = r'\d{1,2}[-/.]\d{1,2}$'
    pattern_ddmmyyyy = r'\d{1,2}[-/.]\d{1,2}[-/.]\d{4}$'
    pattern_mmyyyy = r'\d{1,2}[-/.]\d{4}$'
    words = sentence.split(" ")
    for i in range(0, len(words)-1):
        if words[i] in dict_start:
            if re.match(pattern_ddmm, words[i+1]):
                pieces = re.split('\W+',words[i+1])
                words[i+1] = pieces[0] + " tháng " + pieces[1]
            elif re.match(pattern_ddmmyyyy, words[i+1]):
                pieces = re.split('\W+', words[i + 1])
                words[i + 1] = pieces[0] + " tháng " + pieces[1] + " năm " + pieces[2]
            elif re.match(pattern_mmyyyy, words[i+1]):
                pieces = re.split('\W+', words[i + 1])
                words[i + 1] = pieces[0] + " năm " + pieces[1]
    sentence = " ".join(words)
    return sentence

dict_number = {'0':" không", '1':" một",'2':" hai",'3':" ba",'4':" bốn",'5':" năm",'6':" sáu",'7':" bảy",'8':" tám",'9':" chín", '10':" mười", '20':" hai mươi", '30':" ba mươi", '40':" bốn mươi", '50':" năm mươi",'60':" sáu mươi",'70':" bảy mươi",'80':" tám mươi",'90':" chín mươi"}
dict_dv = {'m':" mét", 'dm' :" đề xi mét" , 'cm' :" xen ti mét", 'mm':" mi li mét", 'ha':" héc ta", 'm2' :" mét vuông" , 'm3':" mét khối", '.':" chấm", '-':" đến"}
div_dv2 = {'-':" đến", '/':" trên"}
#ok1 : 1 so truoc no bang 0, ok2: 1 co so khac 0 dang truoc
def call_number(s, ok1, ok2 ):
    if len(s) == 1:
        if s[0] == '0':
            if ok2:
                return " "
            else:
                return dict_number[s[0]]
        if ok1:
            if ok2:
                return " linh " + dict_number[s[0]]
            else:
                return dict_number[s[0]]
        else:
            return dict_number[s[0]]
    if s[0] == '0':
        ok1 = 1
    else:
        ok2 = 1
        ok1 = 0
    if len(s) == 2:
        if s[0] == '0':
            if ok2:
                return " " + call_number(s[1:], ok1, ok2)
            else:
                return dict_number[s[0]] + call_number(s[1:], ok1, ok2)
        else:
            return dict_number[s[0]+'0'] + call_number(s[1:], ok1, ok2)
    if len(s) == 3:
        if s[0] == '0':
            if ok2:
                return " không trăm " + call_number(s[1:], ok1, ok2)
            else:
                return " không " + call_number(s[1:], ok1, ok2)
        else:
            return dict_number[s[0]] + " trăm " + call_number(s[1:], ok1, ok2)
    if len(s) == 4:
        if s[0] == '0':
            if ok2:
                return  call_number(s[1:], ok1, ok2)
            else:
                return " không " + call_number(s[1:], ok1, ok2)
        else:
            return dict_number[s[0]] + " nghìn " + call_number(s[1:], ok1, ok2)
    if len(s) == 5:
        if s[0] == '0':
            if ok2:
                return  call_number(s[1:], ok1, ok2)
            else:
                return " không " + call_number(s[1:], ok1, ok2)
        else:
            return dict_number[s[0]+'0'] + " nghìn " + call_number(s[1:], ok1, ok2)
    if len(s) == 6:
        if s[0] == '0':
            if ok2:
                return " không trăm " + call_number(s[1:], ok1, ok2)
            else:
                return " không " + call_number(s[1:], ok1, ok2)
        else:
            return dict_number[s[0]] + " trăm nghìn " + call_number(s[1:], ok1, ok2)
    res = ""
    for ss in s:
        res = res + dict_number[ss]
    return res


def acronym_to_word(sentence):
    dict = {'0': " không", '1': " một", '2': " hai", '3': " ba", '4': " bốn", '5': " năm", '6': " sáu", '7': " bẩy",
            '8': " tám", '9': " chín"
            , '/': " ", '.': "", '%': " phần trăm", '-': " ", ',': " ", '.': ""}
        # , '/': " trên ", '.': " chấm ", '%': " phần trăm", '-': " gach ngang ", ',': " phẩy ", '.': " chấm "}
    dict_word = {'TS': "tiến sĩ", 'GS': "giáo sư", 'HS': "học sinh", "TPHCM": "thành phố Hồ Chí Minh", "ĐH": "đại học",
                 "THCS": "trung học cơ sở", "THPT": "trung học phổ thông", "LHS": "lưu học sinh",
                 "GD": "giáo dục", "ĐT": "đào tạo", "SV": "sinh viên", "UBND": "ủy ban nhân dân",
                 "NLĐ": "người lao động", "CLB": "câu lạc bộ", "NV": "nhân viên", "KV1": "khu vực một",
                 "KV2": "khu vực hai", "KV3": "khu vực ba", "ĐHDL": "đại học dân lập", "TP": "thành phố",
                 "GV": "giáo viên", "TP": "thành phố",
                 "I": "một", "II": "hai", "CĐ": "cao đẳng", "ThS": "thạc sĩ", "KHXH": "khoa học xã hội",
                 "SGK": "sách giáo khoa",
                 "VN": "Việt Nam", "KT": "kinh tế", "XH": "xã hội", "TTXVN": "thông tấn xã Việt Nam", "HN": "Hà Nội",
                 "QH": "quốc hội",
                 "BS": "bác sĩ", "km": "ki lô mét", "cm": "xen ti mét", "gd": "giáo dục", "đt": "đào tạo",
                 "vn": "Việt Nam", "ha": "héc ta",
                 "Q1": "quận nhất", "Q2": "quận hai", "Q3": "quận ba", "Q4": "quận bốn", "Q5": "quận năm",
                 "Q6": "quận sáu", "Q7": "quận bẩy",
                 "Q": "quận", "Q9": "quận chín", "Q10": "quận mười", "HIV/AIDS": "H I V AIDS", "m2": "mét vuông",
                 "m3": "mét khối", "kwh": "ki lô goắt giờ",
                 "m": "mét", "mm": "mi li mét", "P1": "phường một", "P2": "phường hai", "P3": "phường ba",
                 "P4": "phường bốn", "x": "nhân",
                 "LDBĐ": "liên đoàn bóng đá", "+": "cộng"}

    # nếu thuộc dict kia thì thay thế, nếu là từ viết tắt thì tách ra , ví dụ như VN thì tách thành V N để hiểu là hai chữ riêng để đọc
    list = sentence.splitlines()
    # dd = 0
    # len(luu_) = 0
    number_sentences = 0
    pri = ""
    sentences=""
    def w_(s):
        if s in dict:           
            return dict[s]
        else:        
            return s

    for l in list:
        #print("cau : " + l)
        dd = 0
        luu = ''
        l.replace("/", " / ")
        words = l.split(' ')
        pri = ""
        pre_word_is_number = False
        word_after_pre_word=False
        for word in words:
            accepted_word = True
            dem = 0
            luu_c = ""
            is_number = False
            is_dv = False
            dv = ""
            if pre_word_is_number and word in div_dv2:
                pri = pri + " " + div_dv2[word] + " "
                pre_word_is_number = False
                word_after_pre_word=True
                continue            
            if pre_word_is_number and not(word in div_dv2):                
                pri = pri + " " + word
                pre_word_is_number = False
                word_after_pre_word=True
                continue
            if word in dict_word:
                pri = pri + " " + dict_word[word] + " "                
                continue
            pre_word_is_number = False
            for s in word:
                pre = 0
                dem += 1
                if s == '\\' or ord(s) >= 8220:
                    continue
                if (s <= '9' and s >= '0'):
                    is_number = True
                    luu_c += s
                    if is_dv:
                        if dv in dict_dv:
                            pri = pri + dict_dv[dv]
                            # _out.write(dict_dv[dv])
                        is_dv = False
                        dv = ""
                    pre_word_is_number = True
                else:
                    if is_number:
                        try:
                            pri = pri + " " + call_number(luu_c, 0, 0)                            
                            is_dv = True
                            dv = dv + s
                            is_number = False
                            luu_c = ""
                        except:
                            print("line: "+l+" error in word: "+word+" with character: "+s+"\r\n")
                if dem == len(word):
                    if is_number:
                        try:
                            pri = pri + " " + call_number(luu_c, 0, 0)
                        except:
                            print("line: "+l+" error in word: "+word+" with character: "+s+"\r\n")                       
                    if is_dv:
                        dv = dv + s
                        if dv in dict_dv:
                            pri = pri + dict_dv[dv]
                        is_dv = False
                        dv = ""
                if (ord(s) <= ord("Z") and ord(s) >= ord("A")) or ord(s) == ord('Đ') or ord(s) == ord('Ư'):
                    if dd == 1:                       
                        pri = pri + " " + s
                    else:                       
                        pri = pri + s
                        dd = 1
                    continue
                else:
                    dd = 0
                if not(pre_word_is_number):
                    if word_after_pre_word==False:                        
                        pri = pri + s
                    else:                       
                        pri = pri + " "+s
                        word_after_pre_word=False                                           
            pri = pri + " "        
        number_sentences = number_sentences + 1
        sentences=sentences+pri+" "      
    return sentences

# 
# with codecs.open("/home/hoangtrongbinh/HoangTrongBinh/NCKH-2020-Speech2Text/eagle_vnspeech2text/Binh/prepare_vocabs/TESTok.txt", "r", encoding= "utf8") as f_in:
#     sentences = f_in.read()
#     sentences=Date_to_word(sentences)
#     sentences= acronym_to_word(sentences)
#     f_dict = open("/home/hoangtrongbinh/HoangTrongBinh/NCKH-2020-Speech2Text/eagle_vnspeech2text/Binh/prepare_vocabs/fix_Text_small.txt", "w+",encoding="utf-8")
#     f_dict.write(sentences)
    # res=re.findall(r"\b[A-Za-z]+\b", sentences)
    # print(res)
    
 






