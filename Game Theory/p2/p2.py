import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
import pandas as pd
import dash_table
import numpy as np


#BACKEND CODE
class Player:
    def __init__(self,name,n):
        self.name = name
        self.nstrat = n
        self.strat=[]
        for i in range (0,n):
            self.strat.append(name+str(i))


def pureValue(matrix):
    '''Pure strategies game value'''
    p1g=[]
    for i in matrix :
       p1g.append(i[:,0])
    p1g=np.array(p1g)
    x=np.max(np.min(p1g,axis=0))
    y=np.min(np.max(p1g,axis=1))
    if x==y:
        return str(x)
    return None


def convertnewstruct(matrix,sizeA,sizeB):
    result=[]
    if sizeA == 2 and sizeB ==2 :
        result.append([matrix[0],matrix[1]])
        result.append([matrix[2],matrix[3]])
        return np.array(result)
    # elif sizeA == 3 and sizeB ==2 :
    #     result.append([matrix[0],matrix[1],matrix[2]])
    #     result.append([matrix[3],matrix[4],matrix[5]])
    #     return np.array(result)
    # elif sizeA == 2 and sizeB ==3 :
    #     result.append([matrix[0],matrix[2],matrix[4]])
    #     result.append([matrix[1],matrix[3],matrix[5]])
    #     return np.array(result)
    elif sizeA == 3 and sizeB ==3 :
        result.append([matrix[0],matrix[1],matrix[2]])
        result.append([matrix[3],matrix[4],matrix[5]])
        result.append([matrix[6],matrix[7],matrix[8]])
        return np.array(result)
    
        # return np.array(np.array([matrix[0],matrix[1]]),np.array([matrix[0],matrix[1]]))
        # return np.array(np.array([matrix[0],matrix[1]]),np.array([matrix[2],matrix[3]]))


def converttostr(input_seq, seperator):
    x=""
    for i in input_seq:
        i=str(i)
        final_str = seperator.join(i)
        x=x+(final_str)
    return x


def NashEquil(matrix,sizeA,sizeB):
    p1g=[]
    p2g=[]
    result=[]
    for i in matrix :
       p1g.append(i[:,0])
       p2g.append(i[:,1])
    p1g=np.array(p1g)
    p2g=np.array(p2g)
    if sizeA ==2 and sizeB ==2:
        a=p1g[0,0]-p1g[1,0]-p1g[0,1]+p1g[1,1]
        b=p1g[1,1]-p1g[0,1]
        q=b/a
        q2=1-q
        result.append(np.round([q,q2],decimals=3))
        a=p2g[0,0]-p2g[1,0]-p2g[0,1]+p2g[1,1]
        b=p2g[1,1]-p2g[1,0]
        q=b/a
        q2=1-q
        result.append(np.round([q,q2],decimals=3))
    if sizeA ==3 and sizeB ==3:
        t1=[p1g[0,0]-p1g[0,2]-p1g[1,0]+p1g[1,2],p1g[0,1]-p1g[0,2]-p1g[1,1]+p1g[1,2]]
        t2=[p1g[1,0]-p1g[1,2]-p1g[2,0]+p1g[2,2],p1g[1,1]-p1g[1,2]-p1g[2,1]+p1g[2,2]]
        t3=[p1g[1,2]-p1g[0,2],p1g[2,2]-p1g[1,2]]
        x=np.linalg.solve([t1,t2],t3)
        q=x[0]
        q2=x[1]
        q3=1-q-q2
        result.append(np.round([q,q2,q3],decimals=3))
        t1=[p2g[0,0]-p2g[0,1]-p2g[2,0]+p2g[2,1],p2g[1,0]-p2g[1,1]-p2g[2,0]+p2g[2,1]]
        t2=[p2g[0,1]-p2g[2,1]-p2g[0,2]+p2g[2,2],p2g[1,1]-p2g[2,1]-p2g[1,2]+p2g[2,2]]
        t3=[p2g[2,1]-p2g[2,0],p2g[2,2]-p2g[2,1]]
        x=np.linalg.solve([t1,t2],t3)
        q=x[0]
        q2=x[1]
        q3=1-q-q2
        result.append(np.round([q,q2,q3],decimals=3))
    return(np.array(result))







#FRONTEND CODE
def convert(number,weights):
    result=[]
    weights=np.flip(weights)
    for w in weights:
        result.append(int(number%w))
        number=int(number/w)
    result.reverse()
    return result

def getcol(tab,col):
    tab2 = np.array(tab)
    return tab2[:,col]

# Boostrap CSS.
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets.append('https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css')


app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.Nav([
            html.Div(
                children=[html.H3(children='TP2 : Game theory',
                                    style={
                                            'color': '#2bb1d2',
                                            'text-align': 'center'
                                        }, className="col-sm-11"
                                ),
                        html.Div(
                        [
                            dbc.Button("About", id="open"),
                            dbc.Modal(
                                [
                                    dbc.ModalHeader(
                                        html.H3("Game theory project developed by BANDOUI Nazim",style={'color': '#2bb1d2'})
                                    ),
                                    dbc.ModalBody(
                                        [
                                            html.P(" Explication (fontionnement et tt ... )"),
                                            html.Ul([
                                                html.Li([html.B("point 1 :"),html.P("Description 1")]),
                                                html.Li([html.B("Point 2 :"),html.P("Description 2")]),
                                                html.Li([html.B("Point 3 :"),html.P("Description 3")]),
                                                ])
                                        ] ),
                                    dbc.ModalFooter(
                                        dbc.Button("fermer", id="close", className="ml-auto")
                                    ),
                                ],
                                id="modal",
                                size="xl",
                            ),
                        ],className="col-sm-1"
                    )],className="container-fluid")
            ],className="navbar navbar-expand-lg shadow p-4 mb-4"),
    html.Button(id="add", n_clicks=0 , hidden="hidden"),
    html.Div(id='container', children=[]),
    html.Div(id='dropdown-container-output'),
    html.Div(id="matrix-container"),
    html.Div(id="final-result"),
    html.Footer([
                html.Div(['© USTHB, MIV 2019/2020'],className="copyright text-center")],className="footer")
],className="wrapper")

