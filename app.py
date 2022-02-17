from cmath import isnan
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import dash_daq as daq

import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from datetime import datetime, date

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport",
                "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.SUPERHERO],update_title=None
)
server = app.server
app.title = "Vattenfall Smart Charging"


def logo(app):
    title = html.H5(
        "Vattenfall Smart Charging",
        style={"marginTop": 5, "marginLeft": "10px"},
    )

    info_about_app = html.H6(
        "Very important message about sustainability. GO green!",
        style={"marginLeft": "10px"}
    )

    logo_image = html.Img(src=app.get_asset_url(
        "VF_logo.png"), style={"height": 100})

    return dbc.Row([
        dbc.Col([
            dbc.Row([title]),
            dbc.Row([info_about_app])],
            width={'size': 3}),
        dbc.Col([logo_image], width={'size': 2})], justify='between'
    )


#  get data from csv
df = pd.read_csv('./assets/data.csv')
format = "%Y-%m-%d %I:%M %p"
df['Interval'] = df['Interval'].apply(lambda x: datetime.strptime(x, format))
df['Interval (UTC)'] = df['Interval (UTC)'].apply(
    lambda x: datetime.strptime(x, format))


graphs = dbc.Card(
    children=[
        dbc.CardBody(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id="Main-Graph",
                            figure={
                                "layout": {
                                    "margin": {"t": 30, "r": 35, "b": 40, "l": 50},
                                    "xaxis": {
                                        "dtick": 5,
                                        "gridcolor": "#636363",
                                        "showline": False,
                                    },
                                    "yaxis": {"showgrid": False, "showline": False},
                                    "plot_bgcolor": "black",
                                    "paper_bgcolor": "black",
                                    "font": {"color": "gray"},
                                },
                            },
                            config={"displayModeBar": False},
                        ),
                        html.Pre(id="update-on-click-data"),
                    ],
                    style={"width": "98%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        dcc.DatePickerRange(
                            id="date-picker",
                            min_date_allowed=pd.Series.min(df['Interval']),
                            max_date_allowed=pd.Series.max(df['Interval']),
                            # min_date_allowed=date(2000, 5, 1),
                            # max_date_allowed=date.today(),
                            initial_visible_month=date.today(),
                            start_date_placeholder_text="Start Period",
                            end_date_placeholder_text="End Period",
                            calendar_orientation="vertical",
                        ),
                        html.Div(id="output-container-date-picker-range"),
                    ],
                    style={
                        "vertical-align": "top",
                        "position": "absolute",
                        "right": "3%",
                        "float": "right",
                        "display": "inline-block",
                        "color": "black",
                    },
                ),
            ],
            style={
                "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        )
    ]  # , outline=False
)

info_box = dbc.Card(
    children=[
        dbc.CardBody(
            [
                html.Div(
                    dcc.Textarea(
                        id="Info-Textbox",
                        placeholder="This field is used to display information about a feature displayed "
                        "on the graph.",
                        rows=8,
                        style={
                            "width": "100%",
                            "height": "100%",
                            "background-color": "black",
                            "color": "#fec036",
                            "placeholder": "#fec036",
                            "fontFamily": "Arial",
                            "fontSize": "16",
                            "display": "inline-block",
                        },
                    )
                )
            ],
            style={
                "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        ),
    ],
)

flowView = html.Div(
    children=[
        html.Div(
            id="horizontalArrowAnim1",
            children=[
                html.Div(
                    className="horizontalArrowSliding",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    className="horizontalArrowSliding delay1",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    className="horizontalArrowSliding delay2",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    className="horizontalArrowSliding delay3",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    className="horizontalArrowSliding delay4",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    className="horizontalArrowSliding delay5",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    className="horizontalArrowSliding delay6",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    className="horizontalArrowSliding delay7",
                    children=[
                        html.Div(className="arrow1")
                    ],
                )
            ],
        ),
        html.Div(
            id="horizontalArrowAnim2",
            children=[
                html.Div(
                    className="horizontalArrowSliding",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    className="horizontalArrowSliding delay1",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    className="horizontalArrowSliding delay2",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    className="horizontalArrowSliding delay3",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    className="horizontalArrowSliding delay4",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    className="horizontalArrowSliding delay5",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    className="horizontalArrowSliding delay6",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    className="horizontalArrowSliding delay7",
                    children=[
                        html.Div(className="arrow1")
                    ],
                )
            ],
        )
    ]
)

hills = html.Div(
    children=[
        html.Div(className="hills1"),
        html.Div(className="hills2"),
    ]
)

windmillView = html.Div(
    className="windmill",
    children=[
        html.Div(
            id="battery",
            children=[html.Div(id="battery-fill")],
        ),
        html.Div(className="house"),
        html.Div(className="mill"),
        html.Div(className="roof"),
        html.Div(
            className="wheel",
            children=[
                html.Div(className="windwheel"),
                html.Div(className="windwheel windwheel2"),
                html.Div(className="windwheel windwheel3"),
                html.Div(className="windwheel windwheel4"),
            ]
        ),

    ],
)

# where everything gets put into the page
app.layout = dbc.Container(
    fluid=True,
    children=[
        logo(app),
        hills,
        graphs,
        windmillView,
        flowView,
        dcc.Interval(
            id='interval-component',
            interval=1*100,  # in milliseconds
            n_intervals=1
        )
    ],
)


def fig_update_layout(fig):
    fig.update_layout(
        xaxis=dict(
            showline=False,
            showgrid=False,
            showticklabels=True,
            zeroline=False,
            gridcolor="#636363",
            linecolor="rgb(204, 204, 204)",
            linewidth=2,
            tickfont=dict(family="Arial", size=12, color="white",),
            title=dict(font=dict(family="Arial", size=24, color="#fec036"),),
        ),
        yaxis=dict(
            showline=False,
            showgrid=False,
            showticklabels=True,
            zeroline=False,
            gridcolor="#636363",
            linecolor="rgb(204, 204, 204)",
            linewidth=2,
            tickfont=dict(family="Arial", size=12, color="white",),
            title=dict(font=dict(family="Arial", size=24, color="#fec036"),),
        ),
        autosize=True,
        margin=dict(autoexpand=True, l=50, b=40, r=35, t=30),
        showlegend=False,
        paper_bgcolor="black",
        plot_bgcolor="black",
        title=dict(
            font=dict(family="Arial", size=32, color="darkgray"),
            xanchor="center",
            yanchor="top",
            y=1,
            x=0.5,
        ),
    )
    return fig


@app.callback(

    Output("battery_fill", "style"),

    [
        Input('interval-component', 'n_intervals'),
    ],
)
def update_battery_level(index):
    index = (index*10) % 1000
    level = df.iloc[index,3] 
    return {'height': str(level*25)+'rem'}

@app.callback(
        Output("Main-Graph", "figure"),
    [
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date"),
        Input('interval-component', 'n_intervals'),
    ],
)
def update_graph_timer(start_date, end_date, index):
    df.style
    # print(index)
    index = (index*10) % 1000
    if index == 0:
        index = 1
    tmp_data = df.iloc[0:index, 3]
    information_update = (
        "test for when it is updated, index = " + str(index)
    )
    fig = go.Figure(
        data=[
            go.Scatter(
                x=df.iloc[0:index, 1],
                y=tmp_data*100
            )
        ]
    )
    fig = fig_update_layout(fig)
    return fig


if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=True)
