import fitdecode
import pandas as pd

def fit_df(fit_file):   

    # Read the fit file into a dataframe
    data = []
    
    with fitdecode.FitReader(fit_file) as f:
        for frame in f:
            if isinstance(frame, fitdecode.records.FitDataMessage):
                message = {}
                for field in frame.fields:
                    message[field.name] = frame.get_value(field.name)

                data.append(message)

    data = pd.DataFrame(data)

    # Clean up
    data = data[data["position_lat"].notna()]

    data = data[["timestamp",
                 "position_lat", "position_long", "altitude", "distance", 
                 "heart_rate", "power", "cadence"]]
    
    # Add elapsed seconds - important for adding sectors (when based on ride time)
    data["seconds"] = data["timestamp"].diff(1).dt.seconds.fillna(0).cumsum()

    # Get world and route to allow reference to sector data sheet
    world = fit_file.split("__")[0].replace("_", " ").replace("data/", "")
    route = fit_file.split("__")[1].replace("_", " ").split(".fit")[0]

    # Get sector data (name, type)
    sectors_data = pd.read_csv("data/sectors.csv")

    # Iterate each sector to identify and transfer data for each sector into the fit data
    for _, s in sectors_data.iterrows():
        if s["world"]==world and s["route"]==route:
            data.loc[((data["seconds"]>=s["start_s"]) & (data["seconds"]<=s["end_s"])), "sector_name"] = s["sector_name"]
            data.loc[((data["seconds"]>=s["start_s"]) & (data["seconds"]<=s["end_s"])), "sector_type"] = s["sector_type"]
    
    # old stuff that may come in useful for mapping, gradients etc.
    #data['position_lat'] = data['position_lat'].apply(lambda x: -x / ((2**32)/360))
    #data['position_long'] = data['position_long'].apply(lambda x: x / ((2**32)/360))
    #data["distance_change"] = data.distance - data.distance.shift(1)
    #data["altitude_change"] = data.altitude - data.altitude.shift(1)
    #data["grade"] = data.altitude_change / data.distance_change * 100
    #data["kmh"] = (data.distance - data.distance.shift(1)) * (3.6 / ((data.timestamp - data.timestamp.shift(1)) / np.timedelta64(1, "s")))
    
    # Formating of distance and altitude for the tooltips in the app
    data["distance_fmt"] = (data["distance"]/1000).round(2)
    data["altitude_fmt"] = data["altitude"].round(1)

    return data
