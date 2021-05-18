from django.shortcuts import render
from web_project.settings import BASE_DIR
from pathlib import Path

from main.models import user_id, Data_set

import os
import datetime
import sqlite3
import threading

import numpy as np #importing numpy 
import pandas as pd #importing pandas
import plotly.graph_objects as go
import plotly.io as pio

from plotly.offline import iplot
from plotly.graph_objs import *

from random import randint

import networkx as nx


import matplotlib as mpl
import matplotlib.pyplot as plt, mpld3 #importing the mpld3 library to make graphs interactive
import matplotlib.colors
import seaborn as sns  # also improves the look of plots
sns.set()  # set Seaborn defaults
plt.rcParams['figure.figsize'] = [10, 5]  # default hor./vert. size of plots, in inches
plt.rcParams['lines.markeredgewidth'] = 1  # to fix issue with seaborn box plots; needed after import seaborn


# hide FutureWarnings, which may show for Seaborn calls in most recent Anaconda
import warnings
warnings.filterwarnings("ignore", category=FutureWarning) 

#This function grabs the data set of the current user an creates the visualization
def create_line_graph():
    #Chechk if the user has uploaded a file by quering on the user_id and if a exception occurs set the path
    #to the default csv file
    try:
        path = Data_set.objects.get(user_id= user_id).data.path
    except:
        path = Path.joinpath(BASE_DIR, "data_set/enron-v1.csv")

    df_enron = pd.read_csv(path, parse_dates=['date']) #reading the enron csv and storing it as dataframe

    df_enron_sorted = df_enron.sort_values(by='date') #making a sorted dataframe by sorting on the date
    #df_enron_sorted.head() (disregard)

    grouped = df_enron_sorted.groupby('date') #making a grouping object to group by date

    df_average_sentiment = grouped[['sentiment']].mean() #making a new df where the average sentiment per day is stored

    df_average_sentiment.head() 

    fig = go.Figure() #defining a figure

    fig.add_trace(
        go.Scatter(x=list(df_average_sentiment.index), y=list(df_average_sentiment['sentiment']))) #adding the data to the figure

    # Set title
    fig.update_layout(
        title_text="Average sentiment per day across all Enron emails (with interactive timeline)"
    )

    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
        type="date"
        )
    )
    return fig
def create_network_graph():
    #Chechk if the user has uploaded a file by quering on the user_id and if a exception occurs set the path
    #to the default csv file
    try:
        path = Data_set.objects.get(user_id= user_id).data.path
    except:
        path = Path.joinpath(BASE_DIR, "data_set/enron-v1.csv")

    df_enron = pd.read_csv(path, parse_dates=['date']) #reading the enron csv and storing it as dataframe
    #get a list of all the years in the dataset
    df_enron['year'] = pd.DatetimeIndex(df_enron['date']).year
    years= list(df_enron['year'].unique())
    list.sort(years)

    #make a new dataframe that counts all the mails that are sent from one person to another in one year
    df_enron_test = df_enron.groupby(['year', 'fromId','toId', 'fromJobtitle', 'toJobtitle', 'fromEmail'])['toId'].nunique()
    df =df_enron_test.to_frame()
    df.columns=['amount']
    df= df.reset_index()
    df=df.sort_values(by=['year','fromId'])

    #make a new df from where all the nodes are made from
    df_enron_to = df_enron.groupby('toId').agg({'sentiment':['mean'], 'toJobtitle': ['min'], 'fromEmail':['min']}).reset_index()
    df_enron_to.columns=['ID', 'mean sentiment', 'Jobtitle', 'fromEmail']
    
    #define the senders and receivers as nodes
    mailsenders = list(df["fromId"].unique()) 
    mailreceivers = list(df["toId"].unique())
    jobtitles = list(df['fromJobtitle'].unique()) #list of all the job titles
    node_list = list(set(mailsenders+mailreceivers)) #list of everything that needs to be a node
    G = nx.MultiGraph() #defining the graph

    jobtitlescount = len(jobtitles) #amount of functions in the company
    yearscount = len(years)#amount of years that mail are sent
    yearsstring = [str(i) for i in years]

    #make color lists for years and jobs
    jobcolor = []
    for i in range(jobtitlescount):
        jobcolor.append('#%06X' % randint(0, 0xFFFFFF))
    yearcolor = []
    for i in range(yearscount):
        jobcolor.append('#%06X' % randint(0, 0xFFFFFF))
        
    for i in node_list:
        G.add_node(i) #adding every node to the graph 
        #G.nodes[i]['Title'] = df_enron_from['fromJobtitle'].loc[i]
        
    for i in mailreceivers:
        G.nodes[i]['Title'] = df_enron_to['Jobtitle'].loc[i-1]
        G.nodes[i]['mail'] = df_enron_to['fromEmail'].loc[i-1]

        G.nodes[i]['sentiment'] = df_enron_to['mean sentiment'].loc[i-1]
        
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
                    text="No. of connections",
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
                mode='markers',
                hoverinfo='text',
                marker=dict(
                    color=[],
                    size=15,
                    line=dict(width=0))))
    test = 0
    #add the mails as connections to the trace with the corresponding year   
    for edge in G.edges(keys=True):
        year = years.index(G.edges[edge]['year'])
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        fig.data[year]['x'] += tuple([x0, x1, None])
        fig.data[year]['y'] += tuple([y0, y1, None])

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
                    node_info = G.nodes[node+1]['Title']+', ID: '+adjacencies[0].astype(str) + ', mail: ' + G.nodes[node+1]['mail']#DE .astype(str) IS TOEGEVOEGD
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

    return fig

#This function renders our html page for the visualizations
def visualization_view(request, *args, **kwargs):
    #convert the graph to a html displable graph with default width and heigth 
    fig = threading.Thread(target =create_network_graph).start()
    line_fig = create_line_graph()
    line_graph = line_fig.to_html(full_html=False, default_height=500, default_width=700)
    #convert the network graph to html
    network_fig = fig
    network_graph = network_fig.to_html(full_html= False, default_height=500, default_width=700)
    #pass the graph as context to the html file
    context = {'line_graph': line_graph, 'network_graph': network_graph}
    #render the html file and load in the context
    return render(request, "visualizations.html", context)