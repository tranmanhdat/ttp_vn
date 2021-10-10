import os, sys

in_folder = sys.argv[1]
out_folder = sys.argv[2]
os.makedirs(out_folder, exist_ok=True)
f_result = os.path.join(out_folder, in_folder.split("/")[-1]+".txt")
f_result = open(f_result, "w+", encoding="UTF-8")
files = os.listdir(in_folder)
for file in files:
    f_in = os.path.join(in_folder, file)
    data = open(f_in, "r").readlines()
    sum = 0
    for line in data:
        if len(line.rstrip()) > 10:
            piece = line.rstrip().split("\t")[2]
            sum = sum + float(piece)
    f_result.write(str(file)+"\t"+str(round(sum/3600,2))+"\n")
