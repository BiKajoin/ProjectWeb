from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from pymongo import MongoClient
import pandas as pd

import plotly.graph_objects as go

# Create your views here.
def home(request):

    #connect to mongodb and retrieve data cursor
    client = MongoClient('mongodb+srv://pvcell:IXLCBUqW6U8FGUFr@cluster0.htuap5h.mongodb.net/userdatabase?retryWrites=true&w=majority')
    db = client['data']
    collection = db['admin1:second_half']
    projection = {'datetime': 1, 'W': 1}
    cursor = collection.find({}, projection)

    #convert pymongo cursor to pandas dataframe
    df = pd.DataFrame(list(cursor))
    print(df.head())
    df['datetime'] = pd.to_datetime(df['datetime'])

    #fill in missing dates
    start_date = df['datetime'].iloc[0]
    end_date = df['datetime'].iloc[-1]
    date_range = pd.date_range(start = start_date, end = end_date, freq='1min')
    missing_dates = date_range[~date_range.isin(df['datetime'])]
    missing_rows = pd.DataFrame({'datetime': missing_dates, 'W': None})
    df = pd.concat([df, missing_rows]).sort_values('datetime')

    #plot data with plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['datetime'], y=df['W'], mode='lines', connectgaps = False))
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
    )
    
    #convert plotly figure to html
    graph = fig.to_html(full_html = False)

    #render html
    return render(request, 'appGeneral/home.html', context = {'graph': graph})

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
    
