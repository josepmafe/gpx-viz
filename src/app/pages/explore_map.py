import enum

import streamlit as st
from streamlit_plotly_mapbox_events import plotly_mapbox_events

from app.lib.plot_map import plot_map, plot_simple_elevation


class ScatterMapStyles(enum.StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
       return name.replace('_', '-').lower()
    
    OPEN_STREET_MAP = enum.auto()
    OUTDOORS = enum.auto()
    SATELLITE = enum.auto()
    SATELLITE_STREETS = enum.auto()

gpx_df = st.session_state['gpx_df']

fig_col, select_col = st.columns([5, 1], gap='small')
with select_col:
    map_style = st.selectbox('Map style', ScatterMapStyles, index=2, format_func=lambda x: x.replace('-', ' ').title())

with fig_col:
    map_fig = plot_map(gpx_df, map_style=map_style)
    hover_event = plotly_mapbox_events(
        map_fig,
        click_event=False,
        select_event=False,
        hover_event=True,
    )

elev_fig = plot_simple_elevation(gpx_df, hover_event=hover_event)
st.plotly_chart(elev_fig, width=1200)