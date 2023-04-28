from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from appData.models import PVCellData
from pymongo import MongoClient
from datetime import datetime
import itertools
import csv

# Create your views here.
@login_required
def data(request):
    client = MongoClient('mongodb+srv://wannawanna:d1Dj8cOiWwUCIxQs@cluster0.htuap5h.mongodb.net/userdatabase?retryWrites=true&w=majority')
    db = client['data']
    collection = db['admin-1']

    startdate = request.GET.get('startdate', '')
    enddate = request.GET.get('enddate', '')

    if (startdate and enddate):
        startdate = datetime.strptime(startdate, '%Y-%m-%d')
        startyear = startdate.year
        startmonth = startdate.month
        startday = startdate.day

        enddate = datetime.strptime(enddate, '%Y-%m-%d')
        endyear = enddate.year
        endmonth = enddate.month
        endday = enddate.day
    
        if(startyear==endyear and startmonth<endmonth):
            if endmonth - startmonth > 1:
                filtered_data = collection.find({'year': {'$eq': startyear}, 'month': {'$eq': startmonth}, 'day': {'$gte': startday}})
                for i in range(startmonth+1, endmonth):
                    filtered_data1 = collection.find({'year': {'$eq': startyear}, 'month': {'$eq': i}})
                    filtered_data = itertools.chain(filtered_data, filtered_data1)
                filtered_data1 = collection.find({'year': {'$eq': startyear}, 'month': {'$eq': endmonth}, 'day': {'$lte': endday}})
                filtered_data = itertools.chain(filtered_data, filtered_data1)
            """else: 
                filtered_data1 = collection.find({'year': {'$eq': startyear}, 'month': {'$eq': startmonth}, 'day': {'$gte': startday}})
                filtered_data2 = collection.find({'year': {'$eq': startyear}, 'month': {'$eq': endmonth}, 'day': {'$lte': endday}})
                filtered_data = itertools.chain(filtered_data1, filtered_data2)"""
        elif(startyear<endyear):
            if endyear - startyear > 1:
                print("hello1")
                filtered_data = collection.find({'year': {'$eq': startyear}, 'month': {'$eq': startmonth}, 'day': {'$gte': startday}})
                filtered_data1 = collection.find({'year': {'$eq': startyear}, 'month': {'$gte': startmonth}})
                filtered_data = itertools.chain(filtered_data, filtered_data1)
                for i in range(startyear+1, endyear):
                    filtered_data1 = collection.find({'year': {'$eq': i}})
                    filtered_data = itertools.chain(filtered_data, filtered_data1)
                filtered_data1 = collection.find({'year': {'$eq': endyear}, 'month': {'$lte': endmonth-1}})
                filtered_data = itertools.chain(filtered_data, filtered_data1)
                filtered_data1 = collection.find({'year': {'$eq': endyear}, 'month': {'$eq': endmonth}, 'day': {'$lte': endday}})
                filtered_data = itertools.chain(filtered_data, filtered_data1)
            """else: #good???
                print("hello2")
                filtered_data1 = collection.find({'year': {'$eq': startyear}, 'month': {'$gte': startmonth}})
                filtered_data2 = collection.find({'year': {'$eq': endyear}, 'month': {'$lte': endmonth-1}})
                filtered_data3 = collection.find({'year': {'$eq': endyear}, 'month': {'$lte': endmonth}, 'day': {'$lte': endday}})
                filtered_data = itertools.chain(filtered_data1, filtered_data2)
                filtered_data = itertools.chain(filtered_data, filtered_data3)"""
        else:
            filtered_data = collection.find({'year': {'$eq': startyear}, 'month': {'$eq': startmonth}, 'day': {'$gte': startday, '$lte': endday}})
        filtered_data_list = list(filtered_data)
        try:
            filtered_paginator = Paginator(filtered_data_list, 20) # 20 items per page
            filtered_page_number = request.GET.get('page')
            print("page is", filtered_page_number)
            filtered_page_data = filtered_paginator.get_page(filtered_page_number) 
        except PageNotAnInteger:
             filtered_page_data = filtered_paginator.page(1)
        except EmptyPage:
            filtered_page_data = filtered_paginator.page(filtered_paginator.num_pages)
        context = {
            'filtereddata': filtered_page_data,
            #'startdate': startdate,
            #'enddate': enddate,
            'startdateString': datetime.strftime(startdate, '%Y-%m-%d'),
            'enddateString': datetime.strftime(enddate, '%Y-%m-%d'),
        }
        return render(request, 'appData/filter.html', context) 
    else:
        data = collection.find()
        data_list = list(data)
        try:
            paginator = Paginator(data_list, 20) # 20 items per page
            page_number = request.GET.get('page')
            page_data = paginator.get_page(page_number) 
        except PageNotAnInteger:
             page_data = paginator.page(1)
        except EmptyPage:
            page_data = paginator.page(paginator.num_pages)
        context = {
            'data': page_data,
            'isFiltered': 'false',
        }
        return render(request, 'appData/data.html', context)   
     
@login_required
def upload(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        data = csv.reader(csv_file)
        client = MongoClient()
        db = client['userdatabase']
        """for row in data:
            # assume the CSV file has two columns: "name" and "age"
            name, age = row
            collection.insert_one({'name': name, 'age': age})
        return render(request, 'success.html')"""
    return render(request, 'appData/upload.html')