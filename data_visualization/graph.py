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
# default hor./vert. size of plots, in inches
    plt.rcParams['figure.figsize'] = [15, 20]
# to fix issue with seaborn box plots; needed after import seaborn
    plt.rcParams['lines.markeredgewidth'] = 1

# reading the enron csv and storing it as dataframe
    df_enron = pd.read_csv(path, parse_dates=['date'])

# get a list of all the years in the dataset
    df_enron['year'] = pd.DatetimeIndex(df_enron['date']).year
    years = list(df_enron['year'].unique())
    list.sort(years)
# make a new dataframe that counts all the mails that are sent from one person to another per year year
    df = df_enron.groupby(['year', 'fromId', 'toId', 'fromJobtitle',
                       'toJobtitle', 'fromEmail', 'toEmail']).agg({'toId': ['count']})
    df.columns = ['amount']
    df = df.reset_index()
    df = df.sort_values(by=['year', 'fromId'])

# making a sorted dataframe by sorting on the date
    df_enron_sorted = df_enron.sort_values(by='date')

    df_time = df_enron_sorted.groupby(['date', 'fromEmail']).agg({'sentiment': ['mean'], 'fromEmail': [
    'count']}).reset_index()  # making a grouping object to group by date
    df_time.columns = ['date', 'fromEmail', 'sentiment', 'fromEmailCount']
# make a dataframe with all the from email adresses
    df_enron_from = df_enron.groupby('fromId').agg(
    {'sentiment': ['mean'], 'fromJobtitle': ['min'], 'fromEmail': ['min']}).reset_index()
    df_enron_from.columns = ['ID', 'mean sentiment', 'Jobtitle', 'fromEmail']
# make a dataframe with all the to email adresses
    df_enron_to = df_enron.groupby('toId').agg(
    {'sentiment': ['mean'], 'toJobtitle': ['min'], 'toEmail': ['min']}).reset_index()
    df_enron_to.columns = ['ID', 'mean sentiment', 'Jobtitle', 'fromEmail']
# join to and from dataframes to make sure everyone is in the df ( if there is anyone that only sent or only received a mail they are still in here)
    df_enron_tot = df_enron_from.combine_first(df_enron_to)

# define the senders and receivers as nodes
    mailsenders = list(df["fromId"].unique())
    mailreceivers = list(df["toId"].unique())
    jobtitles = list(df['fromJobtitle'].unique())  # list of all the job titles
    jobtitlesindex = jobtitles.copy()
# list of everything that needs to be a node
    node_list = list(set(mailsenders+mailreceivers))
    G = nx.MultiGraph()  # defining the graph

    jobtitlescount = len(jobtitles)  # amount of functions in the company
    yearscount = len(years)  # amount of years that mail are sent
    yearsstring = [str(i) for i in years]
# make color lists for years and jobs
    jobcolor = ['#377eb8', '#ff7f00', '#4daf4a',
            '#f781bf', '#a65628', '#984ea3',
            '#999999', '#e41a1c', '#dede00',
            '#67001f', '#b2182b', '#d6604d',
            '#f4a582', '#fddbc7', '#f7f7f7',
            '#d1e5f0', '#92c5de', '#4393c3',
            '#2166ac', '#053061']

    for i in node_list:
        G.add_node(i)  # adding every node to the graph
    for i in mailreceivers:
        G.nodes[i]['Title'] = df_enron_tot['Jobtitle'].loc[i-1]
        G.nodes[i]['mail'] = df_enron_tot['fromEmail'].loc[i-1]
        G.nodes[i]['sentiment'] = df_enron_tot['mean sentiment'].loc[i-1]

    for i, j in df.iterrows():  # adding the edges
        G.add_edges_from(
        [(j["fromId"], j["toId"], {"year": df['year'].loc[i]})])

# assigning a position to each node for plotting
    pos = nx.fruchterman_reingold_layout(G, k=1)

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
            if G.nodes[n]['Title'] == jobtitles[r]:
                posx = r

        else:
            pass
        G.nodes[n]['pos'] += repos[posx]

