import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input ,Output

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets= ['asset/main.css']
app= dash.Dash(__name__, external_stylesheets=external_stylesheets)
server= app.server


State= ['Andaman and Nicobar Islands', 'Andhra Pradesh',
 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh',
 'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu',
 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh',
 'Jammu and Kashmir', 'Jharkhand', 'Karnataka',
 'Kerala', 'Ladakh', 'Madhya Pradesh',
 'Maharashtra', 'Manipur', 'Meghalaya',
 'Mizoram', 'Nagaland', 'Odisha',
 'Puducherry', 'Punjab', 'Rajasthan',
 'Sikkim', 'Tamil Nadu', 'Telangana',
 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']
theme =  {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

colors = {
    'background': '#111111',
    'text': '#7FDBFF',
    'font_family': 'Lobster'
}
#data plot
mapbox_access_token= 'pk.eyJ1IjoiaGl0ZXNoaGVkd2lnIiwiYSI6ImNrZmR5aDE0cTFuYjczNm81cXJhNHNhNDAifQ.jrWakhEV-U2F2EJdFGW6RQ'

MapTime= pd.read_csv('data/MapTime_new.csv')
fig = px.density_mapbox(MapTime, lat='Lat', lon='Long',
                        z='Total',radius=70, zoom=0.8,
                        hover_name=MapTime['Country/Region'],
                        mapbox_style="dark",
                        color_continuous_scale='darkmint',
                        )
fig.update_layout(mapbox_accesstoken=mapbox_access_token)
#fig.update_layout(paper_bgco)

#AllIndia3D:
@app.callback(
    Output('3DViz','figure'),
    [Input('Select State/UT_k','value')]
)
def AllIndia3D(States):
    CovidIndia= pd.read_csv('data/CovidIndia.csv')
    if type(States)==str:
        CovidIndia11=CovidIndia[CovidIndia['State/UnionTerritory'].isin([States])]
        print('string')
        fig1=px.scatter_3d(CovidIndia11, x='Confirmed', y='Cured', z='Deaths', color='State/UnionTerritory',
                        hover_name='State/UnionTerritory', hover_data=['Date'],
                        template='plotly_dark', opacity=0.7, title='Covid plot',size_max=10,
                        labels={'Confirmed': 'Confirmed', 'Cured': 'Cured', 'Deaths':'Deaths'})
        return fig1
        
    if type(States)==list:
        print('List')
        CovidIndia12=CovidIndia[CovidIndia['State/UnionTerritory'].isin(States)]
        fig2=px.scatter_3d(CovidIndia12, x='Confirmed', y='Cured', z='Deaths', color='State/UnionTerritory',
                        hover_name='State/UnionTerritory', hover_data=['Date'],
                        template='plotly_dark', opacity=0.7, title='Covid plot',size_max=10,
                        labels={'Confirmed': 'Confirmed', 'Cured': 'Cured', 'Deaths':'Deaths'})
        return fig2

        


##StateWise Analysis:
@app.callback(
    Output('StateWise','figure'),
    [Input('PosNeg','value')]
)
def PieChart(PosNeg):
    StateWise1= pd.read_csv('data/State_sample.csv')
    StateWise= StateWise1.groupby('State').sum().reset_index()
    fig11= px.pie(StateWise, values=PosNeg, names='State',
       color_discrete_sequence=px.colors.sequential.RdBu, hole=.3)
    return fig11

@app.callback(
    Output('lineplot','figure'),
    [Input('Select State/UT','value'),
     Input('caseresult', 'value')]
)
def StateLine(States, caseresult):
    # default would be delhi
    print(States)
    StateWise_t=pd.read_csv('data/State_sample.csv')
    #StateWise[StateWise['State'].isin(Name)]
    if type(States)==str:
        StateWise1=StateWise_t[StateWise_t['State'].isin([States])]
        print('string')
        fig1=px.line(StateWise1, x='Date', y=caseresult,color="State")
        return fig1


    if type(States)==list:
        StateWise2=StateWise_t[StateWise_t['State'].isin(States)]
        fig2=px.line(StateWise2, x='Date', y=caseresult,color="State")
        return fig2
        
    

app.layout =html.Div([
    html.Div([        
        html.Div([
        html.H1(children='COViz-ualize',
                className = "nine columns",
                style={
                'textAlign': 'center',
                'color': '#3b2c2c' ,
                'family': 'monospace',
                "font-size": "45px"
            }),

        html.Div(children='''
            An interactive space to understand COVID-19 insight
        ''', style={
            'textAlign': 'center',
            'color': '#681b1b',
            'text-decoration': "underline"
        }),
        

        dcc.Graph(
            id='World Map',
            figure=fig
        )])
    ], className='row' ),

        html.Div([
        html.Div([
            html.H2(children='State Wise Analysis of COVID-19',
            style={
                'color':'#031fa5',
            }),
            html.P('-------------------------------------------------------------------------------------------------------'),

            dcc.RadioItems(
                id="caseresult",
            options= [
            {'label': 'Total Samples', 'value':'TotalSamples'},
            {'label':'Negative', 'value':'Negative'},
            {'label': 'Positive', 'value': 'Positive'}
            ],
        value='TotalSamples'
            ),
            html.Br(),
            html.Br(),
            dcc.Dropdown(
                id="Select State/UT",
                options= [{'label':k, 'value':k} for k in State],
                value= "Delhi",
                multi= True
            ),   #endofdropdown
        dcc.Graph(
            id="lineplot",
        ),
        
        ], className= "six columns"),
        

        html.Div([html.H2(children='Cases Distribution',
            style={
                'color':'#031fa5',
            }),
            html.P('-------------------------------------------------------------------------------------------------------'),
        html.Br(),
        dcc.RadioItems(
            id="PosNeg",
            options= [
            {'label': 'Positive', 'value':'Positive'},
            {'label':'Total Samples', 'value':'TotalSamples'},
            ], 
            value= "TotalSamples"),
        dcc.Graph(
        id="StateWise",
        
        ),
        
        ],className='six columns'),

        html.Div([
            html.H4(children='3D Visualization',

                style={
                'textAlign': 'Left',
                'color': '#031fa5' ,
                'family': 'monospace',
                "font-size": "25px"
            }),
            html.P('-------------------------------------------------------------------------------------------------------'),
            html.P('Select Cities'),
            dcc.Dropdown(
                id="Select State/UT_k",
                options= [{'label':k, 'value':k} for k in State],
                value= "Delhi",
                multi= True
            ),
            html.Br(),
            dcc.Graph(
                id="3DViz",
            )
        ])

        ],className='row'),



]
     )

if __name__=='__main__':
    app.run_server(port=5006, debug=True)
