from multiprocessing import connection
from matplotlib.pyplot import margins
import pandas as pd
import numpy as np
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import dash_daq as daq

import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from datetime import datetime, date, timedelta
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
yellow = "rgb(255, 218, 0)"
# yellow ="rgb(32, 113, 181)"

################ Functions definition ######################


def fig_update_layout(fig, myTitle):
    fig.update_layout(
        xaxis=dict(
            showline=False,
            showgrid=False,
            showticklabels=True,
            zeroline=False,
            gridcolor="#636363",
            linecolor="rgb(255, 218, 0)",
            linewidth=2,
            tickfont=dict(family="Vattenfall", size=12, color="white",),
            title=dict(font=dict(family="Vattenfall",
                       size=24, color="#fec036"),),
        ),
        yaxis=dict(
            showline=False,
            showgrid=False,
            showticklabels=True,
            zeroline=False,
            gridcolor="#636363",
            linecolor="rgb(255, 218, 0)",
            linewidth=2,
            tickfont=dict(family="Vattenfall", size=12, color="white",),
            title=dict(font=dict(family="Vattenfall",
                       size=24, color="#fec036"),),
        ),
        autosize=True,
        margin=dict(autoexpand=True, l=50, b=40, r=35, t=30),
        showlegend=False,
        paper_bgcolor="black",
        plot_bgcolor="black",
        title=dict(
            text=myTitle,
            font=dict(family="Vattenfall", size=32, color="darkgray"),
            xanchor="center",
            yanchor="top",
            y=1,
            x=0.5,
        ),
    )
    return fig


@app.callback(
    Output("sun", 'style'),
    Input('interval-component', 'n_intervals'),
)
def move_sun(index):
    now = datetime.now()
    seconds = now.second
    a = -0.01
    h = 0.3
    x = (index*2) % 90
    y = (a*(x-50)**2+h)
    style = {'transform': 'translate('+str(x)+'rem, '+str(-y)+'rem)'}
    return style


@app.callback(
    Output("Main-Graph", "relayoutData"),
    Input("Pow-Graph", "relayoutData"),
)
def graph_call_connection(selection):
    return selection


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
        Input("Main-Graph", "relayoutData"),
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date"),
        Input('interval-component', 'n_intervals'),
    ]
)
def update_cars(selection, start_date, end_date, index):
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    end_point = 0
    if trigger == 'interval-component':
        end_point = (index*width_data_points) % 1000
    elif trigger == 'date-picker':
        end_point = df.loc[(df['Interval'] <= end_date)].index[-1]
    elif trigger == 'Main-Graph':
        if "xaxis.range[0]" in selection:
            start_date = str(selection["xaxis.range[0]"])
            end_date = str(selection["xaxis.range[1]"])
            start_date_object = datetime.strptime(
                start_date, "%Y-%m-%d %H:%M:%S.%f")
            end_date_object = datetime.strptime(
                end_date, "%Y-%m-%d %H:%M:%S.%f")
            mask = (df['Interval'] > start_date_object) & (
                df['Interval'] <= end_date_object)
            df_within_dates = df.loc[mask]
            end_point = df_within_dates.index[-1]
        else:
            end_point = df.index[-1]
    else:
        end_point = df.index[-1]
    cars_connected_avg = df.iloc[:, -48::3]
    output = list()
    for i in range(0, 16):
        car_i = cars_connected_avg.iloc[end_point, i]
        if car_i != 0.0:
            output.append(
                {'background-image': 'url(../assets/car-charging.svg)'})
        else:
            output.append({'background-image': 'url(../assets/car-none.svg)'})
    return output


