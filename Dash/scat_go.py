# Run this app with `python scat.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')
continents = df.continent.unique().tolist()


data = [go.Scatter(
    x=df[df.continent==continent]["gdp per capita"],
    y=df[df.continent==continent]["life expectancy"],
    mode='markers',
    text=df[df.continent==continent]["country"],
    hoverinfo=['x','y'],
    name=continent,
    marker=dict(
        size=df[df.continent==continent]["population"]/0.5e+7,
        sizeref=2.*max(df[df.continent==continent]["population"]/0.5e+7)/(12.**2)
        ))
        for continent in continents
        ]


layout = dict(title="gdp verse life expectancy",xaxis_type="log",
              xaxis_title_text='gdp per capita', # xaxis label
              yaxis_title_text='life expectancy')


fig = go.Figure(data=data,layout=layout)
app.layout = html.Div([
    html.H1("plotly.graph_objects"),
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
