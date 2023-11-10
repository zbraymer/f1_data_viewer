import streamlit as st
import os
import fastf1 as f1
import time
import matplotlib.pyplot as plt
from bokeh.models import Range1d
from bokeh.plotting import figure, show
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, HoverTool
from utils.utilities import race_picker_sidebar, get_session_data, get_telemetry
import numpy as np

import altair as alt
# Image Directory
png_dir = os.path.dirname(os.path.dirname(__file__))


# def track_plot(track_source, driver_1=None, driver_2=None):
#     fig = figure(width=800, height=800, title='Circuit Map', match_aspect=True)
#     fig.line(source=track_source, x='X', y='Y', line_width=6, line_color="#000000")
#     if driver_1 is not None:
#         fig.scatter(source=driver_1, x='X', y='Y', size=10, fill_color="#953553")
#     if driver_2 is not None:
#         fig.scatter(source=driver_2, x='X', y='Y', size=10, fill_color="#ff0000")
#
#     return fig


# def animate(window, driver1, driver2):
#
#     if driver1 is not None:
#         scatter_d1.set_ydata(driver1.iloc[window]['Y'])
#         scatter_d1.set_xtdata(driver1.iloc[window]['X'])
#
#     if driver2 is not None:
#         scatter_d2.set_ydata(driver2.iloc[window]['Y'])
#         scatter_d2.set_xtdata(driver2.iloc[window]['X'])
#     the_plot.pyplot(plt)
#     return


def write():
    year, track, session = race_picker_sidebar()
    event = get_session_data(year, track, session)

    pos = event.laps.pick_driver('HAM').pick_fastest().get_pos_data()
    with st.sidebar:
        available_drivers = ['None'] + event.laps['Driver'].unique().tolist()
        driver1 = st.selectbox('Driver 1', options=available_drivers)
        driver2 = st.selectbox('Driver 2', options=available_drivers)

        # use year/track/session to load available laps
        available_laps = ['fastest'] + event.laps['LapNumber'].unique().tolist()
        which_lap = st.selectbox('Laps', options=available_laps)

    driver_1_laps = get_telemetry(event, driver1, which_lap) if driver1 != 'None' else None
    driver_2_laps = get_telemetry(event, driver2, which_lap) if driver2 != 'None' else None


    pos = pos.drop(columns=["Time", "Date", "SessionTime"])
    #st.write(pos.head())
    track = alt.Chart(pos).mark_circle().encode(x='X', y='Y')
    st.altair_chart(track)
    # seq = list(range(pos.shape[0]))
    # window_size = 3
    #
    # for i in range(len(seq) - window_size + 1):
    #     win = seq[i: i + window_size]



    st.button('Race')

    st.write()
    return


if __name__ == "__main__":
    write()