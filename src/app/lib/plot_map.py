import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

ELEVATION_COLOR_SCALE = [
    "#1a9850",   # deep green (low elevation)
    "#66bd63",   # green
    "#d9ef8b",   # yellow-green
    "#fccf03",   # yellow
    "#fdae61",   # orange
    "#d73027",   # red / brownish
]

def plot_map(df: pd.DataFrame, map_style: str) -> go.Figure:
    map_fig = px.scatter_map(
        df,
        lat='latitude',
        lon='longitude',
        color='elevation',
        color_continuous_scale=ELEVATION_COLOR_SCALE,
        map_style=map_style,
        hover_data=['distance_km', 'elevation', 'elevation_gain', 'elevation_loss'],
        zoom=12.5,
        height=650
    )
    map_fig.update_traces(
        hovertemplate=(
            '<b>(%{lat:.6f}, %{lon:6f})</b><br>'
            '<br>Distance: %{customdata[0]:.2f} km'
            '<br>Elevation: %{customdata[1]:.2f} m'
            '<br>Elevation gain: %{customdata[2]:.2f} m'
            '<br>Elevation loss: %{customdata[3]:.2f} m'
            '<extra></extra>'
        )
    )
    map_fig.update_geos(
        fitbounds='locations'
    )
    return map_fig

def plot_simple_elevation(df: pd.DataFrame, hover_event) -> go.Figure:
    # Determine selected point index and compute marker sizes
    highlight_idx = hover_event[0][0]["pointIndex"] if hover_event[0] else None
    marker_sizes = [14 if i == highlight_idx else 2 for i in range(df.shape[0])]
    
    elev_fig = go.Figure(
        go.Scatter(
            x=df['distance_km'],
            y=df['elevation'],
            mode="lines+markers",
            marker=dict(
                size=marker_sizes,
                color=df['elevation'],
                colorscale=ELEVATION_COLOR_SCALE,
            ),
        )
    )
    elev_fig.update_layout(
        height=300,
        xaxis_title="Distance (km)",
        yaxis_title="Elevation (m)",
    )
    return elev_fig