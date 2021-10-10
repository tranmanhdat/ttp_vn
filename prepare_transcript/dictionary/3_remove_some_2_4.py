import os
import locale
locale.setlocale(locale.LC_COLLATE, 'vi_VN')
if __name__ == '__main__':
    f_read = open("prepare_transcript/dictionary/data_merger/dict_2_4_in_check.txt", "r", encoding="UTF-8")
    dict_full = []
    data_dict = f_read.readlines()
    need_remove = ["ãc", "àc", "ãp", "àt", "ảt","àp", "ảp",
                   "òenh", "ỏenh","õenh", "óenh", "ọenh", "oep", "òep","ỏep","õep",
                   "ỏet", "õet", "ỏenh", "õenh", "óenh", "ọenh", "oep", "òep", "òep", "õep","ỏep", "ọep",
                   "oep", "óep", "òep", "õep", "ọep", "ỏep","oet", "òet", "ỏet", "õet",
                   "op", "òp", "õp", "ỏp","ot", "õt", "òt", "ỏt","ồc", "ỗc", "ổc",
                   "ồp", "ổp", "ỗp","ôp","ôt", "ồt", "ỗt", "ổt",
                   "ơp","ờp","ỡp", "ởp","ơt","ờt","ởt", "ỡt","uac", "ùac", "ũac","ụac", "ủac",
                   "uan", "úan","ùan", "ũan", "ụan","uap", "ùap", "úap", "ũap", "ụap", "ủap",
                   "uâc", "ùâc", "ũâc", "ũâc","uầch", "uẩch", "uẫch", "uấch", "uậch",
                   "uầp","uẩp","uẫp","uât", "uầt", "uẩt","uẫt","uc", "ùc", "ũc", "ủc",
                   "uêc", "ùêc","ủêc", "ũêc","uêch","ùêch","ủêch", "ũêch","uêng", "ùêng","úêng", "ũêng", "ủêng",'ụêng',
                   "uêp", "ùêp", "ủêp", "ũêp", "ụêp", "uêt", "ùêt", "ũêt", "ủêt", "uôc", "uôch", "ùt","ủt", "ũt",
                   "uyp", "ùyp", "ũyp", "ủyp","ươnh","ừơnh", "ứơnh", "ữơnh", "ửơnh", "ựơnh","yêc",
                   "yềc", "yểc", "yễc", "êp", "ểp", "ễp", "ềp","êt", "ềt", "ểt", "ễt","oănh", "oăp", "oằp", "oẳp", "oẳp",
                   "oăt", "oằt", "oẳt", "oẵt"]
    # print(need_remove_extend_dau, ")
    for word in data_dict:
        word = word.rstrip()
        save = True
        for case in need_remove:
            if word.__contains__(case):
                save = False
        if save:
            dict_full.append(word)
    dict_full_last = sorted(dict_full, key=locale.strxfrm)
    f_write = open("prepare_transcript/dictionary/data_merger/dict_2_4_in_check_1.txt", "w+", encoding="UTF-8")
    for word in dict_full_last:
        f_write.write(word + "\n")
    f_write.close()