from questions import question_func
import flask
from flask import request, jsonify, render_template

from answers.answer_func import answer_func

app = flask.Flask(__name__)


# Main Function
@app.route('/questions', methods=['POST'])
def main():
    try:
        data = request.form.get("description")

        return question_func.question_func(data)
    except Exception as error:
        app.logger.error(error)
        response = jsonify({'error': error})
        response.status_code = 500
        return response


@app.route('/answer', methods=['POST'])
def answer():
    try:
        arrayAnswerJson = request.json
        return answer_func(arrayAnswerJson)
    except Exception as error:
        response = jsonify(error)
        response.status_code = 500
        return response


@app.route('/', methods=['GET'])
def swagger():
    return render_template('swaggerui.html')


# Call Main Function
if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
