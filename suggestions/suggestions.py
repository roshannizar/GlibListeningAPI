
def get_suggestions(answer, dataSetAnswer, score):
    if score >= 0.8:
        return evaluate_suggestion(answer, dataSetAnswer, score)


def evaluate_suggestion(answer, dataSetAnswer, score):
    if len(answer) != len(dataSetAnswer):
        if score >= 0.8:
            return 'Need more concentration!'
        else:
            return 'Needs to improve your vocabulary!'
    for i, (x, y) in enumerate(zip(answer, dataSetAnswer)):
        if x != y:
            if x.lower() == y.lower():
                return 'Understand where upper case letters and lower case letters to be used!'
            else:
                return 'Try to reduce your spelling mistakes! It\'s available in grammar component'
        else:
            return 'Good keep it up!'