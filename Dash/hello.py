import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Layout of the page
# Usually, we use a container (html.Div) to include all compoments
app.layout = html.Div(children=[
    # header H1
    html.H1(children='PyCon Taiwan tutorial'),

    # container, children is the first parameter, and it can be text.
    html.Div(children="Hello Dash",
             style={'textAlign': 'center','color': '#16A085','fontSize':'350%',}
             # in html, style parameters such as "text-align" became "textAlign",
             # "font-size" became "fontSize" (camelCased)
    ),
    
], style={'backgroundColor': 'pink', 'padding': '5%'}
)


if __name__ == '__main__':
    # use run_server to start server
    # debug is True, if you fix the code, the effect will be simutanuous.
    app.run_server(debug=True)
