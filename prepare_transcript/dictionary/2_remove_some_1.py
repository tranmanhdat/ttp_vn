import os
import locale
locale.setlocale(locale.LC_COLLATE, 'vi_VN')
if __name__ == '__main__':
    f_read = open("prepare_transcript/dictionary/data_merger/dict_u.txt", "r", encoding="UTF-8")
    dict_full = []
    data_dict = f_read.readlines()
    need_remove = ["aic", "aich", "aim","ain", "aing", "ainh", "aip", "ait","aom", "aonh", "aong","aop", "aot",
                   "aoc", "aoch", "aon",
                   "eoch","eoc","eon","eom","eop",
                   "iach","iung", "iat","iac", "iêc", "iuc", "iuch","iup","iut", "iunh","iap",
                   "oic", "oin", "oim","oip","oem","oech","oeng","oec","oit",
                   "ôic","ôit", "ôip","ôim","ôin",
                   "ơic","ơit","ơin","ơim","ơin","ơip",
                   "uic", "uat","uip","uit","uâp","uâch","uin","uim","uach","uam",
                   "ưat", "ưan", "ưam","ưut", "ưup", "ưum", "ưun","ưic", "ưac","ưit","ưip","ưim","ưing","ưap","ưin",
                   "ươch","ườch","ưởch","ưỡch","ướch","ượch",
                   "êuc", "êup", "êut", "êun", "êum", "êuch"]
    need_remove_extend_dau = []
    van_don_gian_1 = []
    van_don_gian_1_file = open("prepare_transcript/dictionary/data_merger/van_don_gian_1.txt", "r", encoding="UTF-8")
    data = van_don_gian_1_file.readlines()
    for line in data:
        van_don_gian_1.append(line.rstrip())
    # print(van_don_gian_1)
    dict_dau = {}
    for i in range(0, len(van_don_gian_1)):
        if i % 6 == 0:
            dict_dau[van_don_gian_1[i]] = []
        else:
            tmp = dict_dau[van_don_gian_1[(i // 6) * 6]]
            tmp.append(van_don_gian_1[i])
            dict_dau[van_don_gian_1[(i // 6) * 6]] = tmp
    dict_dau["â"] = ['ấ', 'ầ', 'ẫ', 'ẩ', 'ậ']
    dict_dau["ă"] = ['ắ', 'ằ', 'ẵ', 'ặ', 'ẳ']
    # print(dict_dau)
    for word in need_remove:
        need_remove_extend_dau.append(word)
        if word[0] in dict_dau.keys():
            list_dau = dict_dau[word[0]]
            for middle_character in list_dau:
                need_remove_extend_dau.append(middle_character+word[1:])
    # print(need_remove_extend_dau)
    for word in data_dict:
        word = word.rstrip()
        save = True
        for case in need_remove_extend_dau:
            if word.__contains__(case):
                save = False
        if save:
            dict_full.append(word)
    dict_full_last = sorted(dict_full, key=locale.strxfrm)
    f_write = open("prepare_transcript/dictionary/data_merger/dict_u_2.txt", "w+", encoding="UTF-8")
    for word in dict_full_last:
        f_write.write(word + "\n")
    f_write.close()
    # f_write = open("prepare_transcript/dictionary/data_merger/dict_2_1.txt", "w+", encoding="UTF-8")
    # for word in dict_full_last[:int(0.25*len(dict_full_last))]:
    #     f_write.write(word+"\n")
    # f_write.close()
    # f_write = open("prepare_transcript/dictionary/data_merger/dict_2_2.txt", "w+", encoding="UTF-8")
    # for word in dict_full_last[int(0.25 * len(dict_full_last)):int(0.5 * len(dict_full_last))]:
    #     f_write.write(word + "\n")
    # f_write.close()
    # f_write = open("prepare_transcript/dictionary/data_merger/dict_2_3.txt", "w+", encoding="UTF-8")
    # for word in dict_full_last[int(0.5 * len(dict_full_last)):int(0.75 * len(dict_full_last))]:
    #     f_write.write(word + "\n")
    # f_write.close()
    # f_write = open("prepare_transcript/dictionary/data_merger/dict_2_4.txt", "w+", encoding="UTF-8")
    # for word in dict_full_last[int(0.75 * len(dict_full_last)):]:
    #     f_write.write(word + "\n")
    # f_write.close()