import os, sys

in_folder = sys.argv[1]
out_folder = sys.argv[2]
os.makedirs(out_folder, exist_ok=True)
f_in_1 = os.path.join(in_folder, "data_record_disabled.lst")
data_1 = open(f_in_1, "r").readlines()
f_in_2 = os.path.join(in_folder, "voice.lst")
data_2 = open(f_in_2, "r").readlines()
f_in_3 = os.path.join(in_folder, "new_voice.lst")
data_3 = open(f_in_3, "r").readlines()
arr_disabled, arr_voice, arr_new_voice = ["empty"] * 58, ["empty"] * 58, ["empty"] * 58
for i in range(30):
    if i < 10:
        arr_disabled[i] = "A00" + str(i)
    else:
        arr_disabled[i] = "A0" + str(i)
arr_voice[1] = "P04"
arr_voice[8] = "P11"
arr_voice[12] = "P14"
arr_voice[14] = "P18"
arr_voice[18] = "P22"
arr_voice[24] = "P25"
arr_voice[30:49] = ["P24", "P23", "P21", "P20", "P19", "P17", "P16", "P15", "P13", "P12", "P10", "P09", "P08", "P07",
                  "P06", "P05", "P03", "P02", "P01"]
arr_new_voice[5] = "A006"
arr_new_voice[8] = "A015"
arr_new_voice[9] = "A001"
arr_new_voice[10] = "A023"
arr_new_voice[12] = "A005"
arr_new_voice[14] = "A018"
arr_new_voice[19] = "A022"
arr_new_voice[22] = "A024"
arr_new_voice[24] = "A025"
arr_new_voice[31] = "A021"
arr_new_voice[37] = "A019"
arr_new_voice[38] = "A008"
arr_new_voice[39] = "A016"
arr_new_voice[41] = "A012"
arr_new_voice[44] = "A011"
arr_new_voice[46] = "A020"
arr_new_voice[49:] = ["A002", "A003", "A004", "A007", "A009", "A010", "A013", "A014", "A017"]
ignore_disabled = ["A003", "A005", "A007", "A008", "A012", "A013", "A016", "A023", "A024"]
ignore_voice = ["P18", "P25", "P24", "P23", "P21", "P17", "P16", "P12"]
ignore_new_voice = ["A006", "A011"]
f_statistic = os.path.join(out_folder, "statistic.txt")
f_write = open(f_statistic, "w+", encoding="UTF-8")
i = 1
for i in range(0, 58):
    f_out = os.path.join(out_folder, "speaker_" + str(i) + ".lst")
    f_w = open(f_out, "w+", encoding="UTF-8")
    count = 0
    sum = 0
    for line in data_1:
        if len(line.rstrip()) > 10:
            piece = line.rstrip().split("\t")[1].split("/")[-3]
            if piece == arr_disabled[i] and piece not in ignore_disabled:
                f_w.write(line.rstrip() + "\n")
                count = count + 1
                sum = sum + float(line.rstrip().split("\t")[2])
    for line in data_2:
        if len(line.rstrip()) > 10:
            piece = line.rstrip().split("\t")[1].split("/")[-4]
            if piece == arr_voice[i] and piece not in ignore_voice:
                f_w.write(line.rstrip() + "\n")
                count = count + 1
                sum = sum + float(line.rstrip().split("\t")[2])
    for line in data_3:
        if len(line.rstrip()) > 10:
            piece = line.rstrip().split("\t")[1].split("/")[-3]
            if piece == arr_new_voice[i] and piece not in ignore_new_voice:
                f_w.write(line.rstrip() + "\n")
                count = count + 1
                sum = sum + float(line.rstrip().split("\t")[2])
    f_w.close()
    f_write.write("{}\t{}\t{:.2f}\n".format(f_out, count, sum/3600))
f_write.close()