@app.callback(
    [
        Output('car_0_0', 'children'),
        Output('car_0_1', 'children'),
        Output('car_1_0', 'children'),
        Output('car_1_1', 'children'),
        Output('car_2_0', 'children'),
        Output('car_2_1', 'children'),
        Output('car_3_0', 'children'),
        Output('car_3_1', 'children'),
        Output('car_4_0', 'children'),
        Output('car_4_1', 'children'),
        Output('car_5_0', 'children'),
        Output('car_5_1', 'children'),
        Output('car_6_0', 'children'),
        Output('car_6_1', 'children'),
        Output('car_7_0', 'children'),
        Output('car_7_1', 'children'),
    ],
    [
        Input("Main-Graph", "relayoutData"),
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date"),
        Input('interval-component', 'n_intervals'),
    ],
)
def update_flow_cars(selection, start_date, end_date, index):
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    end_point = 0
    df_slice = df.iloc[:, 10:-49:3]
    ret = list()
    if trigger == 'interval-component':
        end_point = (index*width_data_points) % 1000
    elif trigger == 'date-picker':
        end_point = df.loc[(df['Interval'] <= end_date)].index[-1]
    elif trigger == 'Main-Graph':
        if "xaxis.range[0]" in selection:
            start_date = str(selection["xaxis.range[0]"])
            end_date = str(selection["xaxis.range[1]"])
            start_date_object = datetime.strptime(
                start_date, "%Y-%m-%d %H:%M:%S.%f")
            end_date_object = datetime.strptime(
                end_date, "%Y-%m-%d %H:%M:%S.%f")
            mask = (df['Interval'] > start_date_object) & (
                df['Interval'] <= end_date_object)
            df_within_dates = df_slice.loc[mask]
            end_point = df_within_dates.index[-1]
        else:
            end_point = df_slice.index[-1]
    else:
        end_point = df_slice.index[-1]
    for i in range(0, 16):
        if df_slice.iloc[end_point, i] > 0:
            ret.append(carFlow1)
        else:
            ret.append(html.H6(", ", style={"color": "rgb(32, 113, 181)"}))
            # ret.append(
            #     html.H6("Free", style={
            #         'transform': 'scale(-1,1)',
            #         'top': '-0.3rem',
            #         'left': '-1rem',
            #         'position': 'relative'}))
    return ret


@app.callback(
    [
        Output("wheel", "style"),
        Output("arrow_in_1", "style"),
        Output("arrow_in_2", "style"),
        Output("arrow_in_3", "style"),
        Output("arrow_in_4", "style"),
        Output("arrow_in_5", "style"),
        Output("arrow_in_6", "style"),
        Output("arrow_in_7", "style"),
        Output("arrow_in_8", "style"),
        Output("arrow_out_1", "style"),
        Output("arrow_out_2", "style"),
        Output("arrow_out_3", "style"),
        Output("arrow_out_4", "style"),
        Output("arrow_out_5", "style"),
        Output("arrow_out_6", "style"),
        Output("arrow_out_7", "style"),
        Output("arrow_out_8", "style"),
    ],
    [
        Input("Main-Graph", "relayoutData"),
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date"),
        Input('interval-component', 'n_intervals'),
    ],
)
def update_flow_speed(selection, start_date, end_date, index):
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    end_point = 0
    if trigger == 'interval-component':
        end_point = (index*width_data_points) % 1000
    elif trigger == 'date-picker':
        end_point = df.loc[(df['Interval'] <= end_date)].index[-1]
    elif trigger == 'Main-Graph':
        if "xaxis.range[0]" in selection:
            start_date = str(selection["xaxis.range[0]"])
            end_date = str(selection["xaxis.range[1]"])
            start_date_object = datetime.strptime(
                start_date, "%Y-%m-%d %H:%M:%S.%f")
            end_date_object = datetime.strptime(
                end_date, "%Y-%m-%d %H:%M:%S.%f")
            mask = (df['Interval'] > start_date_object) & (
                df['Interval'] <= end_date_object)
            df_within_dates = df.loc[mask]
            end_point = df_within_dates.index[-1]
        else:
            end_point = df.index[-1]
    else:
        end_point = df.index[-1]

    level = round(df.iloc[end_point, 6])
    ret = list()
    if level < 0:  # discharging battery
        level = round(((1-normalize_data(abs(level), 0, 17.159))+0.5)*5)
        windmill = {'animation': 'spin '+str(0)+'s linear infinite reverse'}
        ret.append(windmill)
        for i in range(1, 9):
            flow_in = {'animation': 'horizontalSlide ' +
                       str(0)+'s linear infinite', 'animation-delay': str(0) + 's'}
            ret.append(flow_in)
        for i in range(1, 9):
            delay = str((level*i)/8)
            flow_out = {'animation': 'horizontalSlide ' +
                        str(level)+'s linear infinite', 'animation-delay': delay+'s'}
            ret.append(flow_out)
    elif level > 0:  # charging battery
        level = round(((1-normalize_data(abs(level), 0, 42.795))+0.5)*5)
        windmill = {'animation': 'spin ' +
                    str(level)+'s linear infinite reverse'}
        ret.append(windmill)
        for i in range(1, 9):
            delay = str((level*i)/8)
            flow_in = {'animation': 'horizontalSlide ' +
                       str(level)+'s linear infinite', 'animation-delay': delay+'s'}
            ret.append(flow_in)
        for i in range(1, 9):
            flow_out = {'animation': 'horizontalSlide ' +
                        str(0)+'s linear infinite', 'animation-delay': str(i*0.5)+'s'}
            ret.append(flow_out)
    else:
        windmill = {'animation': 'spin '+str(0)+'s linear infinite reverse'}
        ret.append(windmill)
        for i in range(1, 9):
            flow_in = {'animation': 'horizontalSlide ' +
                       str(0)+'s linear infinite', 'animation-delay': str(0)+'s'}
            ret.append(flow_in)
        for i in range(1, 9):
            flow_out = {'animation': 'horizontalSlide ' +
                        str(0)+'s linear infinite', 'animation-delay': str(i*0.5)+'s'}
            ret.append(flow_out)
    return ret


