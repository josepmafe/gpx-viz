
import streamlit as st
from app.lib.data_processing import process_segment, get_df_info
from app.lib.state_manager import SessionStateManager


def set_slope_smoother_span(default_fallback: int = 1) -> int:
    default_slope_smoother_span = (
        SessionStateManager.get_slope_smoother_span() or default_fallback
    )
    slope_smoother_span = st.number_input(
        'Slope smoother span',
        min_value=1,
        max_value=20,
        value=default_slope_smoother_span,
        help=(
            'The span for the EWM used when computing the slope. '
            'Set it to 1 for no smoothing on the slope'
        ),
    )
    SessionStateManager.set_slope_smoother_span(slope_smoother_span)
    return slope_smoother_span


def set_distance_3d_flag(default_fallback: bool = True) -> bool:
    default_distance_3d = SessionStateManager.get_distance_3d() or default_fallback
    distance_3d = st.checkbox(
        'Distance 3D', 
        value=default_distance_3d, 
        help='Whether to compute the distance between points in 2D or 3D'
    )
    SessionStateManager.set_distance_3d(distance_3d)
    return distance_3d


with st.expander('GPX data processing params'):
    col_1, col_2, col_3 = st.columns(3)
    with col_1:
        with st.container(horizontal_alignment='left'):
            slope_smoother_span = set_slope_smoother_span()

    with col_2:
        with st.container(horizontal_alignment='right', vertical_alignment='bottom'):
            distance_3d = set_distance_3d_flag()

    with col_3:
        with st.container(horizontal_alignment='right', vertical_alignment='bottom'):
            button = st.button('Recompute', help='Run again the GPX data processing using the given params')

        if button:
            st.session_state['gpx_df'] = process_segment(
                st.session_state['gpx_segment'], 
                distance_3d=distance_3d, 
                slope_smoother_span=slope_smoother_span
            )

df = st.session_state['gpx_df']
metadata, raw_data, stats_data = st.tabs(
    [':material/info: Meta data', ':material/table_view: Raw data', ':material/insights: Stats data'],
    default=':material/table_view: Raw data'
)

with metadata:
    st.dataframe(get_df_info(df))

with raw_data:
    n_rows = df.shape[0]
    with st.container(horizontal=True, horizontal_alignment='right'):
        min_row_idx = st.number_input('Min row idx', min_value=0, max_value=(n_rows - 1), step=5)
        max_row_idx = st.number_input('Max row idx', min_value=(min_row_idx + 10), max_value=n_rows, step=5)
    st.dataframe(df.iloc[min_row_idx:max_row_idx])

with stats_data:
    with st.container(horizontal=True, horizontal_alignment='right'):
        percentiles_allowed = [0.01, 0.05, 0.1, 0.9, 0.95, 0.99]
        percentiles = st.multiselect('Other percentiles', percentiles_allowed, default=None)
        if not percentiles:
            percentiles = None
    st.dataframe(df.describe(percentiles=percentiles))


