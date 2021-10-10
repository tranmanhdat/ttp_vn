import os, sys
from random import shuffle
in_folder = sys.argv[1]
out_folder = sys.argv[2]
os.makedirs(out_folder, exist_ok=True)

dict_words = dict()

f_1_text = os.path.join(in_folder, "1_text.txt")
f_1_text = open(f_1_text, "r", encoding="UTF-8")

f_2_text = os.path.join(out_folder, "2_0_text_splited.txt")
f_2_text = open(f_2_text, "w+", encoding="UTF-8")
text_2 = []
data = f_1_text.readlines()
for line in data:
    text = line.rstrip()
    words = list(filter(None,text.split(" ")))
    if len(words)>30:
        number = int(len(words)/15)-1
        for i in range(0,number):
            text_2.append(" ".join(words[i*15:(i+1)*15]))
        text_2.append(" ".join(words[number*15:]))
    else:
        text_2.append(" ".join(words))
text_2 = sorted(text_2, key=lambda item: len(item.rstrip().split(" ")))
for text in text_2:
    f_2_text.write(text+"\n")