def normalize_data(data, min, max):
    return (data - min) / (max - min)


@app.callback(

    Output("battery-fill", "style"),

    [
        Input("Main-Graph", "relayoutData"),
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date"),
        Input('interval-component', 'n_intervals'),
    ],
)
def update_battery_level(selection, start_date, end_date, index):
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    end_point = 0
    if trigger == 'interval-component':
        end_point = (index*width_data_points) % 1000
    elif trigger == 'date-picker':
        end_point = df.loc[(df['Interval'] <= end_date)].index[-1]
    elif trigger == 'Main-Graph':
        if "xaxis.range[0]" in selection:
            start_date = str(selection["xaxis.range[0]"])
            end_date = str(selection["xaxis.range[1]"])
            start_date_object = datetime.strptime(
                start_date, "%Y-%m-%d %H:%M:%S.%f")
            end_date_object = datetime.strptime(
                end_date, "%Y-%m-%d %H:%M:%S.%f")
            mask = (df['Interval'] > start_date_object) & (
                df['Interval'] <= end_date_object)
            df_within_dates = df.loc[mask]
            end_point = df_within_dates.index[-1]
        else:
            end_point = df.index[-1]
    else:
        end_point = df.index[-1]

    level = df.iloc[end_point, 3]
    return {'height': str(level*20)+'rem'}


def get_info(df_within_dates):
    msg = ""
    charging = 0
    discharging = 0
    idle = 0
    tot = len(df_within_dates)
    # msg += "Battery level: " + str(int(df_within_dates.iloc[-1, 3]*100)) + "\n"
    # msg += "Number of cars connected: " + \
    #     str(int(
    #         df_within_dates['numberOfConnectedVehicles/numConnVehicles.numConnVehicles'].iloc[-1])) + "\n"
    msg += "Total delivered power: " + \
        str(int(df_within_dates['Total_W'].sum()/6000)) + 'kWh\n'
    for i in range(0, tot):
        current_val = df_within_dates['ams-a-bat-ew/AvgValue.avg'].iloc[i]
        if current_val == 0:
            idle += 1
        elif current_val > 0:
            charging += 1
        else:
            discharging += 1
    charging_rate = int((charging/tot)*100)
    discharging_rate = int((discharging/tot)*100)
    idle_rate = int((idle/tot)*100)
    in_use_rate = int(((charging+discharging)/tot)*100)
    msg += "Charging rate: " + str(charging_rate) + "%\n"
    msg += "Discharging rate: " + str(discharging_rate) + "%\n"
    msg += "Idle rate: " + str(idle_rate) + "%\n"
    msg += "Usage of battery: " + str(in_use_rate) + "%\n"
    return msg


@app.callback(
    Output("Info-Textbox", "placeholder"),
    Input('interval-component', 'n_intervals'),
)
def rolling_info(index):
    now = datetime.now()
    seconds = now.second
    interval = 5
    number_messages = 3
    sel_msg = int(seconds/interval) % number_messages
    msg = ""
    if sel_msg == 0:
        msg += "Did you know... \n\n Like a piggy bank, I save energy when we have some over\nand give it back when you need it"
    elif sel_msg == 1:
        msg += "Did you know... \n\n Before I was here \nyou could only charge 3 vehicles. \nNow you can charge 16! "
    elif sel_msg == 2:
        msg += "Did you know... \n\nBy charging your vehicle here you help save the environment!\n "
    elif sel_msg == 3:
        msg += "Did you know... \n\n That I think Amsterdam is a wonderful city! Fijne dag"
    return msg


