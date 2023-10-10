from flask import Flask
app = Flask(__name__)


@app.route('/score', methods=['GET'])
def score_server():
    try:
        # Try to read the score from the scores.txt file
        with open('scores.txt', 'r') as f:
            score = f.read().strip()
        return f'<html> <head> <title>Scores Game</title></head><body><h1>The score is:</h1><div id="score">{score}</div></body></html>'
    except IOError as e:
        return f'<html><head><title>Scores Game</title></head><body><h1>ERROR:</h1><div id="score" style="color:red">{e}</div></body></html>'


if __name__ == '__main__':
    app.run(debug=True)
