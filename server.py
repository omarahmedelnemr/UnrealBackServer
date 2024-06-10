from flask import Flask, jsonify
import json
import random
import os

app = Flask(__name__)
data_file = 'data.json'

# Initialize the file with a default value if it doesn't exist
if not os.path.exists(data_file):
    with open(data_file, 'w') as f:
        json.dump({"Sensor 1":{"power": 10},"Sensor 2":{"power": 10}}, f)

def get_current_power():
    with open(data_file, 'r') as f:
        data = json.load(f)
    return data

def update_power(new_power, new_power2):
    with open(data_file, 'w') as f:
        json.dump({"Sensor 1":{"power": new_power},"Sensor 2":{"power": new_power2}}, f)
@app.route('/', methods=['GET'])
def main():
    return  "<center>\
                <h1>Server is Running .... go to one of the Following:</h1>\
                <h2><a href='./get_readings'>/get_readings</a> # Get Random Readings, Sensor 1 off when < 20, Sensor 2 Totally Random on/off</h2>\
                <h2><a href='./high_reading'>/high_reading</a> # Making the Readings of Both Sensors Go Higher</h2>\
                <h2><a href='./low_reading'>/low_reading</a> # Making the Readings of Both Sensors Go Lower</h2>\
            </center>"
@app.route('/get_readings', methods=['GET'])
def get_readings():
    total = get_current_power()
    current_power_sensor1 = total["Sensor 1"]["power"]
    current_power_sensor2 = total["Sensor 2"]["power"]
    # Randomly adjust the power by -5 to +5, ensuring it stays positive
    new_power = max(0, current_power_sensor1 + random.randint(-5, 5))
    new_power2 = max(0, current_power_sensor2 + random.randint(-5, 5))
    update_power(new_power,new_power2)
    data = {
        "Sensor 1":{
        "on": new_power >= 20,
        "power": new_power
    },"Sensor 2":{
        "on": random.randint(-1, 1) == 1,
        "power": new_power2
    }}
    return jsonify(data)

@app.route('/high_reading', methods=['GET'])
def high_reading():
    current_power = get_current_power()
    current_sesor1 = current_power['Sensor 1']["power"]
    current_sesor2 = current_power['Sensor 2']["power"]
    # Increase power by a random number between 1 and 10
    new_power = current_sesor1 + random.randint(1, 10)
    new_power2 = current_sesor2 + random.randint(1, 10)
    update_power(new_power,new_power2)
    data = {
        "Sensor 1":{
        "on": new_power >= 20,
        "power": new_power
    },"Sensor 2":{
        "on": random.randint(-1, 1) == 1,
        "power": new_power2
    }}
    return jsonify(data)

@app.route('/low_reading', methods=['GET'])
def low_reading():
    current_power = get_current_power()
    current_sesor1 = current_power['Sensor 1']["power"]
    current_sesor2 = current_power['Sensor 2']["power"]
    # Increase power by a random number between 1 and 10
    new_power = current_sesor1 - random.randint(1, 10)
    new_power2 = current_sesor2 - random.randint(1, 10)
    update_power(new_power,new_power2)
    data = {
        "Sensor 1":{
        "on": new_power >= 20,
        "power": new_power
    },"Sensor 2":{
        "on": random.randint(-1, 1) == 1,
        "power": new_power2
    }}
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
