import streamlit as st
import fastf1 as f1


def write_page(page):
    """Writes the specified page/module
	To take advantage of this function, a multipage app should be structured into sub-files with a `def write()` function
	Arguments:
		page {module} -- A module with a "def write():" function
	"""
    page.write()


def get_telemetry(event_obj, driver_name, lap_name):
    driver_laps = event_obj.laps.pick_driver(driver_name)

    if lap_name == 'fastest':
        single_lap = driver_laps.pick_fastest()
    else:
        single_lap = driver_laps[driver_laps['LapNumber'] == lap_name].iloc[0]

    telem = single_lap.get_telemetry().add_distance()
    return telem


def race_picker_sidebar():
    with st.sidebar:
        year = st.selectbox('Year', options=[n + 1 for n in range(2017, 2022)][::-1])
        calendar = f1.events.get_event_schedule(year)
        available_events = calendar['EventName'].to_list()
        track = st.selectbox('Track', options=available_events)

        session_list = ['Session1', 'Session2', 'Session3', 'Session4', 'Session5']
        available_sessions = [calendar[calendar['EventName'] == track][x].to_list()[0] for x in session_list]
        session = st.selectbox('Session', options=available_sessions)
        # use year/track/session to load available drivers
    return year, track, session


@st.cache()
def get_session_data(year, track, session):
    event = f1.get_session(year, track, session)
    event.load()
    return event
