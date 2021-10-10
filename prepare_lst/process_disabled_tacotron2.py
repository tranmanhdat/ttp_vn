import os, sys

in_folder = sys.argv[1]
out_folder = sys.argv[2]
os.makedirs(out_folder, exist_ok=True)
f_in_1 = os.path.join(in_folder, "data_record_disabled.lst")
data = open(f_in_1,"r").readlines()
train_ratio = 0.8
train_index = int(train_ratio * len(data))
with open(os.path.join(out_folder, 'training.txt'), 'w') as fd:
    for i, fname in enumerate(data[:train_index]):
        line = data[i].rstrip()
        if len(line)<2:
            continue
        elements = line.split("\t")
        fd.write('{}|{}\n'.format( elements[1], elements[3]))
with open(os.path.join(out_folder,'testing.txt'), 'w') as fd:
    for i, fname in enumerate(data[train_index:]):
        line = data[i].rstrip()
        if len(line) < 2:
            continue
        elements = line.split("\t")
        fd.write('{}|{}\n'.format(elements[1], elements[3]))