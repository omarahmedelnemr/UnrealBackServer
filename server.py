from flask import Flask, request, jsonify
import json
import random
import os
from datetime import datetime

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
def get_last_reading():
    file_path = 'Readings.json'

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                readings = json.load(file)
                if readings:
                    last_reading = readings[-1]
                    return jsonify(last_reading)
                else:
                    return jsonify({'error': 'No readings found'}), 404
            except json.JSONDecodeError:
                return jsonify({'error': 'Error reading JSON file'}), 500
    else:
        return jsonify({'error': 'File not found'}), 404

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
@app.route('/save_data', methods=['POST'])
def receive_data():
    if request.method == 'POST':
        print(request.form)

        # Load the received JSON data
        data = json.loads(list(request.form)[0])

        print("Received Data:")
        print("Voltage:", data["voltage"])
        print("Current:", data["current"])

        # Define the file path for the JSON file
        file_path = 'Readings.json'

        # Initialize an empty list to hold the readings
        readings = []

        # Check if the JSON file already exists
        if os.path.exists(file_path):
            # Read the existing data from the file
            with open(file_path, 'r') as file:
                try:
                    readings = json.load(file)
                except json.JSONDecodeError:
                    # Handle case where file is empty or not properly formatted
                    readings = []
        newData = {}
        newData['voltage'] = data['voltage']
        newData['current'] = data['current']
        newData['power'] = float(data['voltage']) * float(data['current'])
        newData['on'] = float(newData['power']) > 0
        newData['timestamp'] = datetime.now().isoformat()

        # Append the new reading to the list
        readings.append(newData)

        # Write the updated readings list back to the JSON file
        with open(file_path, 'w') as file:
            json.dump(readings, file, indent=4)

        # Optionally, you can send a response back to the ESP32
        return 'Data received successfully', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