@app.callback(
    [
        Output("Main-Graph", "figure"),
        Output("Pow-Graph", "figure"),
        Output("Info-Textbox2", "placeholder"),
    ],

    [
        Input("Main-Graph", "relayoutData"),
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date"),
        Input('interval-component', 'n_intervals'),
    ],
)
def update_graph_timer(selection, start_date, end_date, index):
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    if trigger == 'interval-component':
        index = (index*width_data_points) % 1000
        if index == 0:
            index = 1
        end_date = df['Interval'].iloc[index]
        # select a max range of 3 days to show from end date
        start_date = end_date - timedelta(days=3)
        mask = (df['Interval'] > start_date) & (df['Interval'] <= end_date)
        df_within_dates = df.loc[mask]
        tmp_data = df_within_dates.iloc[:, 3]
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=df_within_dates['Interval'],
                    y=tmp_data*100,
                    line_color=yellow,
                )
            ]
        )
        fig1 = go.Figure(
            data=[
                go.Scatter(
                    x=df_within_dates['Interval'],
                    y=df_within_dates['Total_W'],
                    line_color=yellow,
                )
            ]
        )
    elif trigger == 'date-picker':
        if start_date is None:
            start_date = pd.Series.min(df['Interval'])
        if end_date is None:
            end_date = pd.Series.max(df['Interval'])
        if start_date == end_date:
            start_date_object = datetime.strptime(
                start_date+" 12:00 AM", "%Y-%m-%d %I:%M %p")
            end_date_object = datetime.strptime(
                end_date+" 11:59 PM", "%Y-%m-%d %I:%M %p")
        else:
            start_date_object = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_object = datetime.strptime(end_date, "%Y-%m-%d")
        mask = (df['Interval'] > start_date_object) & (
            df['Interval'] <= end_date_object)
        df_within_dates = df.loc[mask]
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=df_within_dates['Interval'],
                    y=df_within_dates['ams-a-control-in-stateOfCharge/AvgValue.avg'],
                    line_color=yellow,
                )
            ]
        )
        fig1 = go.Figure(
            data=[
                go.Scatter(
                    x=df_within_dates['Interval'],
                    y=df_within_dates['Total_W'],
                    line_color=yellow,
                )
            ]
        )
    elif trigger == 'Main-Graph':
        if "xaxis.range[0]" in selection:
            start_date = str(selection["xaxis.range[0]"])
            end_date = str(selection["xaxis.range[1]"])
            start_date_object = datetime.strptime(
                start_date, "%Y-%m-%d %H:%M:%S.%f")
            end_date_object = datetime.strptime(
                end_date, "%Y-%m-%d %H:%M:%S.%f")
            mask = (df['Interval'] > start_date_object) & (
                df['Interval'] <= end_date_object)
            df_within_dates = df.loc[mask]
            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=df_within_dates['Interval'],
                        y=df_within_dates['ams-a-control-in-stateOfCharge/AvgValue.avg'],
                        line_color=yellow,
                    )
                ]
            )
            fig1 = go.Figure(
                data=[
                    go.Scatter(
                        x=df_within_dates['Interval'],
                        y=df_within_dates['Total_W'],
                        line_color=yellow,
                    )
                ]
            )
        else:
            if start_date == None and end_date == None:
                end_date = df['Interval'].iloc[df.index[-1]]
                # select a max range of 3 days to show from end date
                start_date = end_date - timedelta(days=3)
            mask = (df['Interval'] > start_date) & (df['Interval'] <= end_date)
            df_within_dates = df.loc[mask]
            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=df_within_dates.iloc[:, 1],
                        y=df_within_dates.iloc[:, 3]*100,
                        line_color=yellow,
                    )
                ]
            )
            fig1 = go.Figure(
                data=[
                    go.Scatter(
                        x=df_within_dates.iloc[:, 1],
                        y=df_within_dates['Total_W'],
                        line_color=yellow,
                    )
                ]
            )
    else:
        end_date = df['Interval'].iloc[df.index[-1]]
        # select a max range of 3 days to show from end date
        start_date = end_date - timedelta(days=3)
        mask = (df['Interval'] > start_date) & (df['Interval'] <= end_date)
        df_within_dates = df.loc[mask]
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=df_within_dates.iloc[:, 1],
                    y=df_within_dates.iloc[:, 3]*100,
                    line_color=yellow,
                )
            ]
        )
        fig1 = go.Figure(
            data=[
                go.Scatter(
                    x=df_within_dates.iloc[:, 1],
                    y=df_within_dates['Total_W'],
                    line_color=yellow,
                )
            ]
        )
    information_update = get_info(df_within_dates)
    fig = fig_update_layout(fig, "Battery Level")
    fig1 = fig_update_layout(fig1, "Power W")
    return fig, fig1, information_update


