import io
import os
import base64
import joblib
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import mysql.connector
from datetime import datetime
from flask import Flask, request, jsonify

matplotlib.use('Agg')

app = Flask(__name__)

model = joblib.load('Machine Learning Model.pkl')

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'username'),
        password=os.environ.get('DB_PASSWORD', 'password'),
        database=os.environ.get('DB_NAME', 'ReachWhen'),
        port=int(os.environ.get('DB_PORT', 3306))
    )

@app.route('/', methods=['GET'])
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ReachWhen -  Tamil Nadu Train Journey Duration Predictor</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
            }
            input, select {
                padding: 10px;
                margin: 10px 0;
                width: 100%;
                box-sizing: border-box;
            }
            input[type=number]::-webkit-inner-spin-button,
            input[type=number]::-webkit-outer-spin-button {
                -webkit-appearance: none;
                margin: 0;
            }
            input[type=number] {
                -moz-appearance: textfield;
            }
            button {
                padding: 10px 20px;
                background: #007bff;
                color: white;
                border: none;
                cursor: pointer;
                width: 100%;
                font-size: 16px;
            }
            button:hover {
                background: #0056b3;
            }
            .result {
                margin-top: 30px;
            }
            h1 {
                color: #333;
                text-align: center;
            }
            .input-group {
                display: flex;
                gap: 10px;
            }
            .input-group > div {
                flex: 1;
            }
        </style>
    </head>
    <body>
        <h1>ReachWhen</h1>
        <div>
            <label>Train Number:</label>
            <input type="text" id="trainNo">

            <div class="input-group">
                <div>
                    <label>Pickup Station:</label>
                    <input type="text" id="fromStation">
                </div>
                <div>
                    <label>Drop Station:</label>
                    <input type="text" id="toStation">
                </div>
            </div>

            <div class="input-group">
                <div>
                    <label>Distance (km):</label>
                    <input type="number" id="distance" step="0.1">
                </div>
                <div>
                    <label>Number of Stops:</label>
                    <input type="number" id="stops" min="0">
                </div>
            </div>

            <div class="input-group">
                <div>
                    <label>Departure Date & Time:</label>
                    <input type="datetime-local" id="deptTime">
                </div>
                <div>
                    <label>Arrival Date & Time:</label>
                    <input type="datetime-local" id="arrTime">
                </div>
            </div>

            <button onclick="predict()">Predict Duration</button>
        </div>

        <div id="result" class="result"></div>

        <script>
            function predict() {
                const trainNo = document.getElementById('trainNo').value;
                const fromStation = document.getElementById('fromStation').value.toUpperCase();
                const toStation = document.getElementById('toStation').value.toUpperCase();
                const distance = document.getElementById('distance').value;
                const stops = document.getElementById('stops').value;
                const deptTime = document.getElementById('deptTime').value;
                const arrTime = document.getElementById('arrTime').value;

                if (!trainNo || !fromStation || !toStation || !distance || !stops || !deptTime || !arrTime) {
                    alert('Please fill all fields');
                    return;
                }

                if (isNaN(parseFloat(distance)) || parseFloat(distance) < 0) {
                    alert('Please enter a valid positive distance');
                    return;
                }

                document.getElementById('result').innerHTML = '<p>Loading prediction...</p>';

                fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        train_no: trainNo,
                        from_station: fromStation,
                        to_station: toStation,
                        distance: parseFloat(distance),
                        stops: parseInt(stops),
                        dept_time: deptTime,
                        arr_time: arrTime
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        document.getElementById('result').innerHTML = `<p style="color:red;">${data.error}</p>`;
                    } else {
                        document.getElementById('result').innerHTML = `
                            <div style="border: 1px solid #ddd; padding: 20px; border-radius: 5px; background: #f9f9f9;">
                                <h3 style="margin-top: 0;">Prediction Results</h3>
                                <p><strong>Train:</strong> ${data.train_no} (${data.from_station} &rarr; ${data.to_station})</p>
                                <p><strong>Total Distance:</strong> ${data.distance} km</p>
                                <p><strong>Number of Stops:</strong> ${data.stops}</p>
                                <hr>
                                <p><strong>Actual Duration:</strong> ${data.actual_duration} minutes</p>
                                <p><strong>Predicted Duration:</strong> ${data.predicted_duration.toFixed(2)} minutes</p>
                                <p><strong>Prediction Accuracy:</strong> ${data.accuracy.toFixed(2)}%</p>
                                <img src="data:image/png;base64,${data.chart}" style="width: 100%; border-radius: 5px; margin-top: 15px;">
                            </div>
                        `;
                    }
                })
                .catch(error => {
                    document.getElementById('result').innerHTML = `<p style="color:red;">Error: ${error}</p>`;
                });
            }

            document.addEventListener('keypress', function(event) {
                if (event.key === 'Enter') {
                    predict();
                }
            });
        </script>
    </body>
    </html>
    """

@app.route('/predict', methods=['POST'])
def predict():
    try:
        request_data = request.get_json()
        
        train_no = request_data.get('train_no')
        from_station = request_data.get('from_station')
        to_station = request_data.get('to_station')
        distance = request_data.get('distance')
        stops = request_data.get('stops')
        dept_time_str = request_data.get('dept_time')
        arr_time_str = request_data.get('arr_time')

        if not all([train_no, from_station, to_station, str(distance), str(stops), dept_time_str, arr_time_str]):
            return jsonify({'error': 'Missing required fields'}), 400

        try:
            dept_dt = datetime.strptime(dept_time_str, "%Y-%m-%dT%H:%M")
            arr_dt = datetime.strptime(arr_time_str, "%Y-%m-%dT%H:%M")
        except ValueError:
            return jsonify({'error': 'Invalid date/time format. Use YYYY-MM-DDTHH:MM'}), 400

        time_difference = arr_dt - dept_dt
        actual_duration = int(time_difference.total_seconds() / 60)

        if actual_duration <= 0:
            return jsonify({'error': 'Arrival date/time must be after departure date/time'}), 400

        X = np.array([[float(distance), int(stops)]])
        predicted_duration = float(model.predict(X)[0])

        if actual_duration > 0:
            absolute_error = abs(actual_duration - predicted_duration)
            percentage_error = (absolute_error / actual_duration) * 100
            accuracy = 100 - percentage_error
        else:
            accuracy = 0.0

        try:
            db = get_db_connection()
            cursor = db.cursor()

            sql = """
                INSERT INTO PredictionData
                (TrainNo, PickUpStation, DropStation, Distance, NumberOfStops, 
                ArrivalTime, DestinationTime, ActualDuration, PredictedDuration)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            values = (
                train_no, from_station, to_station, distance, stops,
                dept_time_str, arr_time_str, actual_duration, int(predicted_duration)
            )

            cursor.execute(sql, values)
            db.commit()
        finally:
            if 'db' in locals() and db.is_connected():
                cursor.close()
                db.close()

        fig, ax = plt.subplots()
        categories = ['Actual Duration', 'Predicted Duration']
        values = [actual_duration, predicted_duration]
        colors = ['#2ecc71', '#3498db']

        bars = ax.bar(categories, values, color=colors, width=0.6, edgecolor='black', linewidth=2)

        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2, height, f'{value:.2f}',
                ha='center', va='bottom', fontsize=12, fontweight='bold'
            )

        ax.set_ylabel('Duration (minutes)', fontsize=12, fontweight='bold')
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_ylim(0, max(values) * 1.2)

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
        buffer.seek(0)
        chart_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)

        return jsonify({
            'train_no': train_no,
            'from_station': from_station,
            'to_station': to_station,
            'distance': float(distance),
            'stops': int(stops),
            'actual_duration': actual_duration,
            'predicted_duration': predicted_duration,
            'accuracy': accuracy,
            'chart': chart_base64
        })

    except Exception as error:
        return jsonify({'error': str(error)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
