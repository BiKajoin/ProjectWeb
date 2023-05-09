from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from pymongo import MongoClient
import pandas as pd

import plotly.graph_objects as go
from appData.models import fillBlankDate

# Create your views here.
def home(request):

    #connect to mongodb and retrieve data cursor
    client = MongoClient('mongodb+srv://pvcell:IXLCBUqW6U8FGUFr@cluster0.htuap5h.mongodb.net/userdatabase?retryWrites=true&w=majority')
    db = client['data']
    collection = db['homeMockup']

    # Retrieve data from collection
    dataframe = pd.DataFrame(list(collection.find({})))
    latestDate = dataframe['datetime'].max().strftime("%d/%m/%Y")
    # fill in missing dates
    dataframe = fillBlankDate(dataframe)

    # plot data with plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = dataframe['datetime'], y = dataframe['real'], name = 'Real Value'))
    fig.add_trace(go.Scatter(x = dataframe['datetime'], y = dataframe['predict'], name = 'Prediction Result'))
    fig.update_layout(
        autosize = True,
        margin = dict(l = 20, r = 20, b = 20, t = 20, pad = 4),
        xaxis_title = 'Datetime',
        yaxis_title = 'Power Generation (W)',
        font = dict(
            family = 'Noto San, monospace',
            size = 16,
            color = '#7f7f7f'
        ),
        legend = dict(
            yanchor = "top",
            y = 0.99,
            xanchor = "left",
            x = 0.01
        )
    )
    
    #convert plotly figure to html
    graph = fig.to_html(full_html = False)

    #render html
    return render(request, 'appGeneral/home.html', context = {'graph': graph, 'date': latestDate})

@login_required
def loggedin(request):
    return render(request, 'appGeneral/loggedin.html')

def loginp(request):
    if request.user.is_authenticated:
        return redirect('/loggedin')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)   

        user = authenticate(request, username=username, password=password)
        if user is None:
            print("error")
            context ={"error": "Invalid username or password"}
            return render(request, 'appGeneral/login.html', context)
        login(request, user)
        return redirect('/')
    return render(request, 'appGeneral/login.html',{})

@login_required
def logoutp(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    return render(request, 'appGeneral/logout.html',{})

def about(request):
    return render(request, 'appGeneral/about.html',{})

def handle404(request, exception):
    return render(request, '404.html')

    
