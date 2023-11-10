import streamlit as st
import os
import fastf1 as f1
import fastf1.plotting
from circuits import baku
from utils.utilities import get_telemetry
from bokeh.models import Range1d
from bokeh.plotting import figure, show
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, HoverTool

cache_dir = os.path.dirname(os.path.dirname(__file__))
f1.Cache.enable_cache(os.path.join(cache_dir, 'cache'))
circuit_map = {"BAKU": baku}

# Dict of driver short names used in sidebar to driver full names used in color library
driver_translate = fastf1.plotting.DRIVER_TRANSLATE
driver_colors = fastf1.plotting.DRIVER_COLORS
driver_colors_short = {k: driver_colors[v] for k, v in driver_translate.items()}


def speed_plot(telmetry_dict, xrange=None):
    sf = figure(width=900, height=150, title='Speed Trace', x_range=xrange)
    for driver, telemetry in telmetry_dict.items():
        sf.line(source=telemetry, x='Distance', y='Speed',
                legend_label=driver, line_color=driver_colors_short[driver])
    return sf


def gear_plot(telmetry_dict, xrange=None):
    gp = figure(width=900, height=150, title='Gear Trace', x_range=xrange)
    for driver, telemetry in telmetry_dict.items():
        gp.line(source=telemetry, x='Distance', y='nGear',
                legend_label=driver, line_color=driver_colors_short[driver])
    return gp


def rpm_plot(telmetry_dict, xrange=None):
    rp = figure(width=900, height=150, title='RPM Trace', x_range=xrange)
    for driver, telemetry in telmetry_dict.items():
        rp.line(source=telemetry, x='Distance', y='RPM',
                legend_label=driver, line_color=driver_colors_short[driver])
    return rp


def brake_plot(telmetry_dict, xrange=None):
    bp = figure(width=900, height=150, title='Brake Trace', x_range=xrange)
    for driver, telemetry in telmetry_dict.items():
        bp.line(source=telemetry, x='Distance', y='Brake',
                legend_label=driver, line_color=driver_colors_short[driver])
    return bp


def throttle_plot(telmetry_dict, xrange=None):
    tp = figure(width=900, height=150, title='Throttle Trace', x_range=xrange)
    for driver, telemetry in telmetry_dict.items():
        tp.line(source=telemetry, x='Distance', y='Throttle',
                legend_label=driver, line_color=driver_colors_short[driver])
    return tp


def drs_plot(telmetry_dict, xrange=None):
    dp = figure(width=900, height=200, title='DRS Trace', x_range=xrange)
    for driver, telemetry in telmetry_dict.items():
        dp.line(source=telemetry, x='Distance', y='DRS',
                legend_label=driver, line_color=driver_colors_short[driver])
    return dp


plot_dict = {'Speed': speed_plot, 'Throttle': throttle_plot, 'Brake': brake_plot, 'Gear': gear_plot, 'RPM': rpm_plot}


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
        drivers = st.multiselect('Driver', options=available_drivers, default='HAM')

        # use year/track/session to load available laps
        available_laps = ['fastest'] + event.laps['LapNumber'].unique().tolist()
        which_lap = st.selectbox('Laps', options=available_laps)

        plots = st.multiselect('Plots', options=['All', 'Speed', 'Throttle', 'Brake', 'Gear', 'RPM'], default='All')

    tel_dict = {driver: get_telemetry(event, driver, which_lap) for driver in drivers}
    #tel = get_telemetry(event, driver, which_lap)

    if len(plots) > 0:
        if plots[0] == 'All':
            plots = ['Speed', 'Throttle', 'Brake', 'Gear', 'RPM']
        # Link the plots if there is more than one.
        plot_list = []
        if len(plots) > 1:
            p0 = plot_dict[plots[0]](tel_dict)
            plot_list.append(p0)
            for plot in plots[1:]:
                plot_list.append(plot_dict[plot](tel_dict, xrange=p0.x_range))

        else:
            plot_list = [plot_dict[plot](tel_dict) for plot in plots]
        st.bokeh_chart(column(plot_list))


if __name__ == "__main__":
    write()
