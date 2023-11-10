import numpy as np
from scipy.stats.kde import gaussian_kde
import streamlit as st
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

from utils.utilities import race_picker_sidebar, get_session_data

# TODO show by team or by driver? (selectbox)
# TODO plot scatter of laps ontop of KDE
def write():
    year, track, session = race_picker_sidebar()
    event = get_session_data(year, track, session)

    drivers = event.laps['Driver'].unique().tolist()
    driver_speeds = {driver: [] for driver in drivers}

    for driver in drivers:
        dlaps = event.laps.pick_driver(driver)
        for index, row in dlaps.iterrows():
            if not np.isnan(row['SpeedST']):
                driver_speeds[driver].append(row['SpeedST'])

    x = np.linspace(0, 400, 401)

    def ridge(category, data, scale=20):
        return list(zip([category] * len(data), scale * data))

    source = ColumnDataSource(data=dict(x=x))

    p = figure(y_range=drivers, width=700, x_range=(0, 400))

    for i, driver in enumerate(drivers):
        pdf = gaussian_kde(driver_speeds[driver])
        y = ridge(driver, pdf(x))
        source.add(y, driver)
        team_color = event.get_driver(driver).TeamColor
        p.patch('x', driver, color=f"#{team_color}", alpha=0.6, line_color="black", source=source)

    st.bokeh_chart(p)


if __name__ == "__main__":
    write()
