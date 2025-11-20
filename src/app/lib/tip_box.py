
import streamlit as st


def tip_box(text, *, show_icon: bool = True):
    icon_str = '<span style="font-size: 1.2rem; line-height: 1.4rem;">💡</span>'
    st.markdown(
        f"""
        <div style="
            padding: 1rem;
            border-radius: 0.5rem;
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1rem;
            background-color: rgba(155, 81, 224, 0.12);   /* light purple bg */
            color: rgb(155, 81, 224);                    /* text + icon */
        ">
            {icon_str if show_icon else '<span></span>'}
            <div>{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
