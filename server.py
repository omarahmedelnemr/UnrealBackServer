from flask import Flask, jsonify
import json
import random
import os

app = Flask(__name__)
data_file = 'data.json'

# Initialize the file with a default value if it doesn't exist
if not os.path.exists(data_file):
    with open(data_file, 'w') as f:
        json.dump({"power": 10}, f)

def get_current_power():
    with open(data_file, 'r') as f:
        data = json.load(f)
    return data["power"]

def update_power(new_power):
    with open(data_file, 'w') as f:
        json.dump({"power": new_power}, f)
@app.route('/', methods=['GET'])
def main():
    return  "<center><h1>Server is Running .... go to one of the Following:</h1><h2><a href='./get_readings'>/get_readings</a></h2><h2><a href='./high_reading'>/high_reading</a></h2><h2><a href='./low_reading'>/low_reading</a></h2></center>"
@app.route('/get_readings', methods=['GET'])
def get_readings():
    current_power = get_current_power()
    # Randomly adjust the power by -5 to +5, ensuring it stays positive
    new_power = max(0, current_power + random.randint(-5, 5))
    update_power(new_power)
    data = {
        "on": True,
        "power": new_power
    }
    return jsonify(data)

@app.route('/high_reading', methods=['GET'])
def high_reading():
    current_power = get_current_power()
    # Increase power by a random number between 1 and 10
    new_power = current_power + random.randint(1, 10)
    update_power(new_power)
    data = {
        "on": True,
        "power": new_power
    }
    return jsonify(data)

@app.route('/low_reading', methods=['GET'])
def low_reading():
    current_power = get_current_power()
    # Decrease power by a random number between 1 and 10, ensuring it stays positive
    new_power = max(0, current_power - random.randint(1, 10))
    update_power(new_power)
    data = {
        "on": False,
        "power": new_power
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
