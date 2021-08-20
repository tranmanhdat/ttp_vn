import os, sys

in_folder = sys.argv[1]
out_folder = sys.argv[2]
os.makedirs(out_folder, exist_ok=True)

dict_words = dict()

f_1_text = os.path.join(in_folder, "1_text.txt")
f_1_text = open(f_1_text, "r", encoding="UTF-8")
f_1_dict = os.path.join(in_folder, "1_dict.txt")
f_1_dict = open(f_1_dict, "r", encoding="UTF-8")

for line in f_1_dict.readlines():
    elements = line.rstrip().split("\t")
    dict_words[elements[0]] = int(elements[1])

f_2_text = os.path.join(out_folder, "2_text.txt")
f_2_text = open(f_2_text, "w+", encoding="UTF-8")
f_2_dict = os.path.join(out_folder, "2_dict.txt")
f_2_dict = open(f_2_dict, "w+", encoding="UTF-8")

data = f_1_text.readlines()
for line in data:
    text = line.rstrip()
    words = text.split(" ")
    save = False
    for word in words:
        if dict_words[word] <= 10:
            save = True
    if save:
        f_2_text.write(text+"\n")
    else:
        for word in words:
            dict_words[word] = dict_words[word] - 1
sorted_dict_words = sorted(dict_words.items(), key=lambda item: item[1])
for key, value in sorted_dict_words:
    f_2_dict.write(str(key)+"\t"+str(value)+"\n")