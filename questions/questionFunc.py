from flask import jsonify
from textblob import TextBlob

from questions.removeWord import removeWord


def questionFunc(ww2):
    ww2b = TextBlob(ww2)
    sposs = {}
    questionArray = []

    for sentence in ww2b.sentences:

        # We are going to prepare the dictionary of parts-of-speech as the key and value is a list of words:
        # {part-of-speech: [word1, word2]}
        # We are basically grouping the words based on the parts-of-speech
        poss = {}
        sposs[sentence.string] = poss;
        for t in sentence.tags:
            tag = t[1]
            if tag not in poss:
                poss[tag] = []
            poss[tag].append(t[0])

    for sentence in sposs.keys():
        poss = sposs[sentence]
        (word, sentence, replaced) = removeWord(sentence, poss)
        if replaced is None:
            print("Founded none for ")
            print(sentence)
        else:
            question = {
                "question": replaced,
                "answer": word
            }
            questionArray.append(question)
    response = jsonify(questionArray)
    response.status_code = 200
    return response