def generate_control_id(value):
    return 'Player{}'.format(value)

@app.callback(
    Output('container', 'children'),
    [Input('add', 'n_clicks')],
    [State('container', 'children')])
def display_dropdowns(n_clicks, children):
    if n_clicks == 0:
        DYNAMIC_CONTROLS= dcc.Input(
            id={
                 'type': 'players',
                 'index': "0",
            } ,
            placeholder="Player 1 strategies",
            type="number",
            value=2,
            min=2,
            max=3,
        )
        DYNAMIC_CONTROLS2= dcc.Input(
            id={
                 'type': 'players',
                 'index': "1",
            } ,
            placeholder="Player 2 strategies",
            type="number",
            value=2,
            min=2,
            max=3,
        )
        children.append(DYNAMIC_CONTROLS)
        children.append(DYNAMIC_CONTROLS2)
        return children

@app.callback(
    Output('dropdown-container-output', 'children'),
    [Input({'type': 'players', 'index': ALL}, 'value')]
)
def display_output(values):
    prod=1
    for (i, value) in enumerate(values):
        prod=prod*int(1 if value is None else value)
    s=str(prod)
    DYNAMIC_CONTROLS= dcc.Input(
        id="hiddenproduct",
        type="hidden",
        value=prod
    )
    return DYNAMIC_CONTROLS

@app.callback(
    Output('matrix-container', 'children'),
    [
    Input({'type': 'players', 'index': ALL}, 'value')]
)
def todo (val):
    for i in val:
        i=int(i)
    val = [2 if None else c for c in val]
    val=np.array(val)
    testplayer=[]
    testplayer2=[]
    for i in range(0,len(val)):
        testplayer.append("p"+str(i+1))
        testplayer2.append("p"+str(i+1))
    for i in range(0,len(val)):
        testplayer.append("p"+str(i+1)+"G")
    combplayer=[]
    for i in range(int(np.prod(val))):
        combplayer.append(convert(i,val))    
    cols = [{
            "id" : i,
            "name" : i,
            "type": "text",
            "renamable" : True,
            } for i in testplayer]
    return dash_table.DataTable(
        style_header={'backgroundColor': '#2bb1d2',
                      'position': '-webkit-sticky',
                      'position': 'sticky',
                      'top': '0',
                      'color': 'white',
                      'padding': '5px',
                      'font-size': '10px',
                      'text-align': 'center'},
        style_cell={
            'backgroundColor': '#FFFFF',
            'color': '#00000',
            'padding': '5px',
            'font-size': '10px',
            'text-align': 'center'
        },
        style_as_list_view=True,
        id='playerGains',
         fixed_rows={'headers': True},
         page_size=100,
         style_table={'height': '300px', 'overflowY': 'auto'},
        columns=cols,
        data = [{testplayer2[i] : j[i] for i in range(len(testplayer2))} for j in combplayer],
        editable = True)



@app.callback(
Output("final-result", 'children'),
[Input('playerGains', 'data'),Input({'type': 'players', 'index': ALL}, 'value')],)
def foo(data,p):
    playerGains=[]
    for i in data:
        gg=[]
        for j in i.values():
            gg.append(int(j))
        gg=np.array(gg)
        playerGains.append(gg)
    playerGains=np.array(playerGains)

    try:
        playerGains=np.delete(playerGains,np.arange(len(p)),axis=1)
        playerGainsReshaped=convertnewstruct(playerGains,p[0],p[1])
        x=NashEquil(playerGainsReshaped,p[0],p[1])
        final=""
        for i in x :
            st=converttostr(i,"")
            final=final+"["+st+"]"+"\n"
        return html.Div([
                            html.H3("Results :",style={'color':'#2bb1d2'}),
                            html.Div(children=[
                                html.Div([
                                    html.Div([
                                         html.Div([
                                            html.H3("Nash equilibrium in mixed strategy (Support Enumeration) :",style={'color':'#2bb1d2'},className="card-title"),
                                            html.H3([final],style={'text-align':'center'})],className="card-category"),
                                        ],className="card card-stats shadow p-4 mb-4")
                                ],className="col-sm-6"),
                                html.Div([
                                    html.Div([
                                         html.Div([
                                            html.H3("Game value in Pure strategy : ",style={'color':'#2bb1d2'},className="card-title"),
                                            html.H3([str(pureValue(playerGainsReshaped))],style={'text-align':'center'})],className="card-category"),
                                         ],className="card card-stats shadow p-4 mb-4")
                                ],className="col-sm-6"),
                            ],className="row ")],className=" shadow p-4 mb-4 ")
    except :
        pass

if __name__ == '__main__':
    app.run_server(debug=False,dev_tools_ui=False,dev_tools_props_check=False)