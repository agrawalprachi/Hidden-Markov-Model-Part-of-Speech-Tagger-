import sys
from math import log10

transition = {}
emission = {}
unique_tags = {}
unique_tags_count = {}
unique_words = set()

infile = sys.argv[1]

with open("hmmmodel.txt") as f:
    for line in f:
        elements = line.split(" ")
        type_of_prob = elements[0]
        wordtag = elements[1]
        prob = float(elements[2])

        if type_of_prob == "T":
            transition[wordtag] = prob
            tags = wordtag.split("/")

        if type_of_prob == "E":
            emission[wordtag] = prob
            word_tag_set = wordtag.rsplit("/")
            unique_words.add(word_tag_set[0])

        if type_of_prob == "C":
            unique_tags[wordtag] = 1
            unique_tags_count[wordtag] = prob


ofile = open("hmmoutput.txt", "w")

with open(infile, "r") as testfile:
    for line in testfile:
        words = line.split(" ")
        words = [word.strip() for word in words]
        l = len(words)
        best_score = {}
        best_edge = {}
        for tag in unique_tags:

            if words[0] not in unique_words:
                em = 1
            else:
                em = 0 if words[0] + "/" + tag not in emission else emission[words[0] + "/" + tag]

            if "<s>" + "/" + tag not in transition:
                tr = 1/(len(unique_tags)+ unique_tags_count["<s>"])
            else:
                tr = transition["<s>" + "/" + tag]

            best_score[(tag, words[0], 0)] = tr*em
            best_edge[(tag, words[0], 0)] = "<s>"

        for i in range(1, len(words)):
            for current_tag in unique_tags:
                temp = 0

                if words[i] in unique_words and words[i] + "/" + current_tag not in emission:
                    best_score[(current_tag, words[i], i)] = 0
                    continue

                for prev_tag in unique_tags:

                    if words[i] not in unique_words:
                        em = 1
                    else:
                        em = 0 if words[i] + "/" + current_tag not in emission else emission[words[i] + "/" + current_tag]

                    if prev_tag + "/" + current_tag not in transition:
                        tr = 1 / (len(unique_tags) + unique_tags_count[prev_tag])
                    else:
                        tr = transition[prev_tag+"/"+current_tag]

                    score = best_score[(prev_tag, words[i-1], i-1)]*tr*em
                    best_score[(current_tag, words[i], i)] = temp

                    if temp < score:
                       temp = score
                       best_score[(current_tag, words[i], i)] = score
                       best_edge[(current_tag, words[i],i)] = prev_tag

        last_best_score = 0
        best_last_tag = None

        total_words = len(words)
        for tag in unique_tags:
            if  best_score[(tag, words[-1], total_words-1)]>last_best_score:
                last_best_score = best_score[(tag, words[-1], total_words-1)]
                best_last_tag = tag

        answer_tags = []
        answer_tags.append(best_last_tag)

        for i in range(len(words)-2,-1,-1):
            answer_tags.append(best_edge[(best_last_tag, words[i+1], i+1)])
            best_last_tag = best_edge[(best_last_tag, words[i+1], i+1)]

        answer_tags.reverse()

        answer_sentence = ""
        for j in range(0, l):
            answer_sentence = answer_sentence + words[j] + "/" + answer_tags[j]
            if j != l-1:
                answer_sentence = answer_sentence + " "
        answer_sentence = answer_sentence + "\n"
        ofile.write(answer_sentence)

ofile.close()
testfile.close()