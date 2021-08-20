import os, sys

in_folder = sys.argv[1]
out_folder = sys.argv[2]
os.makedirs(out_folder, exist_ok=True)
f_result = os.path.join(out_folder, "1_text.txt")
f_result = open(f_result, "w+", encoding="UTF-8")
f_dict = os.path.join(out_folder, "1_dict.txt")
f_dict = open(f_dict, "w+", encoding="UTF-8")
files = os.listdir(in_folder)
dict_words = dict()
for file in files:
    if file.__contains__(".lst"):
        f_in = os.path.join(in_folder, file)
        data = open(f_in, "r").readlines()
        for line in data:
            text = line.rstrip().split("\t")[3]
            words = text.split(" ")
            if len(words)>5:
                f_result.write(text+"\n")
                for word in words:
                    if word not in dict_words:
                        dict_words[word] = 1
                    else:
                        dict_words[word] = dict_words[word] + 1
sorted_dict_words = sorted(dict_words.items(), key=lambda item: item[1])
for key, value in sorted_dict_words:
    f_dict.write(str(key)+"\t"+str(value)+"\n")