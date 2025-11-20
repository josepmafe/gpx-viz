import enum
import numpy as np
import pandas as pd

class SlopeCategories(enum.StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.replace('_', ' ').title()
    
    FLAT = enum.auto()
    GENTLE = enum.auto()
    MODERATE = enum.auto()
    STEEP = enum.auto()
    VERY_STEEP = enum.auto()
    EXTREME = enum.auto()
    

DEFAULT_SLOPE_BINS = [0, 3, 8, 15, 30, 50, 100]
DEFAULT_SLOPE_LABEL2COLOR_MAP = {
    SlopeCategories.FLAT: '#06E206',
    SlopeCategories.GENTLE: '#1B964F',
    SlopeCategories.MODERATE: '#F1C40F',
    SlopeCategories.STEEP: '#E67E22',
    SlopeCategories.VERY_STEEP: '#E8321E',
    SlopeCategories.EXTREME: '#8B0000',
}

def enrich_segment_df(
    df: pd.DataFrame, 
    *, 
    distance_bin_size: int,
    slope_labels: list[str],
    slope_bins: list[int]
) -> pd.DataFrame:
    df['abs_slope'] = df['slope'].abs()

    distance_bins = np.arange(0, df['distance'].max() + distance_bin_size, distance_bin_size)
    df['distance_bin'] = pd.cut(df['distance'], distance_bins)
    df['mean_slope'] = df.groupby('distance_bin', observed=False)['abs_slope'].transform('mean')

    df['slope_bin'] = pd.cut(
        df['mean_slope'], slope_bins, right=False
    )
    df['slope_label'] = pd.cut(
        df['mean_slope'], slope_bins, right=False, labels=slope_labels
    )
    
    return df