# make the graph framework with layout settings
    fig = go.Figure(layout=go.Layout(
    title="Network graph of all email data in the year " +
    years[0].astype(str),
    titlefont=dict(size=18),
    showlegend=True,
    hovermode='closest',
    margin=dict(b=20, l=5, r=5, t=40),
    annotations=[dict(
        text="",
        showarrow=False,
        xref="paper", yref="paper")],
    xaxis=dict(showgrid=False, zeroline=False,
               showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

# add all the traces for every year
    for i in range(yearscount):
        fig.add_trace(
        go.Scatter(
            x=[],
            y=[],
            text=[],
            visible=False,
            name=years[i].astype(str),
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines'))

# add all the traces for every job title
    for i in range(jobtitlescount):
        fig.add_trace(
        go.Scatter(
            x=[],
            y=[],
            visible=True,
            text=[],
            name=jobtitles[i],
            customdata=[],
            mode='markers',
            hoverinfo='text',
            marker=dict(
                color=[],
                size=15,
                line=dict(width=0))))

    test = 0
# make a matrix with figure data per year
    testlistx = [[] for _ in range(len(years))]
    testlisty = [[] for _ in range(len(years))]
# add the mails as connections to the trace with the corresponding year

    for edge in G.edges(keys=True):
        year = years.index(G.edges[edge]['year'])
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        testlistx[year] += tuple([x0, x1, None])
        testlisty[year] += tuple([y0, y1, None])

    for year in range(len(years)):
        fig.data[year]['x'] += tuple(testlistx[year])
        fig.data[year]['y'] += tuple(testlisty[year])
    fig.data[0].visible = True
# add every person as a node to the trace with the corresponding job title
    for i in range(jobtitlescount):
        inew = i + yearscount
        if fig.data[inew]['name'] == jobtitles[i]:
            for node in G.nodes():
                if G.nodes[node]['Title'] == jobtitles[i]:
                    x, y = G.nodes[node]['pos']
                    fig.data[inew]['x'] += tuple([x])
                    fig.data[inew]['y'] += tuple([y])
                    fig.data[inew]['marker']['color'] += tuple([jobcolor[i]])
            for node, adjacencies in enumerate(G.adjacency()):
                if G.nodes[node+1]['Title'] == jobtitles[i]:
                # DE .astype(str) IS TOEGEVOEGD
                    node_info = G.nodes[node+1]['mail']
                    fig.data[inew]['text'] += tuple([node_info])
                    node_info = ''

# Create and add slider
    mailyears = []
    jobs = []
    total = []
    for i in range(yearscount):
        year = dict(
        method="update",
        args=[{"visible": [False] * yearscount + [True]*jobtitlescount},
              {"title": "Network graph of all email data in the year " + years[i].astype(str)}],
        label=yearsstring[i],  # layout attribute
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
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='sentiment-time-series'),
        dcc.Graph(id='mail-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'})
])


    def create_time_series(dff, title, y_axis):
        fig = px.scatter(dff, x='date', y=y_axis)

        fig.update_traces(mode='lines+markers')
        fig.update_xaxes(showgrid=False)

        fig.update_yaxes(type='linear')

        fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)

        fig.update_layout(height=225, margin={
        'l': 20, 'b': 30, 'r': 10, 't': 10})

        return fig


    @app.callback(
    dash.dependencies.Output('sentiment-time-series', 'figure'),
    [dash.dependencies.Input('network-graph', 'clickData'), ])
    def update_sentiment(clickData):
        email = clickData['points'][0]['text']
        dff = df_time[df_time['fromEmail'] == email]
        title = '<b>{}<br><b>{}'.format(email, 'Average Sentiment over time')
        y_axis = 'sentiment'
        return create_time_series(dff, title, y_axis)


    @app.callback(
    dash.dependencies.Output('mail-time-series', 'figure'),
    [dash.dependencies.Input('network-graph', 'clickData'), ])
    def update_mails(clickData):
        email = clickData['points'][0]['text']
        dff = df_time[df_time['fromEmail'] == email]
        title = '<b>{}<br><b>{}'.format(email, 'Amount of Mails sent over time')
        y_axis = 'fromEmailCount'
        return create_time_series(dff, title, y_axis)
build_graph()