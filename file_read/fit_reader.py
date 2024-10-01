import fitdecode
import pandas as pd
import numpy as np

def fit_df(fit_file):   
    #data = pd.DataFrame()
    data = []
    with fitdecode.FitReader(fit_file) as f:
        for frame in f:
            if isinstance(frame, fitdecode.records.FitDataMessage):
                message = {}
                for field in frame.fields:
                    message[field.name] = frame.get_value(field.name)

                data.append(message)

    data = pd.DataFrame(data)

    data = data[["timestamp",
                 "position_lat", "position_long", "altitude", "distance", 
                 "heart_rate", "power", "cadence"]]

    data = data[data["position_lat"].notna()]
    #data['position_lat'] = data['position_lat'].apply(lambda x: -x / ((2**32)/360))
    #data['position_long'] = data['position_long'].apply(lambda x: x / ((2**32)/360))
    #data["distance_change"] = data.distance - data.distance.shift(1)
    #data["altitude_change"] = data.altitude - data.altitude.shift(1)

    #data["grade"] = data.altitude_change / data.distance_change * 100
    #data["kmh"] = (data.distance - data.distance.shift(1)) * (3.6 / ((data.timestamp - data.timestamp.shift(1)) / np.timedelta64(1, "s")))
    data["distance_fmt"] = (data["distance"]/1000).round(2)
    data["altitude_fmt"] = data["altitude"].round(1)

    return data