def fix_datapoints():
    l = len(df)
    w = len(df.iloc[0])
    df.iloc[:, 3:] = df.iloc[:, 3:].interpolate(
        method='polynomial', order=1, axis=0)
    for i in range(3, w):
        j = 0
        while np.isnan(df.iloc[:, i][j]):
            j += 1
        if j != 0:
            df.iloc[:, i][0:j] = df.iloc[:, i][j]
    return


def process_df():
    format = "%Y-%m-%d %I:%M %p"
    fix_datapoints()
    df['Interval'] = df['Interval'].apply(
        lambda x: datetime.strptime(x, format))
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
        "BPCH AMSTERDAM",
        style={"marginTop": 5, "marginLeft": "10px",
               "fontSize": "35", "color": "rgb(78,75,72)"},
    )

    info_about_app = html.H6(
        "Battery-Powered Charging Hub Amsterdam",
        style={"marginLeft": "10px", "fontSize": "25",
               "color": "rgb(78,75,72)"}
    )

    logo_image_amst = html.Img(src=app.get_asset_url(
        "amsterdam_logo.png"), style={"marginTop": 5, "height": 60, "left": "3%", "float": "left", "display": "inline-block", })
    logo_image = html.Img(src=app.get_asset_url(
        "VF_logo.png"), style={"marginTop": -20, "height": 100, "right": "3%", "float": "right", "display": "inline-block", })

    return dbc.Row([
        dbc.Col([logo_image_amst], width={'size': 4}),
        dbc.Col([
            dbc.Row([title]),
            dbc.Row([info_about_app])],
            width={'size': 4}, className='text-center'),
        dbc.Col([logo_image], width={'size': 4}),
    ], style={
                "backgroundColor": "white",
                }
    )


#  get data from csv
df = pd.read_csv('assets/data.csv')
process_df()
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
                                    "margin": {"t": 0, "r": 0, "b": 0, "l": 0},
                                    "xaxis": {
                                        "dtick": 5,
                                        "gridcolor": "#636363",
                                        "showline": False,
                                    },
                                    "yaxis": {"showgrid": False, "showline": False},
                                    "plot_bgcolor": "black",
                                    "title": "Battery %",
                                    "paper_bgcolor": "black",
                                    "font": {"color": "gray"},
                                    "height": 200,
                                },
                            },
                            config={"displayModeBar": False},
                        ),
                        html.Pre(id="update-on-click-data"),
                    ],
                    style={"width": "98%", "display": "inline-block"},
                ),
            ],
            style={
                "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "1px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        )
    ]
)

graphs_pow = dbc.Card(
    children=[
        dbc.CardBody(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id="Pow-Graph",
                            figure={
                                "layout": {
                                    "margin": {"t": 0, "r": 0, "b": 0, "l": 0},
                                    "xaxis": {
                                        "dtick": 5,
                                        "gridcolor": "#636363",
                                        "showline": False,
                                    },
                                    "yaxis": {"showgrid": False, "showline": False},
                                    "plot_bgcolor": "black",
                                    "title": "Power kW/h",
                                    "paper_bgcolor": "black",
                                    "font": {"color": "gray"},
                                    "height": 200,
                                },
                            },
                            config={"displayModeBar": False},
                        ),
                        html.Pre(id="update-on-click-data-2"),
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
                            initial_visible_month=pd.Series.max(
                                df['Interval']),
                            start_date_placeholder_text="Start Date",
                            end_date_placeholder_text="End Date",
                            calendar_orientation="vertical",
                        ),
                        html.Div(id="output-container-date-picker-range"),
                    ],
                    style={
                        "vertical-align": "bottom",
                        "position": "absolute",
                        "bottom": 0,
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
                "border-width": "1px",
                "border-top": "1px solid black",
            },
        )
    ]
)

