import json
import sys
from datetime import datetime, timedelta

#get file from starting arg
path = sys.argv[1]
print(path)

#open file on path 
f = open(path)

#extract data from file f
data = json.load(f)

#close file f
f.close()


def transform_json(input_data):
    transformed_data = []
    start_time = datetime.strptime(input_data["startTs"], "%Y-%m-%dT%H:%M:%S.%fZ")

    for key, array in input_data.items():
        if key == "motion":
            for entry in array:
                ms_from_start = entry["msFromStart"]
                timestamp = (start_time + timedelta(milliseconds=ms_from_start)).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                transformed_data.append({
                    "timestamp": timestamp,
                    "type": "- M - motion",
                    "data": {
                        "acc": entry["acc"],
                        "accG": entry["accG"],
                        "rotRate": entry["rotRate"],
                        "interval": entry["interval"]
                    }
                })
        elif key == "orientation":
            for entry in array:
                ms_from_start = entry["msFromStart"]
                timestamp = (start_time + timedelta(milliseconds=ms_from_start)).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                transformed_data.append({
                    "timestamp": timestamp,
                    "type": "- O - orientation",
                    "data": {
                        "alpha": entry["alpha"],
                        "beta": entry["beta"],
                        "gamma": entry["gamma"],
                        "abs": entry.get("abs", False)
                    }
                })
        elif key == "distance":
            for entry in array:
                ms_from_start = entry["msFromStart"]
                timestamp = (start_time + timedelta(milliseconds=ms_from_start)).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                transformed_data.append({
                    "timestamp": timestamp,
                    "type": "- D - distance",
                    "data": {
                        "distance": entry.get("cumulativeWheelRevolutions", "")
                    }
                })
        # Add handling for other keys if necessary
    return transformed_data


#transform data
transformed_data = transform_json(data)

transformed_data.sort(key=lambda x: x["timestamp"])

with open("transformed.txt", "w") as file:
    for entry in transformed_data:
        file.write(f"{entry['timestamp']} {entry['type']} {entry['data']}\n")