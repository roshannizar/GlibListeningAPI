from questions import questionFunc
import flask
from flask import request, jsonify

from answers.answerFunc import answerFunc

app = flask.Flask(__name__)


# Main Function
@app.route('/questions', methods=['POST'])
def main():
    try:
        data = request.form.get("description")

        return questionFunc.questionFunc(data)
    except Exception as error:
        app.logger.error(error)
        response = jsonify({'error': error})
        response.status_code = 500
        return response


@app.route('/answer', methods=['POST'])
def answer():
    try:
        arrayAnswerJson = request.json
        return answerFunc(arrayAnswerJson)
    except Exception as error:
        response = jsonify(error)
        response.status_code = 500
        return response


@app.route("/", methods=["GET"])
def mainPage():
    return "<h1>Welcome to glib listening web service</h2>"


# Call Main Function
if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
