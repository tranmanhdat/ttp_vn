import codecs
import time
if __name__ == '__main__':
    full_text = "Binh/prepare_vocabs/corpus-full_processed.txt"
    step_sentences = 100000
    dictionary_word = {}
    with open(full_text, "r") as f_in:
        i = 0
        start = time.time()
        for line in f_in:
            words = line.rstrip().split(' ')
            for word in words:
                if word == '.':
                    continue
                if word not in dictionary_word:
                    dictionary_word[word] = 1
                else:
                    dictionary_word[word] = dictionary_word[word] + 1
            i = i + 1
            if i%step_sentences==0:
                end = time.time()
                print("processed from {} to {} take {:.2f}".format(
                    i - step_sentences, i, end - start))
                start = end
    with codecs.open("Binh/prepare_vocabs/frequency.txt", "w+", encoding="utf-8") as f_out:
        f_dict = open("Binh/prepare_vocabs/dictionary.txt", "w+", encoding="utf-8")
        for word in sorted(dictionary_word, key=dictionary_word.get,
                           reverse=True):
            f_out.write(word + '\t' + str(dictionary_word[word]) + '\r\n')
            f_dict.write(word + "\r\n")