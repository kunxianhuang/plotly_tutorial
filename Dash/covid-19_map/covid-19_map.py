# Run this app with `python covid-19_map.py` and
# visit http://127.0.0.1:8050/ in your web browser
#
# data from Center for Systems Science and Engineering (CSSE) at Johns Hopkins University
# https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series
# Data are licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0) by the Johns Hopkins University on behalf of its Center for Systems Science in Engineering. Copyright Johns Hopkins University 2020.

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def renameTHMK(df):
    """
    Rename country name of Taiwan, Hong Kong, Macau, and Korea South
    """
    # rename column Country/Region and Province/State
    df.rename(columns={"Country/Region": "country", "Province/State": "state"},inplace=True)
    # Taiwan* -->Taiwan
    df.loc[df.country=="Taiwan*","country"] = "Taiwan"
    # Hong Kong
    df.loc[df.state=="Hong Kong","country"] = "Hong Kong"
    # Macau
    df.loc[df.state=="Macau","country"] = "Macau"
    # Korea, South ->Korea South
    df.loc[df.country=="Korea, South","country"] = "Korea South"


    return df


def agg_merge(df_data,df_code):
    # sum up people number in the same country
    df_tot = df_data.groupby(["country"]).sum().reset_index()


    # combine country name and its iso alpha-3 code
    df_tot = pd.merge(df_tot,df_code,left_on="country",right_on="name",how='left').drop(code_columns,axis=1)
    return df_tot

def rename_agg_us(df_data):
    # rename column Country/Region and Province/State
    df_data.rename(columns={"Country_Region": "country", "Province_State": "state"},inplace=True)

    # sum up pepple number in US
    df_tot = df_data.groupby(["country"]).sum().reset_index()

    df_tot["alpha-3"] = "USA"

    return df_tot

# country code of iso 3166 alpha-3
df_country_code = pd.read_csv('data/country_code.csv')


code_columns = df_country_code.columns.to_list()
code_columns.remove("alpha-3")



# data from CSSE at Johns Hopkins University
df_confirm = pd.read_csv('data/time_series_covid19_confirmed_global.csv')

df_confirm = renameTHMK(df_confirm)

dates = df_confirm.columns.to_list()[4:] # retrieve dates

# confirmed covid-19 person by country
df_confirm_country = agg_merge(df_confirm,df_country_code)

# data from CSSE at Johns Hopkins University
df_US_confirm = pd.read_csv('data/time_series_covid19_confirmed_US.csv')

# rename some columns and sum up all county
df_US_confirm = rename_agg_us(df_US_confirm)

df_confirm_country = pd.concat([df_confirm_country,df_US_confirm], ignore_index=True)

# data from CSSE at Johns Hopkins University
df_death   = pd.read_csv('data/time_series_covid19_deaths_global.csv')

df_death = renameTHMK(df_death)

# covid-19 death person by country
df_death_country = agg_merge(df_death,df_country_code)

# data from CSSE at Johns Hopkins University
df_US_death = pd.read_csv('data/time_series_covid19_deaths_US.csv')

# rename some columns and sum up all county
df_US_death = rename_agg_us(df_US_death)

df_death_country = pd.concat([df_death_country,df_US_death], ignore_index=True)


df_data = {"confirmed":df_confirm_country,"death":df_death_country}

# Layout of webpage from here
app.layout = html.Div([
    html.H1("Covid-19 global map", style={'textAlign': 'center'}),

    html.Div([
        # radio to switch confirmed and death
        dcc.RadioItems(
            id='confirm-death-type',
            options=[{'label': i, 'value': i} for i in ['confirmed', 'death']],
            value='confirmed',
            labelStyle={'display': 'inline-block'}
        ),
        # graph of global map
        dcc.Graph(
            id='worldmap-covid-19',
            # set initial setting of  customdata content
            clickData={'points': [{'customdata': 'Taiwan'}]} # initial clickData
        )
    ], style={'width': '90%', 'display': 'inline-block', 'padding': '0 20', 'height':'900'}),
    html.Div([
        dcc.Graph(id='confirm-time-series'), # time-series plot of confirmed
        dcc.Graph(id='death-time-series'), # time-series plot of death
    ], style={'display': 'inline-block', 'width': '70%'}),

], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }
)


# switch confirmed/death in map
@app.callback(Output('worldmap-covid-19', 'figure'),
              [Input('confirm-death-type', 'value')])
def update_map(value):
    df = df_data[value]
    latest_date = dates[-1]


    # Draw Choropleth Maps
    # Reference:
    # https://plotly.com/python/choropleth-maps/
    figure = px.choropleth(df, locations="alpha-3",
                    color=latest_date, # accumulated confirmed/death persons
                    hover_name="country", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma)

    # Setting customdata attribute of clickData points
    figure.update_traces(customdata=df['country'])

    title_text = 'Covid-19 {} Global Map'.format(value)
    figure.update_layout(
        title_text=title_text,
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        # annotations text in graph
        annotations = [dict(
            x=0.55,
            y=0.1,
            xref='paper',
            yref='paper',
            text='Source: <a href="https://github.com/CSSEGISandData/COVID-19">\
            CSSE at Johns Hopkins University</a>',
        showarrow = False
        )])

    return figure


def create_time_series(dff, title):
    fig = px.scatter(dff, x='date', y='person')
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=False)
    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)
    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig

# callback when click a country
# showing the accumulated confirmed covid-19 patients
@app.callback(
    Output('confirm-time-series', 'figure'),
    [Input('worldmap-covid-19', 'clickData')])
def update_confirm_timeseries(clickData):
    # retrieve the customdata ("country") of the clicked point
    country_name = clickData['points'][0]['customdata']
    dff = df_data['confirmed']
    dff = dff[dff['country'] == country_name]
    dff_allcolumns = dff.columns.tolist()
    id_vars = [var for var in dff_allcolumns if var not in dates]

    dff = dff.melt(id_vars=id_vars,
             value_vars=dates,
             var_name="date",
             value_name="person")
    # convert text object to datetime64 format
    dff['date'] = pd.to_datetime(dff['date'], format='%m/%d/%y')

    title = '<b>{} accumulated covid-19 confirmed time-series</b><br>'.format(dff.country[0])

    return create_time_series(dff, title)


# callback when click a country
# showing the accumulated death covid-19 patients
@app.callback(
    Output('death-time-series', 'figure'),
    [Input('worldmap-covid-19', 'clickData')])
def update_death_timeseries(clickData):
    # retrieve the customdata ("country") of the clicked point
    country_name = clickData['points'][0]['customdata']
    dff = df_data['death']
    dff = dff[dff['country'] == country_name]
    dff_allcolumns = dff.columns.tolist()
    id_vars = [var for var in dff_allcolumns if var not in dates]
    #id_vars = ["country","Lat", "Long","alpha-3"]
    dff = dff.melt(id_vars=id_vars,
             value_vars=dates,
             var_name="date",
             value_name="person")
    # convert text object to datetime64 format
    dff['date'] = pd.to_datetime(dff['date'], format='%m/%d/%y')

    title = '<b>{} accumulated covid-19 death time-series</b><br>'.format(dff.country[0])

    return create_time_series(dff, title)

if __name__ == '__main__':
    app.run_server(debug=True)
