import os, sys

in_folder = sys.argv[1]
out_folder = sys.argv[2]
os.makedirs(out_folder, exist_ok=True)
f_in_1 = os.path.join(in_folder, "new_voice.lst")
data_1 = open(f_in_1, "r").readlines()
i = 1
for i in range(1, 26):
    if i in [4, 11, 14, 18, 22, 25]:
        continue
    if i < 10:
        folder_name = "P0" + str(i)
    else:
        folder_name = "P" + str(i)
    f_out = os.path.join(out_folder, "new_voice_" + str(i) + ".lst")
    f_w = open(f_out, "w+", encoding="UTF-8")
    for line in data_1:
        if len(line.rstrip()) > 10:
            piece = line.rstrip().split("\t")[1].split("/")[-4]
            if piece == folder_name:
                f_w.write(line.rstrip() + "\n")
    f_w.close()
