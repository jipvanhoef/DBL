from web_project.settings import BASE_DIR
from pathlib import Path

from main.models import user_id, Data_set

import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np  # importing numpy and
import pandas as pd  # importing pandas
import plotly.express as px
import plotly.graph_objects as go

import plotly.graph_objects as go
import plotly.io as pio

from plotly.offline import iplot
from plotly.graph_objs import *

from random import randint

import networkx as nx
import numpy as np  # importing numpy and
import pandas as pd  # importing pandas


import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors
import seaborn as sns  # also improves the look of plots
from django_plotly_dash import DjangoDash

def build_graph():
    # search for the correct file in the database by the userid
    try:
    # set the path to the uploaded database of this user
        data_set = Data_set.objects.get(user_id=user_id)
        path = data_set.file
    except:
    # set the path to our default database
        path = Path.joinpath(BASE_DIR, "data_set/enron-v1.csv")

    app = DjangoDash("network_graph")

    styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
            }   
        }

    sns.set()  # set Seaborn defaults
    plt.rcParams['figure.figsize'] = [15, 20]  # default hor./vert. size of plots, in inches
    plt.rcParams['lines.markeredgewidth'] = 1  # to fix issue with seaborn box plots; needed after import seaborn

    df_enron = pd.read_csv(path, parse_dates=['date']) #reading the enron csv and storing it as dataframe

    #get a list of all the years in the dataset
    df_enron['year'] = pd.DatetimeIndex(df_enron['date']).year
    years= list(df_enron['year'].unique())
    list.sort(years)
    #make a new dataframe that counts all the mails that are sent from one person to another per year year
    df = df_enron.groupby(['year', 'fromId','toId', 'fromJobtitle', 'toJobtitle', 'fromEmail', 'toEmail' ]).agg({'toId':['count']})
    df.columns=['amount']
    df= df.reset_index()
    df=df.sort_values(by=['year'])

    df_enron_sorted = df_enron.sort_values(by='date') #making a sorted dataframe by sorting on the date

#make 2 dataframes, one with all the mails that everyone received per day, and one with all the mails that everyone sent per day + the sentiment of those mails
    df_time_from = df_enron_sorted.groupby(['date', 'fromEmail' ]).agg({'sentiment':['mean'], 'fromEmail': [ 'count'],}).reset_index() #making a grouping object to group by date
    df_time_from.columns =['date', 'fromEmail', 'sentiment', 'fromEmailCount']
    df_time_to = df_enron_sorted.groupby(['date', 'toEmail' ]).agg({'toEmail': [ 'count'],}).reset_index() #making a grouping object to group by date
    df_time_to.columns =['date', 'toEmail','toEmailCount']


    #make a dataframe with all the from email adresses
    df_enron_from = df_enron.groupby('fromId').agg({'sentiment':['mean'], 'fromJobtitle': ['min'], 'fromEmail':['min']}).reset_index()
    df_enron_from.columns=['ID', 'mean sentiment', 'Jobtitle', 'fromEmail']
    #make a dataframe with all the to email adresses
    df_enron_to = df_enron.groupby('toId').agg({'sentiment':['mean'], 'toJobtitle': ['min'], 'toEmail':['min']}).reset_index()
    df_enron_to.columns=['ID', 'mean sentiment', 'Jobtitle', 'fromEmail']
