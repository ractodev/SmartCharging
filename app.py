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
import pickle

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport",
                "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.SUPERHERO],
)
server = app.server
app.title = "Vattenfall Smart Charging"
index = 0


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

    # what does it do? links over other resources
    # link_btns = html.Div(
    #     style={"float": "right"},
    #     children=[
    #         html.A(
    #             dbc.Button("Enterprise Demo", color="primary", className="mr-1",),
    #             href="https://plotly.com/get-demo/",
    #             target="_blank",
    #         ),
    #         html.A(
    #             dbc.Button("Source Code", color="secondary", className="mr-1"),
    #             href="https://github.com/plotly/dash-sample-apps/tree/main/apps/dash-turbine-maintenance",
    #             target="_blank",
    #         ),
    #         html.A(
    #             logo_image,
    #             href="https://plotly.com/dash/",
    #             style={"margin-left": "15px"},
    #         ),
    #     ],
    # )

    return dbc.Row([
        dbc.Col([
            dbc.Row([title]),
            dbc.Row([info_about_app])],
            width={'size': 3}),
        dbc.Col([logo_image], width={'size': 2})], justify='between'
    )


#  get data from csv
df = pd.read_csv('/media/leonardo/SharedVolume/Code/VSC/assets/data.csv')
format = "%Y-%m-%d %I:%M %p"
df['Interval'] = df['Interval'].apply(lambda x: datetime.strptime(x, format))
df['Interval (UTC)'] = df['Interval (UTC)'].apply(lambda x: datetime.strptime(x, format))
# print(df)
# df, df_button, x_test, y_test = data_preprocessing()

# predict_button = dbc.Card(
#     className="mt-auto",
#     children=[
#         dbc.CardBody(
#             [
#                 html.Div(
#                     [
#                         dbc.Button(
#                             "Predict",
#                             id="predict-button",
#                             color="#fec036",
#                             size="lg",
#                             style={"color": "#fec036"},
#                         ),
#                     ]
#                 )
#             ],
#             style={
#                 "text-align": "center",
#                 "backgroundColor": "black",
#                 "border-radius": "1px",
#                 "border-width": "5px",
#                 "border-top": "1px solid rgb(216, 216, 216)",
#                 "border-left": "1px solid rgb(216, 216, 216)",
#                 "border-right": "1px solid rgb(216, 216, 216)",
#                 "border-bottom": "1px solid rgb(216, 216, 216)",
#             },
#         )
#     ],
# )

