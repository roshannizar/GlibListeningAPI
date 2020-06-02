import pandas as pd
from Levenshtein import ratio
from flask import jsonify

data = pd.read_csv("../dataset/data.csv", encoding='utf-8')


def getResults(questions, fn):
    answerScoreArray = []

    def getResult(q):
        answer, score, prediction = fn(q)
        answerScoreArray.append(score)
        return [q, prediction, answer, score]

    pd.DataFrame(list(map(getResult, questions)), columns=["Answer", "Prediction", "Exact Answer", "Score"])

    response = jsonify(answerScoreArray)
    response.status_code = 200
    return response


# Getting approximate answer using Levenshtein
def answerPredictor(q):
    max_score = 0
    answer = ""
    prediction = ""
    for idx, row in data.iterrows():
        score = ratio(row["Answer"], q)
        if score >= 0.9:  # I'm sure, stop here
            return row["Answer"], score, row["Question"]
        elif score > max_score:  # I'm unsure, continue
            max_score = score
            answer = row["Answer"]
            prediction = row["Question"]

    if max_score > 0.8:  # threshold is lowered
        return answer, max_score, prediction
    return "Sorry, I didn't get you.", max_score, prediction
