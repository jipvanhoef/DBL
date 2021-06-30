from web_project.settings import BASE_DIR
from pathlib import Path

from data_visualization.models import user_id, Data_set

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
    df_time_from['year'] = pd.DatetimeIndex(df_time_from['date']).year

    df_time_to = df_enron_sorted.groupby(['date', 'toEmail' ]).agg({'toEmail': [ 'count'],}).reset_index() #making a grouping object to group by date
    df_time_to.columns =['date', 'toEmail','toEmailCount']
    df_time_to['year'] = pd.DatetimeIndex(df_time_to['date']).year

    #dataframe for the average sentiment per day of the whole company
    df_sent = df_enron_sorted.groupby(['date']).agg({'sentiment':['mean']}).reset_index() 
    df_sent.columns=['date', 'sentiment']
    df_sent['year'] = pd.DatetimeIndex(df_sent['date']).year

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
    network_fig = go.Figure(layout=go.Layout(
                    title= '<b>{}<br><b>'.format('Network Graph of all email data per Year'),
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
        network_fig.add_trace(
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
        network_fig.add_trace(
            go.Scatter(
                x=[],
                y=[],
                visible = True,
                text=[],
                hovertext=[],
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
            network_fig.data[year]['x'] += tuple(testlistx[year])
            network_fig.data[year]['y'] += tuple(testlisty[year])
    network_fig.data[0].visible = True
    #add every person as a node to the trace with the corresponding job title
    for i in range(jobtitlescount):
        inew = i + yearscount
        if network_fig.data[inew]['name']==jobtitles[i]:
            for node in G.nodes():
                if G.nodes[node]['Title'] == jobtitles[i]:
                    x, y = G.nodes[node]['pos']
                    network_fig.data[inew]['x'] += tuple([x])
                    network_fig.data[inew]['y'] += tuple([y]) 
                    network_fig.data[inew]['marker']['color']+= tuple([jobcolor[i]])
                    hover_node_info ='Mail: ' + G.nodes[node]['mail'] +'. Function: '+G.nodes[node]['Title']
                    network_fig.data[inew]['hovertext']+=tuple([hover_node_info])
                    mail_info = G.nodes[node]['mail']
                    network_fig.data[inew]['text']+=tuple([mail_info])
                    hover_node_info =''
                    mail_info=''

    first_person = df_enron['fromEmail'].iloc[0]
    #html layout for the 3 different graphs and the slider
    app.layout = html.Div([
        html.Div([
            dcc.Graph(
            id='network-graph',
            figure=network_fig,
            clickData={'points': [{'text': first_person}]}
            ),
            dcc.Slider(
            id='years-slider',
            min=years[0],
            max=years[yearscount-1],
            step=1,
            value=years[2],
        ),
        html.Div(id='slider-output-container')
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20', 'top':'50%',  '-ms-transform': 'translateY(-50%)', 'transform':' translateY(-50%)', 'text-align': 'center'}),
        html.Div([
            dcc.Graph(id='sentiment-time-series'),
            dcc.Graph(id='mail-time-series'),

        ], style={'display': 'inline-block', 'width': '49%'}),

    ], style={'border': '5px solid #6D8890'})
    #function that gets called when a node is clicked to create a new figure where all the mails that are sent and received by one person in one year are visualised
    def create_time_series(dffto, dfffrom, title, y_axis1, y_axis2):
        #make the figure with the default parameters
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
        #add a trace with all the mails received by that person
        fig.add_trace(
        go.Bar(
            x=dffto['date'],
            y=dffto[y_axis1],
            text=[],
            visible = True,
            marker_color = 'blue',
            name = 'incoming mails'))
        #add a trace with all the mails sent by that person
        fig.add_trace(
        go.Bar(
            x=dfffrom['date'],
            y=dfffrom[y_axis2],
            text=[],
            visible = True,
            marker_color = 'orange',
            name = 'outgoing mails'))
        #update layout to stack traces if there are values for the same day
        fig.update_layout(barmode='stack')
        return fig
    #function to create a graph with the sentiment of the mails sent by a person in one year
    def create_sentiment_graph(dff_personal, dff_total, title, y_axis, min_date, max_date, min_sent, max_sent):
        #create figure with default parameters
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
        #add bar graph trace for the average sentiment of the whole company
        fig.add_trace(
        go.Bar(
            x=dff_total['date'],
            y=dff_total[y_axis],
            visible = True,
            marker_color = 'grey',
            name = 'Company'))
        #add line trace for the sentiment of that specific person
        fig.add_trace(
        go.Scatter(
            x=dff_personal['date'],
            y=dff_personal[y_axis],
            text=[],
            visible = True,
            name = 'Personal',
            line=dict(color = 'orange', width = 0.75),
            mode='lines+markers'))
        fig.update_layout(xaxis_range=[min_date, max_date], yaxis_range=[min_sent, max_sent])
        return fig

    #function that gets called with an callback when a node is clicked, or when the active year is changed
    #function updates the sentiment graph to the correct person or the correct year
    @app.callback(
        dash.dependencies.Output('sentiment-time-series', 'figure'),
        [dash.dependencies.Input('network-graph', 'clickData'),
        dash.dependencies.Input('years-slider', 'value')])

    def update_sentiment(clickData, year):
        email = clickData['points'][0]['text']
        dff = df_time_from[(df_time_from['fromEmail'] == email) & (df_time_from['year']==year)]
        dfftot = df_sent[df_sent['year']==year]
        if dff.empty:
            title = '<b>{}<br>{}{}'.format('No outgoing mails available for this year!', 'Viewing: ', email)
        else:
            title = '<b>{}<b>{}<br></b>{}{}'.format('average sentiment of outgoing mails over time in the year ', year, 'Viewing: ', email)
        y_axis = 'sentiment'
        min_date = dff['date'].min()
        max_date = dff['date'].max()
        min_sent = dff['sentiment'].min()-0.1
        max_sent = dff['sentiment'].max()+0.1
        return create_sentiment_graph(dff, dfftot, title, y_axis, min_date, max_date, min_sent, max_sent)
    #function that gets called with an callback when a node is clicked, or when the active year is changed
    #function updates the sent-received graph to the correct person or the correct year
    @app.callback(
        dash.dependencies.Output('mail-time-series', 'figure'),
        [dash.dependencies.Input('network-graph', 'clickData'),
        dash.dependencies.Input('years-slider', 'value')])

    def update_mails(clickData, year):
        email = clickData['points'][0]['text']
        dffto = df_time_to[(df_time_to['toEmail'] == email) & (df_time_to['year']==year)]
        dfffrom = df_time_from[(df_time_from['fromEmail'] == email) & (df_time_from['year']==year)]
        if dfffrom.empty and dffto.empty:
            title = '<b>{}<br>{}{}'.format('No in or outgoing mails available for this year!', 'Viewing: ', email)
        else:
            title = '<b>{}<b>{}<br></b>{}{}'.format('Amount of sent and received mails over time in the year ', year, 'Viewing: ', email)
        y_axis1 = 'toEmailCount'
        y_axis2 = 'fromEmailCount'
        return create_time_series(dffto, dfffrom,title, y_axis1, y_axis2)
    #function that gets called with an callback when the active year is changed
    #function updates the text of the year visible
    @app.callback(
        dash.dependencies.Output('slider-output-container', 'children'),
        [dash.dependencies.Input('years-slider', 'value')])
    def update_output(value):
        return 'The year visible is: {}'.format(value)
    #function that gets called with an callback when the active year is changed
    #function updates the network graph to the correct year
    @app.callback(
        dash.dependencies.Output('network-graph', 'figure'),
        [dash.dependencies.Input('years-slider', 'value')])
    def update_network_fig(value):
        year_index = years.index(value)
        for i in range(yearscount):
            if i == year_index:
                network_fig.data[i].visible = True
            else:
                network_fig.data[i].visible = False
        return network_fig
build_graph()