from turtle import width
import pandas as pd
import numpy as np
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import dash_daq as daq

import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from datetime import datetime, date
from dash.exceptions import PreventUpdate

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport",
                "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.SUPERHERO], update_title=None,
)
server = app.server
app.title = "Vattenfall Smart Charging"
width_data_points = 10
speed = 500

################ Functions definition ######################
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
    [
        Output('car_0_0', 'style'),
        Output('car_0_1', 'style'),
        Output('car_1_0', 'style'),
        Output('car_1_1', 'style'),
        Output('car_2_0', 'style'),
        Output('car_2_1', 'style'),
        Output('car_3_0', 'style'),
        Output('car_3_1', 'style'),
        Output('car_4_0', 'style'),
        Output('car_4_1', 'style'),
        Output('car_5_0', 'style'),
        Output('car_5_1', 'style'),
        Output('car_6_0', 'style'),
        Output('car_6_1', 'style'),
        Output('car_7_0', 'style'),
        Output('car_7_1', 'style'),
    ],
    [
        Input('interval-component', 'n_intervals'),
    ]
)
def update_cars(index):
    index = (index*width_data_points) %1000
    cars_connected_avg = df.iloc[:, -48::3]
    output = list()
    for i in range(0,16):
        car_i = cars_connected_avg.iloc[index,i]
        # print(str(car_i)+"index :"+str(index))
        if car_i != 0.0:
            output.append({'background-color': '#ccffac'})
        else:  
            output.append({'background-color': '#595656'})
    return output

@app.callback(

    Output("battery-fill", "style"),

    [
        Input('interval-component', 'n_intervals'),
    ],
)
def update_battery_level(index):
    index = (index*width_data_points) % 1000
    level = df.iloc[index, 3]
    return {'height': str(level*20)+'rem'}

def get_info(index=0, mask=[]):
    msg = ""
    if index != 0:
        1
        msg += "Number of cars connected: " + str(int(df.iloc[index]['numberOfConnectedVehicles/numConnVehicles.numConnVehicles'])) + "\n"
        msg += "Total delivered active power: " + str(int(df.iloc[index]['Total_W']/1000)) + 'kW\n'
    elif mask!=[]:
        2
    else:
        3

    return msg



@app.callback(
    [
        Output("Main-Graph", "figure"),
        Output("Info-Textbox", "placeholder"),
        Output("Info-Textbox2", "placeholder"),
    ],

    [
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date"),
        Input('interval-component', 'n_intervals'),
    ],
)
def update_graph_timer(start_date, end_date, index):
    df.style
    ctx = dash.callback_context
    # print(ctx.triggered)
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    # print(trigger)
    if trigger=='interval-component':
        index = (index*width_data_points) % 1000
        if index == 0:
            index = 1
        tmp_data = df.iloc[0:index, 3]
        information_update = get_info(index)
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=df.iloc[0:index, 1],
                    y=tmp_data*100
                )
            ]
        )
    elif trigger=='date-picker':
        if start_date is None:
            start_date = pd.Series.min(df['Interval'])
        if end_date is None:
            end_date = pd.Series.max(df['Interval'])
        if start_date == end_date:
            start_date_object = datetime.strptime(start_date+" 12:00 AM", "%Y-%m-%d %I:%M %p")
            end_date_object = datetime.strptime(end_date+" 11:59 PM", "%Y-%m-%d %I:%M %p")
        else:
            start_date_object = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_object = datetime.strptime(end_date, "%Y-%m-%d")
        mask = (df['Interval'] > start_date_object) & (df['Interval'] <= end_date_object)
        df_within_dates = df.loc[mask]
        information_update = get_info(mask=mask)
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=df_within_dates['Interval'],
                    y=df_within_dates['ams-a-control-in-stateOfCharge/AvgValue.avg'],
                )
            ]
        )
    else:
        tmp_data = df.iloc[:, 3]
        information_update = get_info()
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=df.iloc[:, 1],
                    y=tmp_data*100
                )
            ]
        )
    # print(df_within_dates)    
    fig = fig_update_layout(fig)
    return fig, information_update, information_update

def fix_datapoints():
    l = len(df)
    w = len(df.iloc[0])
    df.iloc[:, 3:] = df.iloc[:, 3:].interpolate(
        method='polynomial', order=1, axis=0)
    for i in range(3, w):
        j = 0
        # print(df.iloc[:, i][j])
        while np.isnan(df.iloc[:, i][j]):
            j += 1
        if j != 0:
            # print("col "+ str(i) + " row " + str(j) + " val" +str(df.iloc[:, i][0:j]))
            df.iloc[:, i][0:j] = df.iloc[:, i][j]
    return 

