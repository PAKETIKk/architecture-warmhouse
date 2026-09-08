from flask import Flask, request, jsonify
from datetime import datetime, timezone
import random
import os

app = Flask(__name__)

@app.route("/temperature", methods=["GET"])
def get_temperature(location=None, sensorID=None):
    location = request.args.get("location")
    sensorID = request.args.get("sensorID")

    #  If no location is provided, use a default based on sensor ID
    if not location:
        match sensorID:
            case "1":
                location = "Living Room"
            case "2":
                location = "Bedroom"
            case "3":
                location = "Kitchen"
            case _:
                location = "Unknown"

	#  If no sensor ID is provided, generate one based on location
    if not sensorID:
        match location:
            case "Living Room":
                sensorID = "1"
            case "Bedroom":
                sensorID = "2"
            case "Kitchen":
                sensorID = "3"
            case _:
                sensorID = "0"

    temperature = round(random.uniform(-50, 50), 1)

    # return jsonify(
    #     {
    #         "location": location,
    #         "sensorID": sensorID,
    #         "temperature": temperature,
    #         "unit": "°C"
    #     }
    # )

    return jsonify(
            {
                "value": temperature,
                "unit": "°C",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "location": location,
                "status": "active",
                "sensor_id": sensorID
            }
        )

@app.route("/temperature/<sensor_id>", methods=["GET"])
def get_temperature_by_id(sensor_id):
    return get_temperature(
            sensorID=sensor_id
        )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8081))
    app.run(host="0.0.0.0", port=port)