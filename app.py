import streamlit as st

from src import plot_corner, plot_telemetry, homepage, plot_race, plot_speeds
from utils.utilities import write_page


def main():

    plotting_modules = {'Home': homepage,
                        'Telemetry': plot_telemetry,
                        'Corner': plot_corner,
                        'Speed Trap': plot_speeds,
                        "Make 'em Race": plot_race}

    with st.sidebar:
        plot_type = st.selectbox('Plot Type', options=plotting_modules.keys())

    if plot_type == 'Home':
        write_page(homepage)

    if plot_type == 'Telemetry':
        write_page(plot_telemetry)

    if plot_type == 'Corner':
        write_page(plot_corner)

    if plot_type == 'Speed Trap':
        write_page(plot_speeds)

    if plot_type == "Make 'em Race":
        write_page(plot_race)

    return


if __name__ == "__main__":
    main()
