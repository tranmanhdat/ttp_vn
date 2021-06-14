import os, sys

in_folder = sys.argv[1]
out_folder = sys.argv[2]
os.makedirs(out_folder, exist_ok=True)
f_in_1 = os.path.join(in_folder, "data_record_disabled.lst")
data_1 = open(f_in_1,"r").readlines()
f_in_2 = os.path.join(in_folder, "voice.lst")
data_2 = open(f_in_2,"r").readlines()
i = 1
for i in range(0, 30):
    if i<10:
        folder_name = "A00"+str(i)
    else:
        folder_name = "A0"+str(i)
    f_out = os.path.join(out_folder, "disabled_"+str(i)+".lst")
    f_w = open(f_out, "w+", encoding="UTF-8")
    for line in data_1:
        if len(line.rstrip())>10:
            piece = line.rstrip().split("\t")[1].split("/")[-3]
            if piece == folder_name:
                f_w.write(line.rstrip()+"\n")

    voice = ''
    if i==1:
        voice="P04"
    elif i==8:
        voice="P11"
    elif i==12:
        voice="P14"
    elif i==14:
        voice="P18"
    elif i==18:
        voice="P22"
    elif i==24:
        voice="P25"
    if len(voice)>1:
        for line in data_2:
            if len(line.rstrip()) > 10:
                piece = line.rstrip().split("\t")[1].split("/")[-4]
                if piece == voice:
                    f_w.write(line.rstrip() + "\n")
    f_w.close()
