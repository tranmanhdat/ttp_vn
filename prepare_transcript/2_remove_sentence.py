import os, sys
from random import shuffle
in_folder = sys.argv[1]
out_folder = sys.argv[2]
os.makedirs(out_folder, exist_ok=True)

dict_words = dict()

f_1_text = os.path.join(in_folder, "2_0_text_splited.txt")
f_1_text = open(f_1_text, "r", encoding="UTF-8")
f_1_dict = os.path.join(in_folder, "1_dict.txt")
f_1_dict = open(f_1_dict, "r", encoding="UTF-8")

for line in f_1_dict.readlines():
    elements = line.rstrip().split("\t")
    dict_words[elements[0]] = 0

f_2_text = os.path.join(out_folder, "2_text.txt")
f_2_text = open(f_2_text, "w+", encoding="UTF-8")
f_2_dict = os.path.join(out_folder, "2_dict.txt")
f_2_dict = open(f_2_dict, "w+", encoding="UTF-8")

text_2 = []
data = f_1_text.readlines()
# shuffle(data)
data = sorted(data, key=lambda x: len(x.split(" ")), reverse=True)
number_words = 0
for line in data:
    text = line.rstrip()
    words = list(filter(None,text.split(" ")))
    # if len(words)>60:
    #     continue
    save = False
    for word in words:
        if dict_words[word] < 6:
            save = True
    if save:
        number_words += len(words)
        text_2.append(text)
        # f_2_text.write(text+"\n")
        for word in words:
            dict_words[word] = dict_words[word] + 1
sorted_dict_words = sorted(dict_words.items(), key=lambda item: item[1])
print(len(text_2))
print(number_words)
print(number_words/12000)
for key, value in sorted_dict_words:
    f_2_dict.write(str(key)+"\t"+str(value)+"\n")
text_2 = sorted(text_2, key=lambda item: len(item.split(" ")))
for text in text_2:
    f_2_text.write(text+"\n")