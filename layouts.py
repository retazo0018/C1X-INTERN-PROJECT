import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from components import functions
import numpy as np
from components import header
import pandas as pd





# top level metacategory
final = functions.toplevelmetacategories()
pv = final.set_index('Name')
trace1 = go.Bar(x=pv.index, y=pv['Count'], name='TopMC')

# cookie churn
cookieagetrend = functions.cookiechurn()

# ip2geo
latitude, longitude, information = functions.ip2geomapping()

# channelcount
channel = functions.channelcount()

tclicks, timpressions, nuniqueusers, tcapacity = functions.valueboxes()


def updatebox1():
    return nuniqueusers

def updatebox2():
    return tcapacity

def updatebox3():
    return timpressions

def updatebox4():
    return tclicks

colors = {
    'background': '#111111',
    'text': '#fafafa'
}


s = {'border': '1px solid black', 'width': '75%', 'height': '60px','color': '#fafafa',
     'background-color': '#111111','margin-right': '3px','margin-left': '2px', 'flex-grow': '1', 'border-radius': '8px'}

home = html.Div([
    html.Div([
            header.navbar
        ]),
    html.Div([
        html.Div([
            html.Div([
                html.P('Number of Unique Users ',style={'font-weight': '170', 'font-family': 'sans-serif'}),
                html.P(id='box1',  children=updatebox1(), style={'font-weight': '600', 'font-size': '18px'})
            ], style={'margin-left': '5px', 'text-align': 'center'})
        ], style=s),
        html.Div([
            html.Div([
                html.P('Total Capacity ', style={'font-weight': '170', 'font-family': 'sans-serif'}),
                html.P(id='box2', children=updatebox2(), style={'font-weight': '600', 'font-size': '18px'})
            ], style={'margin-left': '5px', 'text-align': 'center'})
        ], style=s),
        html.Div([
            html.Div([
                html.P('Total Impressions ', style={'font-weight': '170', 'font-family': 'sans-serif'}),
                html.P(id='box3', children=updatebox3(), style={'font-weight': '600', 'font-size': '18px'})
            ], style={'margin-left': '5px', 'text-align': 'center'})
        ], style=s),
        html.Div([
            html.Div([
                html.P('Total Clicks ', style={'font-weight': '170', 'font-family': 'sans-serif'}),
                html.P(id='box4', children=updatebox4(), style={'font-weight': '600', 'font-size': '18px'})
            ], style={'margin-left': '5px', 'text-align': 'center'})
        ], style=s),
    ], style={'display': 'flex','justify-content': 'space-between', 'padding': '10px 0', 'margin': '0 0 10px 0px'}),

    html.Div(children=[
        dcc.Dropdown(
            id = 'Date',
            options = [
                {'label': 'All 7 days', 'value': 'All'},
                {'label':'5th June 2019', 'value':"'2019-06-05'"},
                {'label':'6th June 2019', 'value':"'2019-06-06'"},
                {'label':'7th June 2019', 'value':"'2019-06-07'"},
                {'label':'8th June 2019', 'value':"'2019-06-08'"},
                {'label':'9th June 2019', 'value':"'2019-06-09'"},
                {'label':'10th June 2019', 'value':"'2019-06-10'"},
                {'label':'11th June 2019', 'value':"'2019-06-11'"}
            ],
            value = 'All',
            clearable=False,
            placeholder='Select a date',
            style={'background-color': '#b2d5f7','position': 'absolute', 'width': '45%','right': '0'}
        ),
        ],style={'position': 'relative','height': '40px'}),

    html.Div([
            dcc.Graph(
                id='TopMC',
                figure={
                    'data': [trace1],
                    'layout':
                    go.Layout(title='Top Level MetaCategories of 7 days', xaxis = {'title':'MetaCategory Name','type':'category', 'ticks':'outside'},
                              yaxis = {'title':'Number of Unique Users'}, barmode = 'overlay',
                              plot_bgcolor = colors['background'],
                              paper_bgcolor = colors['background'],
                              font = {'color': colors['text']},
                              margin=dict(b=130)
                        )
                }, style={'padding-bottom': '15px'})
            ], style={'padding': '5px', 'width': '100%'}),

    html.Div([
        html.Div([
            dcc.Graph(
                id='channel',
                figure={
                    'data': [go.Bar(
                        x = [channel[0][0], channel[1][0], channel[2][0]],
                        y = [channel[0][1], channel[1][1], channel[2][1]]
                    )],
                    'layout':
                    go.Layout(title='Top Channels of 7 days', xaxis = {'title':'Channel Type','type':'category'},
                              yaxis = {'title':'Number of Unique Users'}, barmode = 'overlay', autosize = True,
                              plot_bgcolor = colors['background'],
                              paper_bgcolor = colors['background'],
                              font = {'color': colors['text']}
                    )
                }
                )
        ], style={'width': '50%'}),
        html.Div([
            dcc.Graph(
                id='CookieAgeTrend',
                figure={
                    'data': [
                        go.Bar(
                            x=['0', '1', '2', '3', '4', '5', '6'],
                            y=[cookieagetrend[0][1], cookieagetrend[1][1], cookieagetrend[2][1], cookieagetrend[3][1],
                               cookieagetrend[4][1], cookieagetrend[5][1], cookieagetrend[6][1]],
                        )
                    ],
                    'layout': go.Layout(
                        title='Cookie Churn trend on Impression logs (%)',
                        xaxis={'title': 'Age (days)', 'type': 'category'}, yaxis={'title': 'Percentage Cookies alive'},
                        barmode='overlay',
                        plot_bgcolor=colors['background'],
                        paper_bgcolor=colors['background'],
                        font = {'color': colors['text']})
                }),
        ], style={'width': '50%', 'padding-left': '5px'})
    ], style={'display': 'flex'}),

    html.Div([
        dcc.Graph(
                figure={
                    'data': [{
                        'lat': latitude, 'lon': longitude, 'text': information, 'hoverinfo': 'text', 'type': 'scattermapbox',
                    'marker':{"color": '#f53636'}}],
                    'layout': {
                        'mapbox': {
                            'accesstoken': (
                                    'pk.eyJ1IjoiY2hyaWRkeXAiLCJhIjoiY2ozcGI1MTZ3M' +
                                    'DBpcTJ3cXR4b3owdDQwaCJ9.8jpMunbKjdq1anXwU5gxIw'
                            )
                        },
                        'margin': {
                            'l': 0, 'r': 0, 'b': 0, 't': 0
                        },
                    }
                }
            )
    ], style={'padding-top': '20px'})
])
noPage = html.Div([
    html.H3("Page not found.")
])

