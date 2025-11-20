import streamlit as st

from app.lib.data_enrichment import enrich_segment_df, DEFAULT_SLOPE_BINS, DEFAULT_SLOPE_LABEL2COLOR_MAP, SlopeCategories
from app.lib.plot_profile import plot_profile, CUSTOMDATA_FIELDS2SETTINGS_MAP
from app.lib.state_manager import SessionStateManager


slope_label2color_map = (
    SessionStateManager.get_slope_label2color_map() or DEFAULT_SLOPE_LABEL2COLOR_MAP.copy()
)
slope_bins = SessionStateManager.get_slope_bins() or DEFAULT_SLOPE_BINS.copy()


def set_distance_bin_size(default_fallback: int = 200) -> int:
    default_distance_bin_size = SessionStateManager.get_distance_bin_size() or default_fallback
    distance_bin_size = st.number_input(
        'Distance bin size', 
        min_value=100, 
        max_value=1_000, 
        value=default_distance_bin_size, 
        step=50
    )
    SessionStateManager.set_distance_bin_size(distance_bin_size)
    return distance_bin_size


def set_slope_color(slope_label: SlopeCategories):
    slope_label2color_map[slope_label] = st.color_picker(
        f'{slope_label} slope color', 
        value=slope_label2color_map[slope_label],
        width=200
    )

def set_slope_max_value(slope_label: SlopeCategories):
    idx = list(SlopeCategories).index(slope_label)
    slope_bins[idx + 1] = st.number_input(
        f'{slope_label} slope max value', 
        min_value=slope_bins[idx] + 1, 
        max_value=slope_bins[idx + 1], 
        value=slope_bins[idx + 1]
    )

with st.expander('Profile plot params'):
    col_1, _, col_3 = st.columns(3)
    with col_3:
        with st.container(horizontal_alignment='right'):
            button = st.button('Reset default params')
            if button:
                slope_label2color_map = DEFAULT_SLOPE_LABEL2COLOR_MAP
                slope_bins = DEFAULT_SLOPE_BINS.copy()

    with col_1:
        distance_bin_size = set_distance_bin_size()
    


    slope_categories = list(SlopeCategories)
    col_1, col_2 = st.columns(2)


    with col_1:
        with st.container(horizontal=True):
            slope_label = SlopeCategories.FLAT
            set_slope_color(slope_label)
            set_slope_max_value(slope_label)
    with col_2:
        with st.container(horizontal=True):
            slope_label = SlopeCategories.GENTLE
            set_slope_color(slope_label)
            set_slope_max_value(slope_label)
    
    with col_1:
        with st.container(horizontal=True):
            slope_label = SlopeCategories.MODERATE
            set_slope_color(slope_label)
            set_slope_max_value(slope_label)

    with col_2:
        with st.container(horizontal=True):
            slope_label = SlopeCategories.STEEP
            set_slope_color(slope_label)
            set_slope_max_value(slope_label)
    
    with col_1:
        with st.container(horizontal=True):
            slope_label = SlopeCategories.VERY_STEEP
            set_slope_color(slope_label)
            set_slope_max_value(slope_label)

    with col_2:
        with st.container(horizontal=True):
            slope_label = SlopeCategories.EXTREME
            set_slope_color(slope_label)
            set_slope_max_value(slope_label)

    # persist changes
    SessionStateManager.set_slope_label2color_map(slope_label2color_map)
    SessionStateManager.set_slope_bins(slope_bins)

with st.spinner('Generating profile plot...'):
    df = enrich_segment_df(
        st.session_state['gpx_df'], 
        distance_bin_size=distance_bin_size, 
        slope_labels=slope_label2color_map.keys(),
        slope_bins=slope_bins
    )
    profile_plot = plot_profile(
        df,
        track_name=st.session_state['gpx_track'].name,
        x_tick_delta=2, 
        customdata_fields=CUSTOMDATA_FIELDS2SETTINGS_MAP.keys(),
        slope_label2color_map=slope_label2color_map
    )
st.plotly_chart(profile_plot)

