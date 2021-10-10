import os, sys
import locale
locale.setlocale(locale.LC_COLLATE, 'vi_VN')
if __name__ == '__main__':
    path_file = sys.argv[1]
    f_dict = open(path_file, "r", encoding="UTF-8")
    data = f_dict.readlines()
    dict_org = []
    for line in data:
        dict_org.append(line.rstrip())
    dict_full_last = sorted(dict_org, key=locale.strxfrm)
    f_dict_sorted = open(path_file, "w+", encoding="UTF-8")
    for word in dict_full_last:
        f_dict_sorted.write(word+"\n")
    f_dict_sorted.close()