import pandas as pd
from Levenshtein import ratio
from flask import jsonify

data = pd.read_csv('data.csv')


def getResults(answerArray, fn):
    answerScoreArray = []
    answerData = []
    questionData = []

    for answer in answerArray["listening"]:
        answerData.append(answer["answer"])
        questionData.append(answer["question"])

    print(answerData)
    print(questionData)

    def getResult(a, q):
        answer, score, prediction, status = fn(a, q)
        answerJson = {
            "score": score,
            "status": status
        }
        answerScoreArray.append(answerJson)
        return [q, prediction, answer, score, status]

    pd.DataFrame(list(map(getResult, answerData, questionData)),
                 columns=["Answer", "Prediction", "Exact Answer", "Score", "Status"])

    response = jsonify(answerScoreArray)
    response.status_code = 200
    return response


# Getting approximate answer using Levenshtein
def answerPredictor(a, q):
    max_score = 0
    answer = ""
    prediction = ""
    status = "Correct"
    for idx, row in data.iterrows():
        if q == row["Question"]:
            score = ratio(row["Answer"], a)
            if score >= 0.9:
                return row["Answer"], score, row["Question"], status
            elif score > max_score:
                max_score = score
                status = "Correct"
                answer = row["Answer"]
                prediction = row["Question"]
            break
        else:
            max_score = 0
            status = "Cannot initialize"

    if max_score < 0.8:
        status = "Wrong"
        return answer, max_score, prediction, status
    return "Sorry, I didn't get you.", max_score, prediction, status