info_box = dcc.Textarea(
    id="Info-Textbox",
    placeholder="This field is used to display information about a feature displayed "
    "on the graph.",
    rows=6,
    style={
        "width": "100%",
        "height": "32rem",
        "resize": "none",
        "background-color": "rgb(189,213,233)",
        "color": "#00000",
        "placeholder": "#00000",
        "fontFamily": "Vattenfall",
        "fontSize": "30",
        "display": "inline-block",
    },
)


info_box2 = dcc.Textarea(
    id="Info-Textbox2",
    placeholder="This field is used to display information about a feature displayed "
    "on the graph.",
    rows=8,
    style={
        "width": "100%",
        "height": "32rem",
        "resize": "none",
        "background-color": "rgb(189,213,233)",
        "color": "#00000",
        "placeholder": "#00000",
        "fontFamily": "Vattenfall",
        "fontSize": "30",
        "display": "inline-block",
    },
)

flowView = html.Div(
    children=[
        html.Div(
            id="horizontalArrowAnim1",
            children=[
                html.Div(
                    id='arrow_out_1',
                    className="horizontalArrowSliding",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    id='arrow_out_2',
                    className="horizontalArrowSliding delay1",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    id='arrow_out_3',
                    className="horizontalArrowSliding delay2",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    id='arrow_out_4',
                    className="horizontalArrowSliding delay3",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    id='arrow_out_5',
                    className="horizontalArrowSliding delay4",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    id='arrow_out_6',
                    className="horizontalArrowSliding delay5",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    id='arrow_out_7',
                    className="horizontalArrowSliding delay6",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    id='arrow_out_8',
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
                    id='arrow_in_1',
                    className="horizontalArrowSliding",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    id='arrow_in_2',
                    className="horizontalArrowSliding delay1",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    id='arrow_in_3',
                    className="horizontalArrowSliding delay2",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    id='arrow_in_4',
                    className="horizontalArrowSliding delay3",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    id='arrow_in_5',
                    className="horizontalArrowSliding delay4",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    id='arrow_in_6',
                    className="horizontalArrowSliding delay5",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    id='arrow_in_7',
                    className="horizontalArrowSliding delay6",
                    children=[
                        html.Div(className="arrow1")
                    ],
                ),
                html.Div(
                    id='arrow_in_8',
                    className="horizontalArrowSliding delay7",
                    children=[
                        html.Div(className="arrow1")
                    ],
                )
            ],
        )
    ]
)

carFlow1 = html.Div(
    className="carFlow1",
    children=[
        html.Div(
            className="horizontalCarArrowSliding",
            children=[
                html.Div(className="arrow2")
            ],
        ),
        html.Div(
            className="horizontalCarArrowSliding d1",
            children=[
                html.Div(className="arrow2")
            ],
        ),
        html.Div(
            className="horizontalCarArrowSliding d2",
            children=[
                html.Div(className="arrow2")
            ],
        ),
        html.Div(
            className="horizontalCarArrowSliding d3",
            children=[
                html.Div(className="arrow2")
            ],
        ),
        html.Div(
            className="horizontalCarArrowSliding d4",
            children=[
                html.Div(className="arrow2")
            ],
        ),
        html.Div(
            className="horizontalCarArrowSliding d5",
            children=[
                html.Div(className="arrow2")
            ],
        ),
        html.Div(
            className="horizontalCarArrowSliding d6",
            children=[
                html.Div(className="arrow2")
            ],
        ),
        html.Div(
            className="horizontalCarArrowSliding d7",
            children=[
                html.Div(className="arrow2")
            ],
        )
    ],
)

