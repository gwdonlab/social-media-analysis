import dash
import plotly.express as px
from dash import dcc
from dash.dependencies import Input,Output
from dash import html
import pandas as pd
pd.set_option('max_columns', 19)

#Load external stylesheets and assign tab styles
external_stylesheets=["https://unpkg.com/purecss@2.1.0/build/pure-min.css" ]
my_app=dash.Dash('My App',external_stylesheets=external_stylesheets)

#Load dataset - replace the data file path according to the scraped data
data=pd.read_csv('data.csv')

#Define the tabs
my_app.layout=html.Div([html.H1('Dashboard for Analysis',style={'textAlign':'center'}),
                        html.Br(),
                        dcc.Tabs(id='tabs1',
                                 children=[
                                     dcc.Tab(label='Basic Information',value='info'),
                                     dcc.Tab(label='Top videos',value='top'),
                                 ]),
                        html.Div(id='layout')

])

#Layout of first tab
tab1_layout=html.Div([html.Br(),
                               html.P('Click one option to understand the basic information about the data!',style={'margin': '1px','textAlign':'left'}),
                               html.Br(),
                               dcc.RadioItems(id='infos',options=[
                                   {'label':'Column Names','value':'Column'},
                                   {'label':'Display data','value':'head'},
                                   {'label':'Channels and their video count','value':'info'
                               }],
                               value='Column',inputStyle={"margin-left": "20px"}),
                               html.Plaintext(id='datainfo',style = {'backgroundColor':'#111111','color':'#FFFFFF','font-size':'15px'}),

])

#Layout for second tab
tab2_layout=html.Div([html.Br(),
                      html.P('Select an option to sort the dataset accordingly!',
                             style={'margin': '1px', 'textAlign': 'left'}),
                      html.Br(),
                      dcc.Dropdown(id='drop1', options=[
                          {'label': 'Number_of_views', 'value': 'Number_of_views'},
                          {'label': 'Number_of_Likes', 'value': 'Number_of_Likes'},
                          {'label': 'Number_of_Comments', 'value': 'Number_of_Comments'
                           }],
                                     value='Number_of_Comments'),
                        html.Br(),
                      html.P('Click to download the sorted dataset!', style={'margin': '1px', 'textAlign': 'left'}),
                     html.Br(),
                      html.Button("Download CSV", id="btn_csv",
                                  style={'background-color': '#111111', 'color': '#FFFFFF'}),
                      dcc.Download(id="download-dataframe-csv"),
                      html.Br(),html.Br(),
                      ])


@my_app.callback(Output(component_id='layout',component_property='children'),
                 [Input(component_id='tabs1',component_property='value')
                ])

def update_layout(ques):
    if ques=='info':
        return tab1_layout
    elif ques=='top':
        return tab2_layout


#Callback for tab1
@my_app.callback(Output(component_id='datainfo',component_property='children'),
                 [Input(component_id='infos',component_property='value')])
def update_graph(input):
    if input=='Column':
        cols=data.columns
        return ['\n'+j for j in cols]
    elif input=='head':
        return f'{data.head()}'
    elif input=='info':
         return f'{data.Channel_Title.value_counts()}'

#callbacks for tab2
@my_app.callback(
    Output("download-dataframe-csv", "data"),
    [Input(component_id='drop1',component_property='value'),Input("btn_csv", "n_clicks")],
    prevent_initial_call=True,
)
def func(drop1,n_clicks):
    data_sort=data.sort_values(by=drop1,ascending=False)
    return dcc.send_data_frame(data_sort.to_csv, "data_sorted.csv")

my_app.run_server(port=8033,host='0.0.0.0')