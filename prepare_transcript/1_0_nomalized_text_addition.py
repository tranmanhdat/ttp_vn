import os, sys
data = open("prepare_transcript/data/addition_text.txt", "r", encoding="UTF-8").readlines()
data_out = open("prepare_transcript/data/addition_text.txt", "w+", encoding="UTF-8")
for line in data:
    data_out.write(line.lower())