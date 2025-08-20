from flask import Flask, jsonify
import logging

app = Flask(__name__)
counter = 0

# Configure logging to file
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

@app.route('/count', methods=['GET'])
def count():
    global counter
    counter += 1
    logging.info(f"Counter incremented to {counter}")
    return jsonify({'count': counter})

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Flask Counter App!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
