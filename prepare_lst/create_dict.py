import os, sys

in_folder = sys.argv[1]
out_folder = sys.argv[2]
os.makedirs(out_folder, exist_ok=True)
f_result = os.path.join(out_folder, "dict.txt")
f_result = open(f_result, "w+", encoding="UTF-8")
files = os.listdir(in_folder)
dict_words = list()
for file in files:
    if file.__contains__(".lst"):
        f_in = os.path.join(in_folder, file)
        data = open(f_in, "r").readlines()
        for line in data:
            pieces = line.rstrip().split("\t")[3].split(" ")
            for piece in pieces:
                if piece not in dict_words:
                    dict_words.append(piece)
dict_words.sort()
for word in dict_words:
    f_result.write(word+"\n")