from django.shortcuts import render
from web_project.settings import BASE_DIR
from pathlib import Path

import numpy as np #importing numpy and 
import pandas as pd #importing pandas
import plotly.graph_objects as go
import plotly.express as px


import matplotlib as mpl
import matplotlib.pyplot as plt, mpld3 #importing the mpld3 library to make graphs interactive
import seaborn as sns  # also improves the look of plots
sns.set()  # set Seaborn defaults
plt.rcParams['figure.figsize'] = [10, 5]  # default hor./vert. size of plots, in inches
plt.rcParams['lines.markeredgewidth'] = 1  # to fix issue with seaborn box plots; needed after import seaborn


# hide FutureWarnings, which may show for Seaborn calls in most recent Anaconda
import warnings
warnings.filterwarnings("ignore", category=FutureWarning) 

from main.views import user_id
import os


#This function grabs the data set of the current user an craetes the visualization
def create_graph():
    #create the path for the folder where the user data set might be stored
    user_folder = Path.joinpath(BASE_DIR, "data_set/"+ user_id)

    #check if the user_folder exists
    if Path.exists(user_folder):
        #set the path of the csv file to the user folder + data_set.csv
        path = Path.joinpath(BASE_DIR, "data_set/"+ user_id + "/data_set.csv")
    else:
        #if the folder does not exist set the path to our default data set
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

#This function renders our html page for the visualizations
def visualization_view(request, *args, **kwargs):
    #convert the graph to a html displable graph with default width and heigth 
    fig = create_graph()
    graph = fig.to_html(full_html=False, default_height=500, default_width=700)
    #pass the graph as context to the html file
    context = {'graph': graph}
    #render the html file and load in the context
    return render(request, "visualizations.html", context)