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
            self.strat.append(name+" Strategy "+str(i))

def index(tup,players):
    ''' tuple to int index'''
    result=0
    power=1
    a=tup[::-1]
    p=players.copy()
    p.reverse()
    for i in range(0,len(players)):
        result+=a[i]*power
        power=power*p[i].nstrat
    return result

def indexReverse(a,p):
    result=[]
    players=p.copy()
    players.reverse()
    for i in players:
        result.append((a%i.nstrat))
        a=(int)(a/i.nstrat)
    result.reverse()
    return tuple(result)


def buildKey(gains,Players):
    x=[]
    for i in range(0,len(gains)):
        x.append(indexReverse(i,Players))
    return np.array(x)

def iterativeElimination(gains,players,delete,strict):
    strr=[]
    for i in range(0,len(players)):
        gains,l=(domination(gains,players,i,delete,strict))
        if l!="":
            strr.append(l)
    return gains,strr

def domination(gains,allplayers,ind,delete,strict):
    """identifies strict domination , deletes the dominated from the gains table if delete = true. """
    dominationStr=""
    length=np.size(gains,axis=0)
    dom=[]
    tab=[]
    dominated=[]
    player=allplayers[ind]
    #Preprocessing
    for i in range(0,player.nstrat):
        tab.append([])
    for k in range(0,length):
        stratChoosen=(int)(indexReverse(k,allplayers)[ind])
        tab[stratChoosen].append(gains[k][ind])
    for i in range(0,len(tab)):
        for j in range(0,len(tab)):
            if (strict and i!= j and min(tab[i]) > max(tab[j]) or (not strict and i!= j and min(tab[i]) >= max(tab[j]))) :
                if strict :
                    dominationStr=html.Div([
                            html.Div([html.H4([player.strat[i]+" strictly dominates "+str(player.strat[j])],style={'color':'#088A08'})],className="card-category"),
                            ],className="card card-stats shadow p-4 mb-4")
                else:
                    dominationStr=html.Div([
                            html.Div([html.H4([player.strat[i]+" weakly dominates "+str(player.strat[j])],style={'color':'#ff0000'})],className="card-category"),
                            ],className="card card-stats shadow p-4 mb-4")
                if dominated.count(j)==0:
                    dominated.append(j)
    if delete :
        dominated.sort()
        dominated.reverse()
        dell=[]
        for i in range(0,length):
            if dominated.count(indexReverse(i,allplayers)[ind])>0:
                dell.append(i)
        dell.reverse()
        for i in dell:
            gains=np.delete(gains,i,axis=0)
    return gains,dominationStr

def extract(arrays,n):
    r=[]
    for i in range(int(len(arrays))):
        w=[]
        for j in range(len(arrays)):
            if all(arrays[i]==arrays[j]):
                 w.append(j)
        w=np.sort(w)
        r.append(w)
    r=np.unique(r,axis=0)
    return r




def bestPlay (gains,keys,players,ind):
    start=gains[:,ind]
    keys=np.delete(keys,ind,axis=1)
    index=extract(keys,players[ind].nstrat)
    result=[]
    for i in range(len(index)):
        x=np.argmax(start[index[i]])
        result.append(index[i][x])
    return(np.array(result))
 
    
def nashEquilibrium (gain,keys,players):
    x=[]
    for i in range(len(players)) :
        x.append(bestPlay(gain,keys,players,i))
    result=x[0]
    for i in x:
        result=np.intersect1d(result,i)
    return keys[result]
    
    
def paretoEfficiency(gains,players):
    result=[]
    for pareto in range(0,len(gains)):
        x=pareto
        add=True
        for i in range(0,len(gains)):
            if(all(gains[pareto]<=gains[i])and not all(gains[pareto]==gains[i])):
               add=False
               break
        if add:
            result.append(np.array(list(indexReverse(x,players))))
    result=np.unique(result,axis=0)
    pestrlist=' '.join([str(item) for item in result ])
    return pestrlist

def sec(gains,key,players,ind):
    lvl=[]
    for i in range(0,(players[ind].nstrat)):
        temp=[]
        rows0=np.where(key[:,ind]==i)[0]
        rows0=key[rows0]
        des=[]
        for i in rows0:
            des.append(index(i,players))
        for i in des :
            temp.append(gains[i,ind])
        lvl.append(min(temp))
    return max(lvl)

def security(gains,key,players):
    result=[]
    for i in range(0,len(players)):
        result.append(sec(gains,key,players,i))
    return np.array(result)
        

