#!/usr/bin/env python3
import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
import pandas as pd


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__)
app.layout = html.Div(
    html.Div([
        html.H4('TILT Live view'),
#	html.H6('Last counts:'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*7000, # in milliseconds
            n_intervals=0
        )
    ])
)


@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    df=pd.read_csv('/home/gluk/forstream.csv', index_col=None)
    df1=df.tail(1)
    
    hae1=df1['HAE'].tolist()
    hae=float(hae1[0])

    han1=df1['HAN'].tolist()
    han=float(han1[0])

    hk21=df1['HK2'].tolist()
    hk2=float(hk21[0])

    tm1=str(df1['T'].tolist())
#    tm=datetime.datetime.strptime(tm1, format='%Y:%m:%d:%H:%M:%S')
#    tm1=(tm1)
#    print(tm1)
#    tm1=pd.to_datetime(df1['T'], format='%Y:%m:%d:%H:%M:%S')
#    tm1=list(tm1)
#    print('list :', tm1)
#    print(str(tm1))
 #   tm1=int(tm1.timestamp())
 #   print(tm1)

    style = {'padding': '2px', 'fontSize': '11px'}
    return [
	html.H1('The data is updated once per hour. Last update time :  {}, recent counts:'.format(tm1) , style=style),
        html.Span('HAE E down     : {0:.2f}, mcRad.'.format(hae), style=style),
        html.Span('  HAN N down     : {0:.2f}, mcRad.'.format(han), style=style),
        html.Span('  Temperature:   : {0:.2f}, degree celsius.'.format(hk2), style=style),
#	html.H1(tm1, style=style)
    ]


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
#    link_size=[2]
    df=pd.read_csv('/home/gluk/forstream.csv')
    ln=len(df)
    if ln<100:
	    df1=df.tail(ln)
    else:
	    df1=df.tail(100)
        
    # Create the graph with subplots
#    fig = plotly.tools.make_subplots(rows=3, cols=2,
    fig = plotly.tools.make_subplots(rows=4, cols=2,
#				    specs=[[{'rowspan': 2}, {}], [None, {}]], !!!с двумя строками работало

#				    specs=[[{'rowspan': 3}, {}], !!!С тремя строками работало
#					     [None, {}],
#					    [None, {}],
#					    ], 
				    specs=[[{'rowspan': 4}, {}], #
					    [None, {}],
					    [None, {}],
					    [None, {}],
					    ],
				    

				    shared_xaxes=True,
				    shared_yaxes=True,
				    vertical_spacing=0.03,
				    horizontal_spacing = 0.02,
				    column_widths=[0.35, 0.65]
				    )
    fig['layout']['margin'] = {
        'l': 0, 'r': 0, 'b': 0, 't': 0
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
#    fig['layout']={'scaleratio': 1.0}

    fig.append_trace({
        'x': df1['T'],
        'y': df1['HAE'],
        'name': 'HAE',
        'mode': 'lines+markers',
        'type': 'scatter'
    },1,2)
    fig.append_trace({
        'x': df1['T'],
        'y': df1['HAN'],
        'text': df1['T'],
        'name': 'HAN',
        'mode': 'lines+markers',
        'type': 'scatter'
    },2,2)
    fig.append_trace({
        'x': df1['T'],
        'y': df1['HK2'],
        'text': df1['T'],
        'name': 'HAN',
        'mode': 'lines+markers',
        'type': 'scatter'
    },3,2)
    fig.append_trace({
        'x': df1['T'],
        'y': df1['PS'],
        'text': df1['T'],
        'name': 'PS',
        'mode': 'lines+markers',
        'type': 'scatter'
    },4,2)
    fig.append_trace({
        'x': df1['HAE'],
        'y': df1['HAN'],
        'text': df1['T'],
        'name': 'HAE vs HAN',
        'mode': 'lines+markers',
        'type': 'scatter',
	'line_color': 'rgba(255,255,255,255)',
	'line_width':1

    }, 1,1)
    fig.update_layout(height=700,
        template="ggplot2",
        margin=dict(
            t=10,
            b=0,
#	    'scaleanchor': 'x',
#	    'scaleratio': 1.0

            ))
    return (fig)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0')#(debug=True)
