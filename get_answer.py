import pandas as pd
from Levenshtein import ratio
from flask import jsonify

from suggestions.suggestions import get_suggestions

suggestion_array = []

# result evalutation based on the answer

def get_results(answerArray, fn):
    answerScoreArray = []
    answerData = []
    questionData = []
    for answer in answerArray["listening"]:
        answerData.append(answer["answer"])
        questionData.append(answer["question"])

    def get_result(a, q):
        answer, score, prediction, status = fn(a, q)
        answerJson = {
            "score": "{0:.2f}".format(score),
            "status": status
        }
        answerScoreArray.append(answerJson)
        return [q, prediction, answer, "{0:.2f}".format(score), status]

    pd.DataFrame(list(map(get_result, answerData, questionData)),
                 columns=["Answer", "Prediction", "Exact Answer", "Score", "Status"])
    suggestionData = suggestion_array

    resultJson = {
        "suggestion": list(dict.fromkeys(suggestionData)),
        "score": answerScoreArray,
        "xp": calculateXP(answerScoreArray)
    }
    suggestion_array.clear()
    response = jsonify(resultJson)
    response.status_code = 200
    return response


# Getting approximate answer using Levenshtein
def answer_predictor(a, q):
    data = pd.read_csv('data.csv') #Read the answers
    max_score = 0
    answer = None
    prediction = None
    status = "Correct"
    for idx, row in data.iterrows():
        question = row["Question"].strip(".")
        if q == question:
            score = ratio(row["Answer"], a)
            status = "Correct"
            if score >= 0.9:
                status = "Correct"
                suggestion_array.append(get_suggestions(a, row["Answer"], score))
                return row["Answer"], score, question, status
            elif score > max_score:
                max_score = score
                status = "Correct"
                answer = row["Answer"]
                suggestion_array.append(get_suggestions(a, row["Answer"], score))
                prediction = question
            break
        else:
            max_score = 0
            status = "Cannot initialize"

    if max_score < 0.8:
        status = "Wrong"
        suggestion_array.append(get_suggestions(a, answer, max_score))
        return answer, max_score, prediction, status
    return "Sorry, I didn't get you.", max_score, prediction, status


def calculateXP(score):
    xp = 0
    nCorrection = 0
    for row in score:
        xp = xp + (int(float(row['score']))*10)
        if row['status'] == 'Correct':
            nCorrection = nCorrection + 1
            xp = xp + 100
    return xp
