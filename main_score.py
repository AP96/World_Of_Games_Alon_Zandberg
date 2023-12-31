from flask import Flask

app = Flask(__name__)


# This server is designed to display the game score stored in a text file

@app.route('/health', methods=['GET'])
def test():
    return 'Test Successful'


# To handle requests to the /score endpoint
# and return a web page with the current game score or an error message.
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
    app.run(host='0.0.0.0', port=5000)
