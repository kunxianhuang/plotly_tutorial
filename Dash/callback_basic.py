# Run this app with `python callback_basic.py` and
# visit http://127.0.0.1:8050/ in your web browser

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# list of graph functions
graph_type_list = [px.line, px.scatter, px.bar]


app.layout = html.Div([
    html.H1("Dash Callback", style={'textAlign': 'center'}),
    
    html.Div([
        # Dropdown selection for graph type
        dcc.Dropdown(
            id ='graph_dropdown', # id for corresponding call back
            options=[
                {'label': type_.__name__, 'value': num} for num, type_ in enumerate(graph_type_list)
            ],
            multi=False,
            value=1, # default is scatter plot
        ),
        # Button for trigger call back
        html.Button(
            id='change_button', # id for corresponding call back
            children='Update Graph',
        ),
    ]),
    html.Div([
        # Graph component for showing graph
        dcc.Graph(
            id='output_graph', # id for corresponding call back
            # figure
        )
    ], style={'width': '89%', 'display': 'inline-block', 'padding': '0 20'}),
    
],
                      style={'height': 300}
)

# use app.callback as a decorator,to access/pass parameters from/to the corresponding component

# Output: passing output component's value, for example output graph, text, and etc.
#         1st parameter is component's id, 2nd parameter is property of the component
# Input: if the corresponding property of component varies, for example number click, value, and etc.
#        the callback is triggered, and pass the property into function's parameter.
#        1st parameter is component's id, 2nd parameter is property of the component
# State: if callback is triggered, the property's value will be pass into parameter of the function, too.
#        1st parameter is component's id, 2nd parameter is property of the component

# 
#
@app.callback(Output('output_graph', 'figure'),
             [Input('change_button', 'n_clicks')],
            [State('graph_dropdown', 'value')]
            )
def update_graph(n_clicks, selected_value):
    return graph_type_list[selected_value](x=[1,2,3,4,5], y=[10,5,3,6,-2])


if __name__ == '__main__':
    app.run_server(debug=True)
