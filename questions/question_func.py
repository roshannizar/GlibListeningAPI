from flask import jsonify
import csv
import nltk

from questions.remove_word import remove_word

# This was mainly used for hosting purpose.
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


def question_func(sentence):
    col_names = ["Question", "Answer"] # For dataset headers csv
    tSen = nltk.sent_tokenize(sentence)
    sposs = {}
    questionArray = [] # stores the extracted questions into array
    number = 0

    for sentence in tSen:
        # going to prepare the dictionary of parts-of-speech as the key and value is a list of words:
        # {part-of-speech: [word1, word2]}
        # basically grouping the words based on the parts-of-speech
        poss = {}
        sposs[sentence] = poss
        tokenizer = nltk.word_tokenize(sentence)
        for t in nltk.pos_tag(tokenizer):
            tag = t[1]
            if tag not in poss:
                poss[tag] = []
            poss[tag].append(t[0])

    for sentence in sposs.keys():
        poss = sposs[sentence]
        (word, sentence, replaced) = remove_word(sentence, poss)
        if replaced is not None:
            number = number + 1
            replaced = replaced.strip(".")
            question = {
                "number": number,
                "question": replaced,
                "answer": word
            }
            questionArray.append(question)

    # Storing the generated questions to the dataset
    with open('data.csv', mode="w") as dataset:
        writer = csv.DictWriter(dataset, fieldnames=col_names)
        writer.writeheader()
        for sentence in questionArray:
            dataset_writer = csv.writer(dataset, delimiter=',', quoting=csv.QUOTE_NONE, lineterminator='\n')
            dataset_writer.writerow([sentence['question'], sentence['answer']])
    response = jsonify(questionArray)
    response.status_code = 200
    return response
