# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 02:07:13 2021

@author: rodbl
"""

# Plotly / Dash
import dash
import plotly.graph_objects as go
import plotly.io as pio
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.figure_factory as ff
import dash_table

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots
from dash.long_callback import DiskcacheLongCallbackManager

# General
import pandas as pd
import numpy as np
import pickle

# Sklearn
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier

# load the model from disk
filename = 'latam_model.sav'
model = pickle.load(open(filename, 'rb'))


#########
# Styles
########


# Icons
FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"


# external CSS stylesheets
app = dash.Dash(__name__, title='Alpha Challenge | Rodolfo Blasser',
                external_stylesheets=[FONT_AWESOME],
                prevent_initial_callbacks=False)

#server = app.server




## Model Function
def prob(val1, val2, val3, val4):
    
    # val1 = "diego"
    # val2 = "mendonca"
    # val3 = int(0)
    # val4 = int(205)
    
    
    data = {'Name': [val1], "LastName": [val2], 'NumberOfRecommendations': [val3], 'NumberOfConnections': [val4]}
    
    df = pd.DataFrame(data, index=[0])
     
     
    
    ## Evaluate if compound Name/Last Name 
    def words(row):
        try:
            if (" ") in row:
                return 1
            else:
                return 0
        except:
            return 0

    df['Name_comp'] = df['Name'].apply(lambda row: words(row))
    df['LastName_comp'] = df['LastName'].apply(lambda row: words(row))


    ## Evaluate if str is ASCII encoded
    def ascii(row):
        try:
            if row.isascii() == True:
                return 1
            else:
                return 0
        
        except:
            return 0
        

    df['Name_is_ascii'] = df['Name'].apply(lambda row: ascii(row))
    df['LastName_is_ascii'] = df['LastName'].apply(lambda row: ascii(row))
    
    print(df)

    ## Scaling
    scaler = MinMaxScaler()
    cols = ['NumberOfRecommendations', 'NumberOfConnections' ]
    df[['NumberOfConnections','NumberOfRecommendations']] = scaler.fit_transform(df[['NumberOfConnections','NumberOfRecommendations']])
    print(df)

    ## Grab IDs
    #ids = df['PersonId']


    # load the model from disk
    filename = 'latam_model.sav'
    model = pickle.load(open(filename, 'rb'))

    # Reindex
    cols = ['NumberOfRecommendations', 'NumberOfConnections', "Name_is_ascii", "LastName_is_ascii", "Name_comp", "LastName_comp"]
    df = df.reindex(columns=cols)

    ## Predict Probabilities
    X = df.values
    probs = pd.DataFrame(model.predict_proba(X))
    prob_yes = probs[1].item()
    print("Probability: " + str(prob_yes))
    #prob_yes = '{:.0%}'.format(prob_yes)
    # probs.head(3)

    return prob_yes

########
# FIG 1
########
gauge1 = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = 0,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {'axis': {'range': [None, 1]},
             'steps' : [
                 {'range': [0, 1], 'color': "lightgray"},
                 {'range': [.75, 1], 'color': "gray"}],
             'threshold' : {'line': {'color': "red", 'width': 3}, 'thickness': 0.75, 'value': 4100}}
        ))

# Transparent background
gauge1.update_layout({
                        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                        'width' : 400,
                        'height': 350,
                        'template':"plotly_dark"
                        
                        })

gauge1.update_layout(title =  dict(text ="Latam Country Probability",
                               font =dict(family='Sherif',
                               size=14,
                               color = 'rgba(0, 36, 227, 0.8)')))

gauge1.update_layout(font = {'color': "#86f653", 'family': "Arial"})

###################
# Pred Button Style
##################
white_button_style = {'background-color': '#86f653',
                      "border": "rgba(0, 0, 0, 0.3)",
                      'color': 'black',
                      'height': '30px',
                      'width': '170px',
                      'margin-top': '50px',
                      'margin-left': '30px'}

# =============================================================================
# BODY
# =============================================================================

#############
# Layout
#############
app.layout = html.Div(style={
                             'background-repeat': 'no-repeat',
                             'background-position': 'right top',
                             'height' : "50%",
                             'width' : "100%"
                             },
                      children=[
    
                        
    
    html.Div(html.P(['Alpha Challenge Tool by ', html.A("Rodolfo Blasser", href="https://www.linkedin.com/in/rodblasser/"), html.Br(), ''])),
    
    html.Br(),
    

    html.Div(html.P(['Considering the following 4 inputs, this solution will determine if the person is located in Latin America ', html.Br(), ''])),
    
    
    
    dbc.Row([dbc.Col([
                html.Label(['Complete First Name.'], style={'font-weight': 'bold', "text-align": "center"}),
                html.Br(),
                dbc.Input(id="input1", placeholder="", type="text"),
                html.Br(),
                html.P(id="output1"),
                ]),
            
            dbc.Col([
                html.Label(['Complete Last Name.'], style={'font-weight': 'bold', "text-align": "center"}),
                html.Br(),
                dbc.Input(id="input2", placeholder="", type="text"),
                html.Br(),
                html.P(id="output2"),
                ]),
                
                
            dbc.Col([
                html.Label(['No. of Recommendations.'], style={'font-weight': 'bold', "text-align": "center"}),
                html.Br(),
                dbc.Input(id="input3",placeholder="", type="number", min=0, max=100000, step=1),
                html.Br(),
                html.P(id="output3"),
                ]),
                
            dbc.Col([
                html.Label(['No. of Connections'], style={'font-weight': 'bold', "text-align": "center"}),
                html.Br(),
                dbc.Input(id="input4", placeholder="", type="number", min=0, max=100000, step=1),
                html.Br(),
                html.P(id="output4"),
                    ]),
                ]),
    
    

   html.Div([
            html.Button('Calculate Probability', id='button',style=white_button_style),
            html.Div(id='my-div')
            ]),
   
   html.Div([
       dcc.Graph(
       id='gauge1',  style={'display': 'inline-block',"border":"0px black solid"},
       figure=gauge1),


            ])





])



############
# Callbacks
############
# Prediction Gauge 1
@app.callback(
    dash.dependencies.Output('gauge1', 'figure'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.Input('input1', 'value')],
    [dash.dependencies.Input('input2', 'value')],
    [dash.dependencies.Input('input3', 'value')],
    [dash.dependencies.Input('input4', 'value')],prevent_initial_call=True)
 


def update_output(n_clicks,val1, val2, val3, val4):
    
    # ctx = dash.callback_context
    
    if n_clicks == None:
        n_clicks = 0
    else:
        n_clicks = n_clicks
        
        
    
    if n_clicks < 1:
        
        raise PreventUpdate
                
    else:
        
        done = prob(val1, val2, val3, val4)

        
        gauge1 = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = done,
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {'axis': {'range': [None, 1]},
                     'steps' : [
                         {'range': [0, 1], 'color': "lightgray"},
                         {'range': [.75, 1], 'color': "gray"}],
                     'threshold' : {'line': {'color': "red", 'width': 3}, 'thickness': 0.75, 'value': 4100}}
                ))
        
        # Transparent background
        gauge1.update_layout({
                                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                'width' : 400,
                                'height': 350,
                                'template':"plotly_dark"
                                
                                })
        
        gauge1.update_layout(title =  dict(text ="Latam Country Probability",
                                       font =dict(family='Sherif',
                                       size=14,
                                       color = 'rgba(0, 36, 227, 0.8)')))
        
        gauge1.update_layout(font = {'color': "#86f653", 'family': "Arial"})
    
        return gauge1



if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run_server(host= '0.0.0.0',debug=True)








