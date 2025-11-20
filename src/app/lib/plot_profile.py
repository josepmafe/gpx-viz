import pandas as pd
import plotly.graph_objects as go


CUSTOMDATA_FIELDS2SETTINGS_MAP = {
    'slope': (1, '%'),
    'mean_slope': (1, '%'),
    'elevation_gain': (2, ' m'),
    'elevation_loss': (2, ' m'),
}

def plot_profile(
    df: pd.DataFrame,
    track_name: str,
    x_tick_delta: int,
    customdata_fields: list[str],
    slope_label2color_map: dict[str, str],
) -> go.Figure:
    
    fig = go.Figure()
    hovertemplate = build_hovertemplate(customdata_fields)
    slope_label2rank_map = dict(zip(slope_label2color_map, range(len(slope_label2color_map))))

    legend_labels = set()
    for _, group_df in df.groupby('distance_bin', observed=False):
        label = group_df['slope_label'].unique()[0]
        color = slope_label2color_map[label]

        show_legend_flag = (label not in legend_labels)
        legend_labels.add(label)

        fig.add_trace(
            go.Scatter(
                x=group_df['distance_km'], 
                y=group_df['elevation'],
                mode='lines',
                line=dict(color=color),
                fill='tozeroy',
                fillcolor=color,
                legendgroup='slope',
                legendrank=slope_label2rank_map[label],
                name=label,
                showlegend=show_legend_flag,
                customdata=group_df[customdata_fields],
                hovertemplate=hovertemplate,
            ),
        )

    max_x_tick = df['distance_km'].max()
    x_ticks = [*range(0, int(max_x_tick) + 1, x_tick_delta), max_x_tick.round(2)]
    fig.update_layout(
        title=f'{track_name} slope analysis',
        paper_bgcolor='white',
        plot_bgcolor='white',
        legend_title_text='Slope Category',
        xaxis=dict(
            title='Distance (km)',
            tickvals=x_ticks,
        ),
        yaxis=dict(
            title='Elevation (m)',
            range=[df['elevation'].min() * .99, df['elevation'].max() * 1.01]
        ),
    )

    return fig


def build_hovertemplate(customdata_fields: list[str]) -> str:
    hovertemplate = (
        'Distance: %{x:.2f} km<br>'
        'Elevation: %{y:.2f} m'
    )

    for field_idx, field in enumerate(customdata_fields):
        precision, unit = CUSTOMDATA_FIELDS2SETTINGS_MAP[field]
        customdata_field = '{' + f'customdata[{field_idx}]:.{precision}f' + '}'
        field_name = field.replace('_', ' ').title()
        hovertemplate += f'<br>{field_name}: %{customdata_field}{unit}'

    return hovertemplate