carFlow2 = html.Div(
    className="carFlow2",
    children=[
        html.Div(
            className="horizontalCarArrowSliding",
            children=[
                html.Div(className="arrow2")
            ],
        ),
        html.Div(
            className="horizontalCarArrowSliding d1",
            children=[
                html.Div(className="arrow2")
            ],
        ),
        html.Div(
            className="horizontalCarArrowSliding d2",
            children=[
                html.Div(className="arrow2")
            ],
        ),
        html.Div(
            className="horizontalCarArrowSliding d3",
            children=[
                html.Div(className="arrow2")
            ],
        ),
        html.Div(
            className="horizontalCarArrowSliding d4",
            children=[
                html.Div(className="arrow2")
            ],
        ),
        html.Div(
            className="horizontalCarArrowSliding d5",
            children=[
                html.Div(className="arrow2")
            ],
        ),
        html.Div(
            className="horizontalCarArrowSliding d6",
            children=[
                html.Div(className="arrow2")
            ],
        ),
        html.Div(
            className="horizontalCarArrowSliding d7",
            children=[
                html.Div(className="arrow2")
            ],
        ),

    ],
)

tulip = html.Div(className='stem',
                 children=[
                     html.Div(className='tulipHead',
                              children=[
                                  html.Div(
                                      className="tulipHair lightTulip lightTulip-1"),
                                  html.Div(
                                      className="tulipHair darkTulip darkTulip-1"),
                                  html.Div(
                                      className="tulipHair lightTulip lightTulip-2"),
                                  html.Div(
                                      className="tulipHair darkTulip darkTulip-2"),
                                  html.Div(
                                      className="tulipHair lightTulip lightTulip-3"),
                              ]),
                     html.Div(className="rightTulipLeaf tulipLeaf leaf"),
                     html.Div(className="leftTulipLeaf tulipLeaf leaf"),
                     html.Div(className="rightStemLeaf stemLeaf leaf"),
                     html.Div(className="leftStemLeaf stemLeaf leaf")
                 ]
                 )


leftTulip1 = html.Div(
    className='tulip1',
    children=[tulip]
)
rightTulip1 = html.Div(
    className='tulip2 rightBabyTulip',
    children=[tulip]
)
leftTulip2 = html.Div(
    className='tulip3',
    children=[tulip]
)
rightTulip2 = html.Div(
    className='tulip4 rightBabyTulip',
    children=[tulip]
)
leftTulip3 = html.Div(
    className='tulip5',
    children=[tulip]
)
rightTulip3 = html.Div(
    className='tulip6 rightBabyTulip',
    children=[tulip]
)
leftTulip4 = html.Div(
    className='tulip7',
    children=[tulip]
)

tulipsView = html.Div(
    children=[
        leftTulip1,
        leftTulip2,
        leftTulip3,
        leftTulip4,
        rightTulip1,
        rightTulip2,
        rightTulip3
    ]
)

chargeView = html.Div(
    className='chargeArea',
    children=[
        html.Div(id='chargeSpot1',
                 children=[
                     html.Div(className='pole'),
                     html.Div(className='poleHead'),
                     html.Div(id='car_0_0', children=[carFlow1]),
                     html.Div(id='car_0_1', children=[carFlow1]),
                 ]),
        html.Div(id='chargeSpot2',
                 children=[
                     html.Div(className='pole'),
                     html.Div(className='poleHead'),
                     html.Div(id='car_1_0', children=[carFlow1]),
                     html.Div(id='car_1_1', children=[carFlow1])
                 ]),
        html.Div(id='chargeSpot3',
                 children=[
                     html.Div(className='pole'),
                     html.Div(className='poleHead'),
                     html.Div(id='car_2_0', children=[carFlow1]),
                     html.Div(id='car_2_1', children=[carFlow1])
                 ]),
        html.Div(id='chargeSpot4',
                 children=[
                     html.Div(className='pole'),
                     html.Div(className='poleHead'),
                     html.Div(id='car_3_0', children=[carFlow1]),
                     html.Div(id='car_3_1', children=[carFlow1])
                 ]),
        html.Div(id='chargeSpot5',
                 children=[
                     html.Div(className='pole'),
                     html.Div(className='poleHead'),
                     html.Div(id='car_4_0', children=[carFlow1]),
                     html.Div(id='car_4_1', children=[carFlow1])
                 ]),
        html.Div(id='chargeSpot6',
                 children=[
                     html.Div(className='pole'),
                     html.Div(className='poleHead'),
                     html.Div(id='car_5_0', children=[carFlow1]),
                     html.Div(id='car_5_1', children=[carFlow1])
                 ]),
        html.Div(id='chargeSpot7',
                 children=[
                     html.Div(className='pole'),
                     html.Div(className='poleHead'),
                     html.Div(id='car_6_0', children=[carFlow1]),
                     html.Div(id='car_6_1', children=[carFlow1])
                 ]),
        html.Div(id='chargeSpot8',
                 children=[
                     html.Div(className='pole'),
                     html.Div(className='poleHead'),
                     html.Div(id='car_7_0', children=[carFlow1]),
                     html.Div(id='car_7_1', children=[carFlow1])
                 ]),
    ]
)

