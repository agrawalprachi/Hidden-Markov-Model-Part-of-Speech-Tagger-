import sys

total_tag = {}
transition = {}
emission = {}
total_transition_tag = {}

infile = sys.argv[1]
ofile = open("hmmmodel.txt", "w")

with open(infile) as f:
    for line in f:
        previous = "<s>"
        if previous.strip() in total_tag:
            total_tag[previous.strip()] += 1
            total_transition_tag[previous.strip()] +=1
        else:
            total_tag[previous.strip()] = 1
            total_transition_tag[previous.strip()] = 1

        wordtags = line.split(" ")
        for wordtag in wordtags:
            wordandtag = wordtag.split("/")
            wordtag = wordtag.strip()
            tag = wordandtag[-1]
            tag = tag.strip()

            if wordtag != wordtags[-1]:
                if tag in total_transition_tag:
                    total_transition_tag[tag] += 1
                else:
                    total_transition_tag[tag] = 1

            if previous+"/"+tag in transition:
                transition[previous+"/"+tag] += 1
            else:
                transition[previous + "/" + tag] = 1

            if tag in total_tag:
                total_tag[tag] += 1
            else:
                total_tag[tag] = 1

            if wordtag in emission:
                emission[wordtag] += 1
            else:
                emission[wordtag] = 1

            previous = tag

emission_prob = {}
transition_prob = {}

for key, value in transition.items():
    previous_and_tag = key.split("/")
    previous = previous_and_tag[0]
    tag = previous_and_tag[1]
    transition_prob[key] = (1+value)/(total_transition_tag[previous] + len(total_tag))
    ofile.write("T "+ key+" "+str(transition_prob[key])+"\n")

for key, value in emission.items():
    word_and_tag = key.split("/")
    tag = word_and_tag[-1]
    emission_prob[key] = value/total_tag[tag]
    ofile.write("E " + key + " " + str(emission_prob[key]) + "\n")

for key, value in total_tag.items():
    if key in total_transition_tag:
        ofile.write("C " + key + " " + str(total_transition_tag[key]) + "\n")
    else:
        ofile.write("C " + key + " " + str(value) + "\n")


