import streamlit as st
import os
import fastf1 as f1
import fastf1.plotting
from circuits import baku
from utils.utilities import get_telemetry
from bokeh.models import Range1d
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool

cache_dir = os.path.dirname(os.path.dirname(__file__))
f1.Cache.enable_cache(os.path.join(cache_dir, 'cache'))
circuit_map = {"BAKU": baku}

# Dict of driver short names used in sidebar to driver full names used in color library
driver_translate = fastf1.plotting.DRIVER_TRANSLATE
driver_colors = fastf1.plotting.DRIVER_COLORS
driver_colors_short = {k: driver_colors[v] for k, v in driver_translate.items()}


def get_corners(track_name):
    corners = circuit_map[track_name].corners
    return list(corners.keys())


# Get data
@st.cache()
def get_session_data(year, track, session):
    event = f1.get_session(year, track, session)
    event.load()
    return event


def write():
    with st.sidebar:
        track = st.selectbox('Track', options=['BAKU'])
        year = st.selectbox('Year', options=[n + 1 for n in range(2017, 2022)][::-1])

        session = st.selectbox('Session',
                               options=['Race', 'Qualifying', 'Sprint', 'Sprint Qualifying',
                                        'Practice 3', 'Practice 2', 'Practice 1'])
        # use year/track/session to load available drivers
        event = get_session_data(year, track, session)

    with st.sidebar:
        available_drivers = event.laps['Driver'].unique().tolist()
        driver1 = st.selectbox('Driver 1', options=available_drivers)
        driver2 = st.selectbox('Driver 2', options=available_drivers)
        # use year/track/session to load available laps
        available_laps = ['fastest'] + event.laps['LapNumber'].unique().tolist()
        which_lap = st.selectbox('Laps', options=available_laps)
        corner = st.selectbox('Corner', options=get_corners(track))

    # event.load()
    driver_1_laps = get_telemetry(event, driver1, which_lap)
    driver_2_laps = get_telemetry(event, driver2, which_lap)

    fig = figure(title=f"Turn {corner}, {track}, {year}",
                 plot_width=600, plot_height=600)
    fig.xaxis.axis_label = 'Distance From Start'
    fig.yaxis.axis_label = 'Speed (mph)'
    fig.title_location ='above'
    fig.title.text_font_size = "25px"

    fig.line(source=driver_1_laps, x='Distance', y='Speed',
             legend_label=driver1, line_color=driver_colors_short[driver1])

    fig.line(source=driver_2_laps, x='Distance', y='Speed',
             legend_label=driver2, line_color=driver_colors_short[driver2])
    fig.x_range = Range1d(*circuit_map[track].corners[corner])

    st.bokeh_chart(fig)
    return


if __name__ == "__main__":
    write()
