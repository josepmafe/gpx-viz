import streamlit as st

LOAD_DATA_PAGES = [
    st.Page('pages/load_data.py', title='Load GPX data', icon=':material/upload_file:')
]
VISUALIZATION_DISABLED_PAGES = [
    st.Page('pages/empty.py', title='Empty', icon=':material/pending:')
]
VISUALIZATION_ENABLED_PAGES = [
    st.Page('pages/display_data.py', title='Display data', icon=':material/manage_search:'),
    st.Page('pages/slope_analysis.py', title='Slope analysis', icon=':material/query_stats:'),
    st.Page('pages/explore_map.py', title='Map explorer', icon=':material/travel_explore:')
]

def build_pages_dict(*, visualization_enabled: bool) -> dict[str, list[st.Page]]:
    pages_dict = {'Load data': LOAD_DATA_PAGES}
    
    if visualization_enabled:
        pages_dict['Visualization'] = VISUALIZATION_ENABLED_PAGES
    else:
        pages_dict['Visualization'] = VISUALIZATION_DISABLED_PAGES

    return pages_dict