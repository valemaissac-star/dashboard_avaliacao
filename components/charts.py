import plotly.graph_objects as go
from config.theme import template

def grafico_ranking_h(df, col_y, col_x, titulo, colorscale="Plasma", height=500):
    top = df.head(20)
    fig = go.Figure(data=[go.Bar(
        y=top[col_y],
        x=top[col_x],
        orientation='h',
        text=top[col_x].round(2),
        textposition='outside',
        textfont=dict(size=14, color="#ffffff"),
        marker=dict(
            color=top[col_x],
            colorscale=colorscale,
            showscale=True,
            colorbar=dict(title='Score', tickfont=dict(size=13)),
            line=dict(color="rgba(255, 255, 255, 0.1)", width=1)
        ),
    )])
    fig.update_layout(
        template(),
        title=titulo,
        height=height,
        xaxis=dict(title="Score Final", tickfont=dict(size=13)),
        yaxis=dict(tickfont=dict(size=13), autorange="reversed"),
    )
    return fig