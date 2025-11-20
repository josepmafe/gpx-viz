import gpxpy
import streamlit as st

from app.lib.data_processing import process_segment
from app.lib.navigation import build_pages_dict
from app.lib.state_manager import SessionStateManager
from app.lib.tip_box import tip_box


with st.container():
    gpx_file = st.file_uploader('Upload GPX file', type='gpx')
    
    if gpx_file is not None:
        gpx_obj = gpxpy.parse(gpx_file)

        gpx_track = st.selectbox(
            'Select GPX track', 
            options=gpx_obj.tracks,
            format_func=lambda t: t.name or "Unnamed track",
        )
        
        if gpx_track is not None:
            gpx_segment = st.selectbox(
                'Select track segment',
                options=gpx_track.segments,
                format_func=lambda segment: f'Segment with {len(segment.points)} points',
            )

        if gpx_segment is not None:
            with st.spinner('Processing segment data...'):
                gpx_df = process_segment(gpx_segment)

            st.success('GPX data processed successfully')

            # persist
            SessionStateManager.set_gpx_track(gpx_track)
            SessionStateManager.set_gpx_segment(gpx_segment)
            SessionStateManager.set_gpx_df(gpx_df)

            # update navigation
            gpx_file = None
            pages_dict = build_pages_dict(visualization_enabled=True)
            st.navigation(pages_dict)
    else:
        gpx_track = SessionStateManager.get_gpx_track()
        gpx_segment = SessionStateManager.get_gpx_segment()
        if gpx_track is not None and gpx_segment is not None:
            st.info(
                f'Track {gpx_track.name} is currently in memory, and its segment with '
                f'{len(gpx_segment.points)} is being used.'
            )

            with st.container(horizontal=True, horizontal_alignment='right'):
                button = st.button('Clear data', help='Remove the current data')
            if button:
                SessionStateManager.clear_state()
                st.rerun()
        else:
            tip_box('Upload your GPX file and start exploring')