def TP1(gains,key,players,delete,strict):
    gainss,R4=(iterativeElimination(gains,players,delete,True))
    gainss,R5=(iterativeElimination(gains,players,delete,False))
    R1=(nashEquilibrium(gains,key,players))
    R2=(paretoEfficiency(gains,players))
    R3=(security(gains,key,players))
    return R1,R2,R3,R4,R5

def converttostr(input_seq, seperator):
   final_str = seperator.join(input_seq)
   return final_str


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
                children=[html.H3(children='TP1 : Game theory',
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
    html.Div([
            html.Button("Add a new player", id="add", n_clicks=0),
            html.Div(id='container', children=[])
        ],className="shadow p-4 mb-4"),
    html.Div(id='dropdown-container-output'),
    html.Br(),
    html.Div(id="matrix-container",className="card shadow "),
    html.Div(id="final-result"),
    html.Br(),
    html.Footer([
                html.Div(['© USTHB, MIV 2019/2020'],className="copyright text-center")],className="footer")
],className="wrapper")


@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

def generate_control_id(value):
    return 'Player{}'.format(value)

@app.callback(
    Output('container', 'children'),
    [Input('add', 'n_clicks')],
    [State('container', 'children')])
def display_dropdowns(n_clicks, children):
    DYNAMIC_CONTROLS= dcc.Input(
        id={
                 'type': 'players',
                 'index': n_clicks,
            } ,
        placeholder=generate_control_id(n_clicks+1)+" strategies",
        type="number",
        value=2,
        min=2,
        max=10,
    )
    children.append(DYNAMIC_CONTROLS)
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
                      'font-size': '15px',
                      'text-align': 'center'},
	    style_cell={
	        'backgroundColor': '#FFFFF',
	        'color': '#00000',
	        'padding': '5px',
            'font-size': '15px',
            'text-align': 'center'
	    },
    	style_as_list_view=True,
        id='playerGains',
         fixed_rows={'headers': True},
         page_size=100,
        columns=cols,
        data = [{testplayer2[i] : j[i] for i in range(len(testplayer2))} for j in combplayer],
        editable = True)


@app.callback(
Output("final-result", 'children'),
[Input('playerGains', 'data'),Input({'type': 'players', 'index': ALL}, 'value')])
def foo(data,p):
    playerGains=[]
    for i in data:
        gg=[]
        for j in i.values():
            gg.append(int(j))
        gg=np.array(gg)
        playerGains.append(gg)
    playerGains=np.array(playerGains)
    Players=[]
    for i in range(len(p)):
        Players.append(Player("Player "+str(i),p[i]))
    key=buildKey(playerGains,Players)
    try :
        playerGains=np.delete(playerGains,np.arange(len(p)),axis=1)
        r1,r2,r3,r4,r5=TP1(playerGains,key,Players,True,True)
        nasheqstringList="No Nash equilibrium found"
        if (len(r1)>0):
            nasheqstringList = ' '.join([str(item) for item in r1 ])
        if (len(r3)>0):
            secstringList = ' '.join([str(item) for item in r3 ])
        return html.Div([
                html.H3("Results :",style={'color':'#2bb1d2'}),
                html.Div(children=[
                    html.Div([
                        html.Div([
                            html.Br(),
                            html.H3(nasheqstringList,style={'color':'#2bb1d2'},className="card-title"),
                            html.P("Nash Equilibrium : ",className="card-category"),
                            ],className=" card card-stats shadow p-4 mb-4"),
                        ],className="col-sm-3"),
                    html.Div([
                        html.Div([
                            html.Br(),
                            html.H3(r2,style={'color':'#2bb1d2'},className="card-title"),
                            html.P("Pareto's Optimum : ",className="card-category"),
                            ],className="card card-stats shadow p-4 mb-4"),
                        ],className="col-sm-4"),
                    html.Div([
                        html.Div([
                            html.Br(),
                            html.H3(secstringList,style={'color':'#2bb1d2'},className="card-title"),
                            html.P("Security level:",className="card-category"),
                            ],className="card card-stats shadow p-4 mb-4")
                        ],className="col-sm-4")
                    ],className="row"),
                html.Div(children=r4,className="col-sm-11"),
                html.Hr(),
                html.Div(children=r5,className="col-sm-11")
                ],className=" shadow p-4 mb-4 "),

                
                
    except :
        pass


if __name__ == '__main__':
    app.run_server(debug=False,dev_tools_ui=False,dev_tools_props_check=False)