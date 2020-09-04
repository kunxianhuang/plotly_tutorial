import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([
    # H1 header
    html.H1("Dash Layout"),
    # container Div for next two components
    html.Div([
        # Dropdown menu of labels and values
        dcc.Dropdown(    
            options=[
                {'label': 'Taipei city', 'value': 'TPE'},
                {'label': 'New Taipei city', 'value': 'TPH'},
                {'label': 'Taoyuan city', 'value': 'TYC'},
                {'label': 'Taichung city', 'value': 'TXG'},
                {'label': 'Tainan', 'value': 'TNN'},
                {'label': 'Kaohsiung city', 'value': 'KHH'}
            ],
            multi=True, # Multiple answer
            value="TNN" # initial value of dropdown
        ),
        # radio menu of labels and values
        dcc.RadioItems(
            options=[
                {'label': 'Taipei city', 'value': 'TPE'},
                {'label': 'New Taipei city', 'value': 'TPH'},
                {'label': 'Taoyuan city', 'value': 'TYC'},
                {'label': 'Taichung city', 'value': 'TXG'},
                {'label': 'Tainan', 'value': 'TNN'},
                {'label': 'Kaohsiung city', 'value': 'KHH'}
            ],
            value='TNN' # initial value of radio
        ),  
    ]),
    # container for the line-graph
    html.Div([
    # graph of line graph
        dcc.Graph(
            id='line-graph', # id of the component for callback
            figure=px.line(x=[1,2,3,4,5], y=[1.2,4.5,2.4,3.1,5.1], title='Line figure')
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}), # style of the graph
    # container for the scatter-graph
    html.Div([
        # graph of scatter graph
        dcc.Graph(
            id='scatter-graph', # id of the component for callback
            figure=px.scatter(x=[1,2,3,4,5], y=[1.2,4.5,2.4,3.1,5.1], title='Scatter figure')
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}) # style of graph
    
],
                      style={'height': 300} 
)

if __name__ == '__main__':
    app.run_server(debug=True)
