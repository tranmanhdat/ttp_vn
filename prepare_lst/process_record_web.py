import os, sys

in_folder = sys.argv[1]
out_folder = sys.argv[2]
os.makedirs(out_folder, exist_ok=True)
f_in_1 = os.path.join(in_folder, "data_record_web.lst")
data_1 = open(f_in_1, "r").readlines()
i = 1
data = {}
tmp = []
for line in data_1:
    if len(line.rstrip()) > 10:
        piece = line.rstrip().split("\t")[1].split("/")[-1].split("_")[0]
        if piece in data:
            tmp = data[piece]
            tmp = tmp + [line.rstrip()]
            data[piece] = tmp
        else:
            data[piece] = [line.rstrip()]
for key, lines in data.items():
    f_out = os.path.join(out_folder, "record_web_" + key + ".lst")
    f_w = open(f_out, "w+", encoding="UTF-8")
    for line in lines:
        f_w.write(line+"\n")