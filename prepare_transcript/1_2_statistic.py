import os, sys

in_folder = sys.argv[1]
out_folder = sys.argv[2]
f_dict = os.path.join(out_folder, "1_statistic.txt")
f_dict = open(f_dict, "w+", encoding="UTF-8")
dict_words = dict()
f_dict_org = open("prepare_transcript/dictionary/dict_092021.txt", "r", encoding="UTF-8")
dict_org = []
data = f_dict_org.readlines()
for line in data:
    dict_org.append(line.rstrip())
    dict_words[dict_org[-1]] = 0
print(len(dict_org))
files = os.listdir(in_folder)
out_of_dict = []
for file in files:
    if file.__contains__(".lst"):
        if file.__contains__("command"):
            continue
        f_in = os.path.join(in_folder, file)
        data = open(f_in, "r").readlines()
        for line in data:
            text = line.rstrip().split("\t")[3]
            words = list(filter(None,text.split(" ")))
            if len(words)>2:
                save = True
                for word in words:
                    if word not in dict_words:
                        if word not in out_of_dict:
                            out_of_dict.append(word)
                        print(word)
                        print(text)
                        save = False
                        break
                if save:
                    for word in words:
                            dict_words[word] = dict_words[word] + 1
sorted_dict_words = sorted(dict_words.items(), key=lambda item: item[1])
for key, value in sorted_dict_words:
    f_dict.write(str(key)+"\t"+str(value)+"\n")