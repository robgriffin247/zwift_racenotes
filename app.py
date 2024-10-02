import streamlit as st
import plotly.graph_objs as go
from file_read.fit_reader import fit_df

dt = fit_df("data/Zwift_Race_Zwift_Racing_League_Open_EMEA_W_Northern_West_Division_1_B_on_Country_to_Coastal_in_Makuri_Islands.fit")

sectors = [{"sector":"Lead in", "sector_type":"orange", "start":0, "end":200},
           {"sector":"Village Sprint", "sector_type":"green", "start":1600, "end":1700},
           {"sector":"Country Sprint", "sector_type":"green", "start":7300, "end":7400},
           {"sector":"Shisa Sprint", "sector_type":"green", "start":20400, "end":20700},
           {"sector":"Tidepool Sprint", "sector_type":"green", "start":25500, "end":25800},
           ]


route_profile = go.Figure()

for sector in sectors:
    route_profile.add_vrect(
                x0=sector["start"],
                x1=sector["end"],
                fillcolor=sector["sector_type"],
                opacity=0.4 ,
                line_width=1,
            )

route_profile.add_trace(go.Scatter(x=dt["distance"], y=dt["altitude"], mode="lines", 
                                   customdata=dt[["distance_fmt", "altitude_fmt"]],
                                   hovertemplate="<b>Distance: %{customdata[0]}km</b><br>" + 
                                    "<b>Altitude: %{customdata[1]}m</b><br>" + 
                                    "<extra></extra>"))

route_profile.update_layout(xaxis_title="Distance (km)", yaxis_title="Altitude (m)")

st.plotly_chart(route_profile)
