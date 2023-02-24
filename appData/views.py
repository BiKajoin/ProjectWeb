from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from appData.models import PVCellData
from pymongo import MongoClient
from datetime import datetime

# Create your views here.
@login_required
def data(request):
     # Connect to MongoDB
    client = MongoClient('mongodb+srv://wannawanna:d1Dj8cOiWwUCIxQs@cluster0.htuap5h.mongodb.net/userdatabase?retryWrites=true&w=majority')
    db = client['userdatabase']
    collection = db['pvcelldata']

    # Retrieve data from MongoDB
    dt = collection.find().limit(20)
    #dt.aggregate([{ '$addField': { 'Date': { "$toDate": {"$dateToString":{"datetime":"$clusterTime"}} }, } }])
    dt = list(dt)
    for i in range(0,20):
        timestamp = datetime.fromtimestamp(dt[0]['datetime'].time)
        print(timestamp)
        #dt[i]['datetime'] = dt[i]['datetime']*1000

    # Pass data to template
    return render(request, 'appData/data.html', {'data': dt})

