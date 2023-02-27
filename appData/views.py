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

    startdate = request.GET.get('startdate', '')
    enddate = request.GET.get('enddate', '')

    if startdate and enddate:
        startdate = datetime.strptime(startdate, '%Y-%m-%d')
        startyear = startdate.year
        startmonth = startdate.month
        startday = startdate.day

        enddate = datetime.strptime(enddate, '%Y-%m-%d')
        endyear = enddate.year
        endmonth = enddate.month
        endday = enddate.day
        
        filtered_data = collection.find({'year': {'$gte': startyear, '$lte': endyear}, 'month': {'$gte': startmonth, '$lte': endmonth}, 'day': {'$gte': startday, '$lte': endday}})
        filtered_data_list = list(filtered_data)
        return render(request, 'appData/filter.html', {'data': filtered_data_list})
    else:
        data = collection.find().limit(20)
        data_list = list(data)
        return render(request, 'appData/data.html', {'data': data_list})