#join to and from dataframes to make sure everyone is in the df ( if there is anyone that only sent or only received a mail they are still in here)
    df_enron_tot = df_enron_from.combine_first(df_enron_to)


    mailsenders = list(df["fromId"].unique()) #define the senders and receivers as nodes
    mailreceivers = list(df["toId"].unique())
    jobtitles = list(df['fromJobtitle'].unique()) #list of all the job titles
    jobtitlesindex = jobtitles.copy()
    node_list = list(set(mailsenders+mailreceivers)) #list of everything that needs to be a node
    G = nx.MultiGraph() #defining the graph

    jobtitlescount = len(jobtitles) #amount of functions in the company
    yearscount = len(years)#amount of years that mail are sent
    yearsstring = [str(i) for i in years]
    #make color lists for years and jobs
    jobcolor = ['#377eb8', '#ff7f00', '#4daf4a',
                '#f781bf', '#a65628', '#984ea3',
                '#99    9999', '#e41a1c', '#dede00',
                '#67001f', '#b2182b', '#d6604d',
                '#f4a582', '#fddbc7', '#f7f7f7',
                '#d1    e5f0', '#92c5de', '#4393c3',
                '#2166ac', '#053061']
    
    for i in node_list:
        G.add_node(i) #adding every node to the graph     
    for i in mailreceivers:
        G.nodes[i]['Title'] = df_enron_tot['Jobtitle'].loc[i-1]
        G.nodes[i]['mail'] = df_enron_tot['fromEmail'].loc[i-1]
        G.nodes[i]['sentiment'] = df_enron_tot['mean sentiment'].loc[i-1]

    for i,j in df.iterrows(): #adding the edges
        G.add_edges_from([(j["fromId"],j["toId"], {"year": df['year'].loc[i]})])
    #assigning a position to each node for plotting
    pos = nx.fruchterman_reingold_layout(G, k =1)

    # grouping the different job titles and putting them in clusters with a different starting point
    angs = np.linspace(0, 2*np.pi, 1+len(jobtitles))
    repos = []
    rad = 3.5     # radius of circle
    for ea in angs:
        if ea > 0:
            repos.append(np.array([rad*np.cos(ea), rad*np.sin(ea)]))
    for n, p in pos.items():
        posx = 0
        G.nodes[n]['pos'] = p
        for r in range(jobtitlescount):
            if G.nodes[n]['Title'] ==jobtitles[r]:
                posx = r

        else:
            pass
        G.nodes[n]['pos'] += repos[posx]

    #make the graph framework with layout settings
    fig = go.Figure(layout=go.Layout(
                    title="network graph of all email data of enron per year <br>year visible: "+years[0].astype(str),
                    titlefont=dict(size=16),
                    showlegend=True,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                    text="",
                    showarrow=False,
                    xref="paper", yref="paper") ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    #add all the traces for every year
    for i in range(yearscount):
        fig.add_trace(
            go.Scatter(
                x=[],
                y=[],
                text=[],
                visible = False,
                name = years[i].astype(str),
                line=dict(width=0.5, color = '#888'),
                hoverinfo='none',
                mode='lines'))

    #add all the traces for every job title
    for i in range(jobtitlescount):
        fig.add_trace(
            go.Scatter(
                x=[],
                y=[],
                visible = True,
                text=[],
                name = jobtitles[i],
                customdata = [],
                mode='markers',
                hoverinfo='text',
                marker=dict(
                    color=[],
                    size=15,
                    line=dict(width=0))))

    test = 0
    #make a matrix with figure data per year
    testlistx = [[] for _ in range(len(years))] 
    testlisty = [[] for _ in range(len(years))] 
    #add the mails as connections to the trace with the corresponding year   

    for edge in G.edges(keys=True):
        year = years.index(G.edges[edge]['year'])
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        testlistx[year]+= tuple([x0, x1, None])
        testlisty[year]+=tuple([y0, y1, None])

    for year in range(len(years)):
            fig.data[year]['x'] += tuple(testlistx[year])
            fig.data[year]['y'] += tuple(testlisty[year])
    fig.data[0].visible = True
    #add every person as a node to the trace with the corresponding job title
    for i in range(jobtitlescount):
        inew = i + yearscount
        if fig.data[inew]['name']==jobtitles[i]:
            for node in G.nodes():
                if G.nodes[node]['Title'] == jobtitles[i]:
                    x, y = G.nodes[node]['pos']
                    fig.data[inew]['x'] += tuple([x])
                    fig.data[inew]['y'] += tuple([y]) 
                    fig.data[inew]['marker']['color']+= tuple([jobcolor[i]])
            for node, adjacencies in enumerate(G.adjacency()):
                if G.nodes[node+1]['Title'] == jobtitles[i]:
                    node_info =G.nodes[node+1]['mail']#DE .astype(str) IS TOEGEVOEGD
                    fig.data[inew]['text']+=tuple([node_info])
                    node_info =''

    # Create and add slider
    mailyears = []
    jobs = []
    total = []
    for i in range(yearscount):
        year = dict(
            method="update",
            args=[{"visible": [False] * yearscount + [True]*jobtitlescount},
                {"title": "network graph of all email data of enron per year <br>year visible: " + years[i].astype(str)}],
            label = yearsstring[i], # layout attribute
        )
        year["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
        mailyears.append(year)

    sliders = [dict(
        active=0,
        currentvalue={"prefix": "year: "},
        pad={"t": 50},
        steps=mailyears,
    )]

    fig.update_layout(
        sliders=sliders
    )
    first_person = df_enron['fromEmail'].iloc[0]
    app.layout = html.Div([
        html.Div([
            dcc.Graph(
            id='network-graph',
            figure=fig,
            clickData={'points': [{'text': first_person}]}
            )
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20', 'top':'50%',  '-ms-transform': 'translateY(-50%)', 'transform':' translateY(-50%)'}),
        html.Div([
            dcc.Graph(id='sentiment-time-series'),
            dcc.Graph(id='mail-time-series'),

        ], style={'display': 'inline-block', 'width': '49%'})
    ], style={'border': '5px solid #6D8890'})
    def create_time_series(dffto, dfffrom, title, y_axis1, y_axis2):
        fig = go.Figure(layout=go.Layout(
                        title= title,
                        titlefont=dict(size=16),
                        showlegend=True,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        annotations=[ dict(
                        text="",
                        showarrow=False,
                        xref="paper", yref="paper") ],
                        xaxis=dict(showgrid=True, zeroline=True, showticklabels=True),
                        yaxis=dict(showgrid=True, zeroline=True, showticklabels=True)))

        fig.add_trace(  
        go.Scatter(
            x=dffto['date'],
            y=dffto[y_axis1],
            text=[],
            visible = True,
            name = 'incoming mails',
            line=dict(color = 'blue', width = 0.75),
            hoverinfo='none',
            mode='lines '))
        fig.add_trace(
        go.Scatter(
            x=dfffrom['date'],
            y=dfffrom[y_axis2],
            text=[],
            visible = True,
            name = 'outgoing mails',
            line=dict(color = 'orange', width = 0.75),
            hoverinfo='none',
            mode='lines'))

        return fig

    def create_sentiment_graph(dff_personal, dff_total, title, y_axis, min_date, max_date, min_sent, max_sent):
        fig = go.Figure(layout=go.Layout(
                    title= title,
                    titlefont=dict(size=16),
                    showlegend=True,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                    text="",
                    showarrow=False,
                    xref="paper", yref="paper") ],
                    xaxis=dict(showgrid=True, zeroline=True, showticklabels=True),
                    yaxis=dict(showgrid=True, zeroline=True, showticklabels=True)))

        fig.add_trace(  
        go.Scatter(
            x=dff_total['date'],
            y=dff_total[y_axis],
            visible = True,
            name = 'average sentiment over time of whole company',
            hoverinfo='none',
            fillcolor='grey',
            fill='tozeroy',
            mode='none'))
        fig.add_trace(
        go.Scatter(
            x=dff_personal['date'],
            y=dff_personal[y_axis],
            text=[],
            visible = True,
            name = 'average sentiment over time personal',
            line=dict(color = 'orange', width = 0.75),
            hoverinfo='none',
            mode='lines+markers'))
        fig.update_layout(xaxis_range=[min_date, max_date], yaxis_range=[min_sent, max_sent])
        return fig

    @app.callback(
        dash.dependencies.Output('sentiment-time-series', 'figure'),
        [dash.dependencies.Input('network-graph', 'clickData'),])

    def update_sentiment(clickData):
        email = clickData['points'][0]['text']
        dff = df_time_from[df_time_from['fromEmail'] == email]
        title = '<b>{}<br><b>{}'.format(email, 'average sentiment over time')
        y_axis = 'sentiment'
        min_date = dff['date'].min()
        max_date = dff['date'].max()
        min_sent = dff['sentiment'].min()-0.1
        max_sent = dff['sentiment'].max()+0.1

        return create_sentiment_graph(dff, df_time_from, title, y_axis, min_date, max_date, min_sent, max_sent)

    @app.callback(
        dash.dependencies.Output('mail-time-series', 'figure'),
        [dash.dependencies.Input('network-graph', 'clickData'),])

    def update_mails(clickData):
        email = clickData['points'][0]['text']
        dffto = df_time_to[df_time_to['toEmail'] == email]
        dfffrom = df_time_from[df_time_from['fromEmail'] == email]
        title = '<b>{}<br><b>{}'.format(email, 'amount of sent and received mails over time')
        y_axis1 = 'toEmailCount'
        y_axis2 = 'fromEmailCount'
        return create_time_series(dffto, dfffrom,title, y_axis1, y_axis2)
build_graph()