# chargeView = html.Div(
#     className="chargeArea",
#     children=[
#         dbc.Row([
#                 dbc.Col([html.Div(id='car_0_0', children=[html.H6('0_0', style={'color': '#000000'})])]), dbc.Col([html.Div(id='car_0_1', children=[html.H6('0_1', style={'color': '#000000'})])]), dbc.Col(
#                     [html.Div(id='car_1_0', children=[html.H6('1_0', style={'color': '#000000'})])]), dbc.Col([html.Div(id='car_1_1', children=[html.H6('1_1', style={'color': '#000000'})])])
#                 ]),
#         dbc.Row([
#                 dbc.Col([html.Div(id='car_2_0', children=[html.H6('2_0', style={'color': '#000000'})])]), dbc.Col([html.Div(id='car_2_1', children=[html.H6('2_1', style={'color': '#000000'})])]), dbc.Col(
#                     [html.Div(id='car_3_0', children=[html.H6('3_0', style={'color': '#000000'})])]), dbc.Col([html.Div(id='car_3_1', children=[html.H6('3_1', style={'color': '#000000'})])])
#                 ]),
#         dbc.Row([
#                 dbc.Col([html.Div(id='car_4_0', children=[html.H6('4_0', style={'color': '#000000'})])]), dbc.Col([html.Div(id='car_4_1', children=[html.H6('4_1', style={'color': '#000000'})])]), dbc.Col(
#                     [html.Div(id='car_5_0', children=[html.H6('5_0', style={'color': '#000000'})])]), dbc.Col([html.Div(id='car_5_1', children=[html.H6('5_1', style={'color': '#000000'})])])
#                 ]),
#         dbc.Row([
#                 dbc.Col([html.Div(id='car_6_0', children=[html.H6('6_0', style={'color': '#000000'})])]), dbc.Col([html.Div(id='car_6_1', children=[html.H6('6_1', style={'color': '#000000'})])]), dbc.Col(
#                     [html.Div(id='car_7_0', children=[html.H6('7_0', style={'color': '#000000'})])]), dbc.Col([html.Div(id='car_7_1', children=[html.H6('7_1', style={'color': '#000000'})])])
#                 ])

#         # gives more flexibility of where to place "cars"
#         # children=[
#         #     html.Div(id='car_0_0'),
#         #     html.Div(id='car_0_1'),
#         #     html.Div(id='car_1_0'),
#         #     html.Div(id='car_1_1'),
#         #     html.Div(id='car_2_0'),
#         #     html.Div(id='car_2_1'),
#         #     html.Div(id='car_3_0'),
#         #     html.Div(id='car_3_1'),
#         #     html.Div(id='car_4_0'),
#         #     html.Div(id='car_4_1'),
#         #     html.Div(id='car_5_0'),
#         #     html.Div(id='car_5_1'),
#         #     html.Div(id='car_6_0'),
#         #     html.Div(id='car_6_1'),
#         #     html.Div(id='car_7_0'),
#         #     html.Div(id='car_7_1'),
#         # ]
#     ]
# )

hills = html.Div(
    children=[
        html.Div(className="hills1"),
        html.Div(className="hills2"),
        html.Div(className="hills3"),
        html.Div(className="hills4"),
        html.Div(className="hills5"),
        html.Div(className="hills6"),
        html.Div(className="hills7"),
        html.Div(id="sun")
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
            id="wheel",
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
        chargeView,
        tulipsView,
        # html.Div(id="sun")
    ]
)

###################### Style app layout ########################################
app.layout = dbc.Container(
    fluid=True,
    children=[
        dcc.Interval(
            id='interval-component',
            interval=1*speed,  # in milliseconds
            n_intervals=1
        ),
        logo(app),
        dbc.Row([
                dbc.Col([info_box], width=4),
                dbc.Col([info_box2], width=4),
                dbc.Col([graphs, graphs_pow])
                ]),
        bottomView,
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=True)