def process_df():
    format = "%Y-%m-%d %I:%M %p"
    fix_datapoints()
    df['Interval'] = df['Interval'].apply(lambda x: datetime.strptime(x, format))
    df['Interval (UTC)'] = df['Interval (UTC)'].apply(
        lambda x: datetime.strptime(x, format))
    df['Total_W'] = (df['ams-a-chrg-0-0-3PhaseActivePowW/AvgValue.avg'] + df['ams-a-chrg-0-1-3PhaseActivePowW/AvgValue.avg'] +
                    df['ams-a-chrg-1-0-3PhaseActivePowW/AvgValue.avg'] + df['ams-a-chrg-1-1-3PhaseActivePowW/AvgValue.avg'] +
                    df['ams-a-chrg-0-1-3PhaseActivePowW/AvgValue.avg'] + df['ams-a-chrg-2-0-3PhaseActivePowW/AvgValue.avg'] +
                    df['ams-a-chrg-2-1-3PhaseActivePowW/AvgValue.avg'] + df['ams-a-chrg-0-1-3PhaseActivePowW/AvgValue.avg'] +
                    df['ams-a-chrg-3-0-3PhaseActivePowW/AvgValue.avg'] + df['ams-a-chrg-3-1-3PhaseActivePowW/AvgValue.avg'] +
                    df['ams-a-chrg-0-1-3PhaseActivePowW/AvgValue.avg'] + df['ams-a-chrg-4-0-3PhaseActivePowW/AvgValue.avg'] +
                    df['ams-a-chrg-4-1-3PhaseActivePowW/AvgValue.avg'] + df['ams-a-chrg-0-1-3PhaseActivePowW/AvgValue.avg'] +
                    df['ams-a-chrg-5-0-3PhaseActivePowW/AvgValue.avg'] + df['ams-a-chrg-5-1-3PhaseActivePowW/AvgValue.avg'] +
                    df['ams-a-chrg-0-1-3PhaseActivePowW/AvgValue.avg'] + df['ams-a-chrg-6-0-3PhaseActivePowW/AvgValue.avg'] +
                    df['ams-a-chrg-6-1-3PhaseActivePowW/AvgValue.avg'] + df['ams-a-chrg-0-1-3PhaseActivePowW/AvgValue.avg'] +
                    df['ams-a-chrg-7-0-3PhaseActivePowW/AvgValue.avg'] + df['ams-a-chrg-7-1-3PhaseActivePowW/AvgValue.avg'])
    return

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
process_df()
# print(df)
# df, df_button, x_test, y_test = data_preprocessing()


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
                            initial_visible_month=pd.Series.max(df['Interval']),
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
    ] 
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
                            "height": "30rem",
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

info_box2 = dbc.Card(
    children=[
        dbc.CardBody(
            [
                html.Div(
                    dcc.Textarea(
                        id="Info-Textbox2",
                        placeholder="This field is used to display information about a feature displayed "
                        "on the graph.",
                        rows=8,
                        style={
                            "width": "100%",
                            "height": "30rem",
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

chargeView = html.Div(
    className="chargeArea",
    children=[
            dbc.Row([
                dbc.Col([html.Div(id='car_0_0')]), dbc.Col([html.Div(id='car_0_1')]), dbc.Col([html.Div(id='car_1_0')]), dbc.Col([html.Div(id='car_1_1')])
            ]), 
            dbc.Row([
                dbc.Col([html.Div(id='car_2_0')]), dbc.Col([html.Div(id='car_2_1')]), dbc.Col([html.Div(id='car_3_0')]), dbc.Col([html.Div(id='car_3_1')])
            ]), 
            dbc.Row([
                dbc.Col([html.Div(id='car_4_0')]), dbc.Col([html.Div(id='car_4_1')]), dbc.Col([html.Div(id='car_5_0')]), dbc.Col([html.Div(id='car_5_1')])
            ]), 
            dbc.Row([   
                dbc.Col([html.Div(id='car_6_0')]), dbc.Col([html.Div(id='car_6_1')]), dbc.Col([html.Div(id='car_7_0')]), dbc.Col([html.Div(id='car_7_1')])
            ])

            # gives more flexibility of where to place "cars"
            # children=[
            #     html.Div(id='car_0_0'),
            #     html.Div(id='car_0_1'),
            #     html.Div(id='car_1_0'),
            #     html.Div(id='car_1_1'),
            #     html.Div(id='car_2_0'),
            #     html.Div(id='car_2_1'),
            #     html.Div(id='car_3_0'),
            #     html.Div(id='car_3_1'),
            #     html.Div(id='car_4_0'),
            #     html.Div(id='car_4_1'),
            #     html.Div(id='car_5_0'),
            #     html.Div(id='car_5_1'),
            #     html.Div(id='car_6_0'),
            #     html.Div(id='car_6_1'),
            #     html.Div(id='car_7_0'),
            #     html.Div(id='car_7_1'),
            # ]
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
        html.Div(  
        )
    ],
)

bottomView = html.Div(
    className="bottom-view",
    children=[
        hills,
        windmillView,
        flowView,
        chargeView
    ]
)

###################### Style app layout ########################################
app.layout = dbc.Container(
    fluid=True,
    children=[
        logo(app),
        dbc.Row([
                dbc.Col([info_box], width=2), 
                dbc.Col([info_box2], width=2), 
                dbc.Col([graphs])       
        ]),
        bottomView,
        dcc.Interval(
            id='interval-component',
            interval=1*speed,  # in milliseconds
            n_intervals=1
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=True)
