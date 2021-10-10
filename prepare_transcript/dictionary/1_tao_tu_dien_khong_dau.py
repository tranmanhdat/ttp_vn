import os, sys
import locale
locale.setlocale(locale.LC_COLLATE, 'vi_VN')
if __name__ == '__main__':
    path_folder = sys.argv[1]
    phu_am_dau = []
    phu_am_dau_file = os.path.join(path_folder, "phu_am_dau.txt")
    phu_am_dau_file = open(phu_am_dau_file,"r",encoding="UTF-8")
    data = phu_am_dau_file.readlines()
    for line in data:
        phu_am_dau.append(line.rstrip())
    print(phu_am_dau)
    phu_am_cuoi = []
    phu_am_cuoi_file = os.path.join(path_folder, "phu_am_cuoi.txt")
    phu_am_cuoi_file = open(phu_am_cuoi_file, "r", encoding="UTF-8")
    data = phu_am_cuoi_file.readlines()
    for line in data:
        phu_am_cuoi.append(line.rstrip())
    print(phu_am_cuoi)
    van_don_gian_1 = []
    van_don_gian_1_file = os.path.join(path_folder, "van_don_gian_1.txt")
    van_don_gian_1_file = open(van_don_gian_1_file, "r", encoding="UTF-8")
    data = van_don_gian_1_file.readlines()
    for line in data:
        van_don_gian_1.append(line.rstrip())
    print(van_don_gian_1)
    van_don_gian_2 = []
    van_don_gian_2_file = os.path.join(path_folder, "van_don_gian_2.txt")
    van_don_gian_2_file = open(van_don_gian_2_file, "r", encoding="UTF-8")
    data = van_don_gian_2_file.readlines()
    for line in data:
        van_don_gian_2.append(line.rstrip())
    print(van_don_gian_2)
    van_hoa_am = []
    van_hoa_am_file = os.path.join(path_folder, "van_hoa_am.txt")
    van_hoa_am_file = open(van_hoa_am_file, "r", encoding="UTF-8")
    data = van_hoa_am_file.readlines()
    for line in data:
        van_hoa_am.append(line.rstrip())
    print(van_hoa_am)
    van_hop_am = []
    van_hop_am_file = os.path.join(path_folder, "van_hop_am.txt")
    van_hop_am_file = open(van_hop_am_file, "r", encoding="UTF-8")
    data = van_hop_am_file.readlines()
    for line in data:
        van_hop_am.append(line.rstrip())
    print(van_hop_am)

    dict_dau = {}
    for i in range(0, len(van_don_gian_1)):
        if i%6==0:
            dict_dau[van_don_gian_1[i]] = []
        else:
            tmp = dict_dau[van_don_gian_1[(i//6)*6]]
            tmp.append(van_don_gian_1[i])
            dict_dau[van_don_gian_1[(i//6)*6]] = tmp
    dict_dau["â"] = ['ấ', 'ầ', 'ẫ', 'ẩ', 'ậ']
    dict_dau["ă"] = ['ắ', 'ằ', 'ẵ', 'ặ', 'ẳ']
    print(dict_dau)

    f_dict = os.path.join(path_folder, "dict.txt")
    f_dict = open(f_dict, "w+", encoding="UTF-8")

    dict_full = []
    # tu = van nguyen am
    dict_full = dict_full + van_don_gian_1
    # tu = phu am dau + van don gian 1
    for start_character in phu_am_dau:
        for end_character in van_don_gian_1:
            dict_full.append(start_character+end_character)
    # tu = phu am dau + van don gian 2 + dau
    for start_character in phu_am_dau:
        for end_character in van_don_gian_2:
            dict_full.append(start_character+end_character)
            list_dau = dict_dau[end_character[0]]
            for middle_character in list_dau:
                dict_full.append(start_character+middle_character+end_character[1:])
    # tu = phu am dau + van hoa am +-phu am cuoi + dau
    for start_character in phu_am_dau:
        for end_character in van_hoa_am:
            dict_full.append(start_character+end_character)
            list_dau = dict_dau[end_character[0]]
            for middle_character in list_dau:
                dict_full.append(start_character+middle_character+end_character[1:])
            for last_character in phu_am_cuoi:
                dict_full.append(start_character + end_character + last_character)
                list_dau = dict_dau[end_character[0]]
                for middle_character in list_dau:
                    dict_full.append(start_character + middle_character + end_character[1:]+ last_character)
    # tu = phu am dau + van hop am
    # loai 1 tu = phu am dau + 4 hop am dau
    for start_character in phu_am_dau:
        for end_character in van_hop_am[:4]:
            dict_full.append(start_character+end_character)
            list_dau = dict_dau[end_character[0]]
            for middle_character in list_dau:
                dict_full.append(start_character + middle_character + end_character[1:])
    #loai 2 tu = phu am dau +- nguyen am + 6 van hop am cuoi + phu am cuoi
    # loai 2.1 khong co nguyen am
    for start_character in phu_am_dau:
        for middle_character in van_hop_am[4:]:
            for end_character in phu_am_cuoi:
                dict_full.append(start_character+middle_character+end_character)
                list_dau = dict_dau[middle_character[1]]
                for dau_character in list_dau:
                    dict_full.append(start_character+middle_character[0]+dau_character+end_character)
    # loai 2.2 co nguyen am
    for start_character in phu_am_dau:
        for start_2_character in dict_dau.keys():
            for middle_character in van_hop_am[4:]:
                for end_character in phu_am_cuoi:
                    dict_full.append(start_character + middle_character + end_character)
                    list_dau = dict_dau[middle_character[1]]
                    for dau_character in list_dau:
                        dict_full.append(start_character + middle_character[0] + dau_character + end_character)

    dict_full_last = sorted(dict_full, key=locale.strxfrm)
    dict_full_last = list(dict.fromkeys(dict_full_last))
    for word in dict_full_last:
        f_dict.write(word+"\n")
    f_dict.close()