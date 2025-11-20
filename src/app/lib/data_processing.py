import itertools

import gpxpy.gpx
import numpy as np
import pandas as pd


# @st.cache_data
def process_segment(segment: gpxpy.gpx.GPXTrackSegment, *, distance_3d: bool = True, slope_smoother_span: int = 1) -> pd.DataFrame:
    df = pd.DataFrame({
        'latitude': (p.latitude for p in segment.points),
        'longitude': (p.longitude for p in segment.points),
        'p2p_distance': point2point_distance(segment.points, distance_3d=distance_3d),
        'elevation': (p.elevation for p in segment.points),
    })

    df['p2p_elevation'] = df['elevation'].diff()
    df['p2p_slope'] = (df['p2p_elevation'] / df['p2p_distance']) * 100

    df['distance'] = df['p2p_distance'].cumsum()
    df['distance_km'] = df['distance'] / 1_000
    df['slope'] = df['p2p_slope'].ewm(span=slope_smoother_span, min_periods=1).mean()
    df['elevation_gain'] = df['p2p_elevation'].clip(lower=0, upper=None).cumsum()
    df['elevation_loss'] = df['p2p_elevation'].clip(lower=None, upper=0).cumsum()

    return df


def get_df_info(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        'Column': df.columns,
        'Null Count': df.isna().sum(),
        'Non-null Count': df.shape[0] - df.isna().sum(),
        'Dtype': df.dtypes.apply(lambda x: str(x))
    }).reset_index(drop=True)


def point2point_distance(points: list[gpxpy.gpx.GPXTrackPoint], *, distance_3d: bool = True) -> np.ndarray:
    point_pairs = itertools.pairwise(points)
    if distance_3d:
        p2p_distance = map(lambda p: p[0].distance_3d(p[1]), point_pairs)
    else:
        p2p_distance = map(lambda p: p[0].distance_2d(p[1]), point_pairs)

    return np.insert(np.fromiter(p2p_distance, dtype=float), 0, np.nan)