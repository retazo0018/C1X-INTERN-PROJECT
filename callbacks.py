from dash.dependencies import Input, Output

from app import app

import pandas as pd

import plotly.graph_objs as go

from components import functions


colors = {
    'background': '#111111',
    'text': '#fafafa'
}

@app.callback(
    Output('TopMC','figure'),
    [Input ('Date','value')])
def update_graphic(Date):
    conn, cursor = functions.connection()
    if (Date == 'All'):
        k = "select mcid, uuid from click_agg_poc"
        Date = "7 days"
    else:
        k = "select mcid, uuid from click_agg_poc where date_utc = " + Date

    cursor.execute(k)
    day = cursor.fetchall()
    day = pd.DataFrame(day)
    day.columns = ['MCID','UUID']
    day = day[day['UUID']!='undefined']
    new = day.groupby(day.MCID)
    category = new.apply(lambda x:x['UUID'].unique())
    category = pd.DataFrame(category)
    category.columns = ['UUID']
    top = {}
    for index,row in category.iterrows():
        top.update({index:0})
        for i in row:
            c = len(i)
        top[index]=c
    topCategory = [ [k,v] for k, v in top.items() ]
    topCategory.sort(key = lambda x: x[1], reverse=True)
    df = pd.DataFrame(topCategory)
    df.columns = ['MCID','Count']
    cat = pd.read_csv("assets/category-soka.csv")
    cat = cat[['id','name']]
    cat = pd.DataFrame(cat)
    cat.columns = ['MCID','Name']
    cat.head()
    result = pd.merge(df, cat, on='MCID')
    final = result.head(10)
    pv = final.set_index('Name')
    trace1 = go.Bar(x=pv.index, y=pv['Count'], name='TopMC')
    return{
        'data': [trace1],
        'layout': go.Layout(title='Top Level MetaCategories of '+Date, xaxis = {'title':'MetaCategory Name','type':'category', 'ticks':'outside'},
                            yaxis = {'title':'Number of Unique Users'}, barmode = 'overlay',
                            plot_bgcolor=colors['background'],
                            paper_bgcolor=colors['background'],
                            font={'color': colors['text']},
                            margin=dict(b=130)
                        )
    }

@app.callback(
    Output('channel','figure'),
    [Input ('Date','value')])
def updatechannel(Date):
    conn, cursor = functions.connection()
    if (Date == 'All'):
        k = "select channel, count(*) from click_agg_poc group by channel"
        Date = "7 days"
    else:
            k = "select channel, count(*) from click_agg_poc where date_utc = " + Date + " group by channel"
    cursor.execute(k)
    channel = cursor.fetchall()
    nchannel=[]
    for i in range(len(channel)):
        temp = []
        if(channel[i][0] == 'M'):
            temp.append('Mobile')
            temp.append(channel[i][1])
            nchannel.append(temp)
        elif (channel[i][0] == 'D'):
            temp.append('Desktop')
            temp.append(channel[i][1])
            nchannel.append(temp)
        else:
            temp.append('App')
            temp.append(channel[i][1])
            nchannel.append(temp)
    nchannel = sorted(nchannel, key=lambda x: x[1], reverse=True)
    return{
        'data': [go.Bar(
            x=[nchannel[0][0], nchannel[1][0], nchannel[2][0]],
            y=[nchannel[0][1], nchannel[1][1], nchannel[2][1]]
        )],
        'layout':
        go.Layout(title='Top Channels of '+Date, xaxis={'title': 'Channel Type', 'type': 'category'},
                  yaxis={'title': 'Number of Unique Users'}, barmode='overlay',
                  plot_bgcolor = colors['background'],
                  paper_bgcolor = colors['background'],
                  font = {'color': colors['text']}
                  )
    }