# get_new_information_button = dbc.Card(
#     className="mt-auto",
#     children=[
#         dbc.CardBody(
#             [
#                 html.Div(
#                     [
#                         dbc.Button(
#                             "Get New Data",
#                             id="get-new-info-button",
#                             color="#fec036",
#                             size="lg",
#                             style={"color": "#fec036"},
#                         ),
#                     ]
#                 )
#             ],
#             style={
#                 "text-align": "center",
#                 "backgroundColor": "black",
#                 "border-radius": "1px",
#                 "border-width": "5px",
#                 "border-top": "1px solid rgb(216, 216, 216)",
#                 "border-left": "1px solid rgb(216, 216, 216)",
#                 "border-right": "1px solid rgb(216, 216, 216)",
#                 "border-bottom": "1px solid rgb(216, 216, 216)",
#             },
#         )
#     ],
# )


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
                # html.Div(
                #     [
                #         dcc.Dropdown(
                #             id="feature-dropdown",
                #             options=[
                #                 {"label": label, "value": label} for label in df.columns
                #             ],
                #             value="",
                #             multi=False,
                #             searchable=False,
                #         )
                #     ],
                #     style={
                #         "width": "33%",
                #         "display": "inline-block",
                #         "color": "black",
                #     },
                # ),
                html.Div(
                    [
                        dcc.DatePickerRange(
                            id="date-picker",
                            min_date_allowed= pd.Series.min(df['Interval']),
                            max_date_allowed= pd.Series.max(df['Interval']),
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

# rul_estimation_indicator = dbc.Card(
#     children=[
#         dbc.CardHeader(
#             "System RUL Estimation (days)",
#             style={
#                 "text-align": "center",
#                 "color": "white",
#                 "backgroundColor": "black",
#                 "border-radius": "1px",
#                 "border-width": "5px",
#                 "border-top": "1px solid rgb(216, 216, 216)",
#             },
#         ),
#         dbc.CardBody(
#             [
#                 daq.LEDDisplay(
#                     id="rul-estimation-indicator-led",
#                     size=24,
#                     color="#fec036",
#                     style={"color": "#black"},
#                     backgroundColor="#2b2b2b",
#                     value="0.0",
#                 )
#             ],
#             style={
#                 "text-align": "center",
#                 "backgroundColor": "black",
#                 "border-radius": "1px",
#                 "border-width": "5px",
#                 "border-top": "1px solid rgb(216, 216, 216)",
#             },
#         ),
#     ]
# )

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

blade_angle_display = dbc.Card(
    children=[
        dbc.CardHeader(
            "charge port 1",
            style={
                "text-align": "center",
                "color": "white",
                "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        ),
        dbc.CardBody(
            [
                html.Div(
                    daq.Gauge(
                        id="charge port 1",
                        min=0,
                        max=100,
                        # min=min(df["WEC: ava. blade angle A"]),
                        # max=max(
                        #     df["WEC: ava. blade angle A"]
                        # ),  # This one should be the theoretical maximum
                        value=0,
                        showCurrentValue=True,
                        color="#fec036",
                        style={
                            "align": "center",
                            "display": "flex",
                            "marginTop": "5%",
                            "marginBottom": "-10%",
                        },
                    ),
                    className="m-auto",
                    style={
                        "display": "flex",
                        "backgroundColor": "black",
                        "border-radius": "1px",
                        "border-width": "5px",
                    },
                )
            ],
            className="d-flex",
            style={
                "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        ),
    ],
    style={"height": "95%"},
)

active_power_display = dbc.Card(
    children=[
        dbc.CardHeader(
            "charge port 2",
            style={
                "text-align": "center",
                "color": "white",
                "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        ),
        dbc.CardBody(
            [
                html.Div(
                    daq.Gauge(
                        id="charge port 2",
                        min=0,
                        max=100,
                        # min=min(df["WEC: ava. Power"]),
                        # max=max(
                        #     df["WEC: ava. Power"]
                        # ),  # This one should be the theoretical maximum
                        value=50,
                        showCurrentValue=True,
                        color="#fec036",
                        style={
                            "align": "center",
                            "display": "flex",
                            "marginTop": "5%",
                            "marginBottom": "-10%",
                        },
                    ),
                    className="m-auto",
                    style={
                        "display": "flex",
                        "backgroundColor": "black",
                        "border-radius": "1px",
                        "border-width": "5px",
                    },
                )
            ],
            className="d-flex",
            style={
                "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        ),
    ],
    style={"height": "95%"},
)

active_power_from_wind_display = dbc.Card(
    children=[
        dbc.CardHeader(
            "charge port 3",
            style={
                "display": "inline-block",
                "text-align": "center",
                "color": "white",
                "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        ),
        dbc.CardBody(
            [
                html.Div(
                    daq.Gauge(
                        id="charge port 3",
                        min=0,
                        max=100,
                        # min=min(df["WEC: ava. available P from wind"]),
                        # max=max(df["WEC: ava. available P from wind"]),
                        value=10,
                        showCurrentValue=True,
                        color="#fec036",
                        style={
                            "align": "center",
                            "display": "flex",
                            "marginTop": "5%",
                            "marginBottom": "-10%",
                        },
                    ),
                    className="m-auto",
                    style={
                        "display": "flex",
                        "backgroundColor": "black",
                        "border-radius": "1px",
                        "border-width": "5px",
                    },
                )
            ],
            className="d-flex",
            style={
                "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        ),
    ],
    style={"height": "95%"},
)

wind_speed_information = dbc.Card(
    className="mt-auto",
    children=[
        dbc.CardHeader(
            "charge port 4",
            style={
                "text-align": "center",
                "color": "white",
                "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        ),
        dbc.CardBody(
            [
                html.Div(
                    daq.Gauge(
                        id="charge port 4",
                        min=0,
                        max=100,
                        # min=min(df["WEC: ava. windspeed"]),
                        # max=int(max(df["WEC: ava. windspeed"])),
                        value=0,
                        showCurrentValue=True,
                        color="#fec036",
                        style={
                            "align": "center",
                            "display": "flex",
                            "marginTop": "5%",
                            "marginBottom": "-10%",
                        },
                    ),
                    className="m-auto",
                    style={
                        "display": "flex",
                        "backgroundColor": "black",
                        "border-radius": "1px",
                        "border-width": "5px",
                    },
                )
            ],
            className="d-flex",
            style={
                "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        ),
    ],
    style={"height": "95%"},
)

reactive_power_display = dbc.Card(
    className="mt-auto",
    children=[
        dbc.CardHeader(
            "charge port 5",
            style={
                "text-align": "center",
                "color": "white",
                "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        ),
        dbc.CardBody(
            [
                html.Div(
                    daq.Gauge(
                        id="charge port 5",
                        min=0,
                        max=100,
                        # min=min(df["WEC: ava. reactive Power"]),
                        # max=max(df["WEC: ava. reactive Power"]),
                        value=0,
                        showCurrentValue=True,
                        color="#fec036",
                        style={
                            "align": "center",
                            "display": "flex",
                            "marginTop": "5%",
                            "marginBottom": "-10%",
                        },
                    ),
                    className="m-auto",
                    style={
                        "display": "flex",
                        "backgroundColor": "black",
                        "border-radius": "1px",
                        "border-width": "5px",
                    },
                )
            ],
            className="d-flex",
            style={
                "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        ),
    ],
    style={"height": "95%"},
)

# windmill = html.Iframe(src="https://codepen.io/wolf019/embed/OJOpeGV",
#                        style={"height":"1000", "width": "100%", "scrolling":"no", "frameborder":"no", "loading":"lazy", "allowtransparency":"true", "allowfullscreen":"true"})
# <iframe height="300" style="width: 100%;" scrolling="no" title="Codevember: pure CSS windmill" src="https://codepen.io/wolf019/embed/OJOpeGV?default-tab=html%2Cresult" frameborder="no" loading="lazy" allowtransparency="true" allowfullscreen="true">
#   See the Pen <a href="https://codepen.io/wolf019/pen/OJOpeGV">
#   Codevember: pure CSS windmill</a> by Tom Axberg (<a href="https://codepen.io/wolf019">@wolf019</a>)
#   on <a href="https://codepen.io">CodePen</a>.
# </iframe>

gauge_size = "auto"
# where everything gets put into the page
app.layout = dbc.Container(
    fluid=True,
    children=[
        logo(app),
        # windmill,
        dbc.Row(
            [
                dbc.Col(graphs, xs=10, md=10, lg=10, width=10),
                dbc.Col(
                    [
                        dbc.Row(
                            dbc.Col(
                                xs=12, md=12, lg=12, width=12
                                # rul_estimation_indicator, xs=12, md=12, lg=12, width=12
                            )
                        ),
                        dbc.Row(dbc.Col(info_box, xs=12,
                                        md=12, lg=12, width=12)),
                        dbc.Row(
                            dbc.Col(
                                # get_new_information_button,
                                xs=12,
                                md=12,
                                lg=12,
                                width=12,
                            )
                        ),
                        dbc.Row(dbc.Col(xs=12, md=12, lg=12, width=12)),
                        # dbc.Row(dbc.Col(predict_button, xs=12, md=12, lg=12, width=12)),
                    ]
                ),
            ],
            justify="start",
            style={"display": "flex", "marginBottom": "-3%"},
        ),
        dbc.Row(
            [
                dbc.Col(
                    active_power_display,
                    xs=gauge_size,
                    md=gauge_size,
                    lg=gauge_size,
                    width=gauge_size,
                ),
                dbc.Col(
                    active_power_from_wind_display,
                    xs=gauge_size,
                    md=gauge_size,
                    lg=gauge_size,
                    width=gauge_size,
                ),
                dbc.Col(
                    reactive_power_display,
                    xs=gauge_size,
                    md=gauge_size,
                    lg=gauge_size,
                    width=gauge_size,
                ),
                dbc.Col(
                    wind_speed_information,
                    xs=gauge_size,
                    md=gauge_size,
                    lg=gauge_size,
                    width=gauge_size,
                ),
                dbc.Col(
                    blade_angle_display,
                    xs=gauge_size,
                    md=gauge_size,
                    lg=gauge_size,
                    width=gauge_size,
                ),
            ],
            style={"marginTop": "3%"},
        ),
        dcc.Interval(
            id='interval-component',
            interval=1*100, # in milliseconds
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

# @app.callback(
#     [
#         Output("Main-Graph", "figure"),
#         Output("Info-Textbox", "value"),
#         # Output("charge port 2", "value"),
#         # Output("date-picker", "initial_visible_month"),
#     ],
#     [
#         Input("date-picker", "start_date"),
#         Input("date-picker", "end_date"),
#     ],
# )
# def update_graph(start_date, end_date):
#     if start_date is None or end_date is None:
#         start_date = "2021-11-03"
#         end_date = "2021-11-06"
#     # print(start_date)
#     # print(end_date)
#     start_date_object = datetime.strptime(start_date, "%Y-%m-%d")
#     end_date_object = datetime.strptime(end_date, "%Y-%m-%d")
#     mask = (df['Interval'] > start_date_object) & (df['Interval'] <= end_date_object)
#     # print(mask)
#     df_within_dates = df.loc[mask]
#     # print(df_within_dates)
#     information_update = (
#         "test for when it is updated, start date is " + str(start_date) + ", end date is : " + str(end_date)
#     )
#     fig = go.Figure(
#         data=[
#             go.Scatter(
#                 x=df_within_dates['Interval'],
#                 y=df_within_dates['ams-a-control-in-stateOfCharge/AvgValue.avg'],
#             )
#         ]
#     )
#     # bat = int(df_within_dates.iloc[-1]*100)
#     fig = fig_update_layout(fig)
#     return fig, information_update

@app.callback(
    [
        Output("Main-Graph", "figure"),
        Output("Info-Textbox", "value"),
        Output("charge port 2", "value"),
    ],
    [
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date"),
        Input('interval-component', 'n_intervals'),
    ],
)
def update_graph_timer(start_date, end_date, index):
    df.style
    # print(index)
    index = index % 1000
    if index == 0: 
        index = 1
    tmp_data = df.iloc[0:index, 3]
    information_update = (
        "test for when it is updated, index = " + str(index)
    )
    fig = go.Figure(
        data=[
            go.Scatter(
                x=df.iloc[0:index,1],
                y=tmp_data*100
            )
        ]
    )
    bat = int(tmp_data.iloc[index-1]*100)
    # print(bat)
    index = (index +1)%1000
    fig = fig_update_layout(fig)
    return fig, information_update, bat



@app.callback(
    [
        Output("active-power-information-gauge", "value"),
        Output("active-power-from-wind-information-gauge", "value"),
        Output("wind-power-information-gauge", "value"),
        Output("reactive-power-information-gauge", "value"),
        Output("blade-angle-information-gauge", "value"),
    ],
    Input("Main-Graph", "clickData"),
)
def display_click_data(clickData):
    if clickData:
        data_time = clickData["points"][0]["x"]
        value_active_power = df["WEC: ava. Power"].loc[df.index ==
                                                       data_time].values[0]
        value_active_power_wind = (
            df["WEC: ava. available P from wind"].loc[df.index == data_time].values[0]
        )
        value_reactive_power = (
            df["WEC: ava. reactive Power"].loc[df.index == data_time].values[0]
        )
        value_wind_speed = (
            df["WEC: ava. windspeed"].loc[df.index == data_time].values[0]
        )
        value_blade_angle = (
            df["WEC: ava. blade angle A"].loc[df.index == data_time].values[0]
        )
        return (
            value_active_power,
            value_active_power_wind,
            value_wind_speed,
            value_reactive_power,
            value_blade_angle,
        )
    else:
        value_active_power = 0
        value_active_power_wind = 0
        value_reactive_power = 0
        value_wind_speed = 0
        value_blade_angle = 0
        return (
            value_active_power,
            value_active_power_wind,
            value_wind_speed,
            value_reactive_power,
            value_blade_angle,
        )


if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=True)
