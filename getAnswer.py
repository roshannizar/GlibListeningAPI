import pandas as pd
from Levenshtein import ratio
from flask import jsonify
import os


def getResults(answerArray, fn):
    answerScoreArray = []
    answerData = []
    questionData = []

    for answer in answerArray["listening"]:
        answerData.append(answer["answer"])
        questionData.append(answer["question"])

    def getResult(a, q):
        answer, score, prediction, status = fn(a, q)
        answerJson = {
            "score": "{0:.2f}".format(score),
            "status": status
        }
        answerScoreArray.append(answerJson)
        return [q, prediction, answer, "{0:.2f}".format(score), status]

    pd.DataFrame(list(map(getResult, answerData, questionData)),
                 columns=["Answer", "Prediction", "Exact Answer", "Score", "Status"])

    response = jsonify(answerScoreArray)
    response.status_code = 200
    return response


# Getting approximate answer using Levenshtein
def answerPredictor(a, q):
    data = pd.read_csv('data.csv')
    max_score = 0
    answer = ""
    prediction = ""
    status = "Correct"
    for idx, row in data.iterrows():
        question = row["Question"].strip(".")
        if q == question:
            score = ratio(row["Answer"], a)
            status = "Correct"
            if score >= 0.9:
                status = "Correct"
                return row["Answer"], score, question, status
            elif score > max_score:
                max_score = score
                status = "Correct"
                answer = row["Answer"]
                prediction = question
            break
        else:
            max_score = 0
            status = "Cannot initialize"

    if max_score < 0.8:
        status = "Wrong"
        return answer, max_score, prediction, status
    return "Sorry, I didn't get you.", max_score, prediction, status
