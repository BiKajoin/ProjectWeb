from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    print("start:",startdate,"end:", enddate)
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
        try:
            filtered_paginator = Paginator(filtered_data_list, 20) # 20 items per page
            filtered_page_number = request.GET.get('page')
            filtered_page_data = filtered_paginator.get_page(filtered_page_number) 
        except PageNotAnInteger:
             filtered_page_data = filtered_paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            filtered_page_data = filtered_paginator.page(filtered_paginator.num_pages)
        context = {
            'filteredData': filtered_page_data,
            'isFiltered': 'true',
            #'page_changed': filtered_page_number != request.GET.get('previous_page'),
            #'previous_page': request.GET.get('page'),
        }
        return render(request, 'appData/datatable.html', context) 
        #return render(request, 'appData/datatable.html', {'data': filtered_page_data})
    else:
        #data = collection.find().limit(20)
        data = collection.find()
        data_list = list(data)
        """paginator = Paginator(data_list, 20) # 20 items per page
        page_number = request.GET.get('page')
        page_data = paginator.get_page(page_number)"""
        try:
            paginator = Paginator(data_list, 20) # 20 items per page
            page_number = request.GET.get('page')
            page_data = paginator.get_page(page_number ) 
        except PageNotAnInteger:
             page_data = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            page_data = paginator.page(paginator.num_pages)
        context = {
            'data': page_data,
            'isFiltered': 'false',
            #'page_changed': page_number != request.GET.get('previous_page'),
            #'previous_page': request.GET.get('page'),
        }
        #if  page_number != request.GET.get('previous_page'):
        #    return render(request, 'appData/datatable.html', context)
        return render(request, 'appData/data.html', context)    
        #return render(request, 'appData/data.html', {'data': page_data})


