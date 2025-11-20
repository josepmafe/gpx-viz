import streamlit as st

from app.lib.navigation import build_pages_dict
from app.lib.state_manager import SessionStateManager


SessionStateManager.init_state()
st.set_page_config(page_title='GPX viewer', layout='wide')

visualization_enabled = (st.session_state['gpx_df'] is not None)
pages_dict = build_pages_dict(visualization_enabled=visualization_enabled)
pg = st.navigation(pages_dict)
pg.run()
