import sys, os

f_in_1 = sys.argv[1]
out_folder = sys.argv[2]
os.makedirs(out_folder, exist_ok=True)
data = open(f_in_1, "r").readlines()
train_ratio = 0.8
train_index = int(train_ratio * len(data))
train_time = 0
test_time = 0
f_wave = open(os.path.join(out_folder, 'train_files.txt'), 'w+')
with open(os.path.join(out_folder, 'training.txt'), 'w') as fd:
    for i, fname in enumerate(data[:train_index]):
        line = data[i].rstrip()
        if len(line)<2:
            continue
        elements = line.split("\t")
        train_time = train_time + float(elements[2])
        elements[1] = elements[1].replace("/speech_data/", "/speech_data_22050/")
        fd.write('{}|{}\n'.format( elements[1], elements[3]))
        f_wave.write('{}\n'.format( elements[1]))

with open(os.path.join(out_folder,'testing.txt'), 'w') as fd:
    for i, fname in enumerate(data[train_index:]):
        line = data[i].rstrip()
        if len(line) < 2:
            continue
        elements = line.split("\t")
        test_time = test_time + float(elements[2])
        elements[1] = elements[1].replace("/speech_data/", "/speech_data_22050/")
        fd.write('{}|{}\n'.format(elements[1], elements[3]))
        f_wave.write('{}\n'.format( elements[1]))

print(train_time, test_time)