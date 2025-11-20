import enum
import functools
from typing import Any

import streamlit as st


class StateKeys(enum.StrEnum):
    # data-loading related
    GPX_TRACK = enum.auto()
    GPX_SEGMENT = enum.auto()
    GPX_DF = enum.auto()

    # GPX-`processing related
    SLOPE_SMOOTHER_SPAN = enum.auto()
    DISTANCE_3D = enum.auto()

    # profile-analysis related
    DISTANCE_BIN_SIZE = enum.auto()
    SLOPE_BINS = enum.auto()
    SLOPE_LABEL2COLOR_MAP = enum.auto()


def add_keys_accessor_methods(cls: 'SessionStateManager'):
    for key in cls.state_keys:
        set_method = functools.partial(cls._set_param, name=key)
        setattr(cls, f'set_{key}', set_method)

        get_method = functools.partial(cls._get_param, name=key)
        setattr(cls, f'get_{key}', get_method)

    return cls
        

@add_keys_accessor_methods
class SessionStateManager:
    state_keys = StateKeys

    @classmethod
    def init_state(cls):
        for key in cls.state_keys:
            if key not in st.session_state:
                st.session_state[key] = None

    @classmethod
    def clear_state(cls):
        for key in cls.state_keys:
            st.session_state[key] = None

    @staticmethod
    def _set_param(value, name):
        st.session_state[name] = value

    @staticmethod
    def _get_param(name) -> Any:
        return st.session_state.get(name)
