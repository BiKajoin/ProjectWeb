from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django_tables2 import RequestConfig
from pymongo import MongoClient
from datetime import datetime, timedelta

import csv
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from io import BytesIO
import pandas as pd

from appData.models import PVCellData, PVCellTable

# Create your views here.
@login_required
def data(request):
    client = MongoClient('mongodb+srv://wannawanna:d1Dj8cOiWwUCIxQs@cluster0.htuap5h.mongodb.net/userdatabase?retryWrites=true&w=majority')
    db = client['data']
    userCollectionNames = request.GET.get('collectionName')

    # get a list of collection names in your database
    # get the selected collection name from the form submission
    if(userCollectionNames == None):
        userCollectionNames = [name for name in db.list_collection_names() if f"{request.user.username}:" in name]
        tempList = []
        for col in userCollectionNames:
            temp = col.split(':')[1]
            tempList.append(temp)
        userCollectionNames = sorted(tempList)
    
    userCollectionNames.append("Admin")
    # print(splited_collection_names)
    selected = request.GET.get('collection', 'Admin')
    if(selected != 'Admin'):
        collectionName = f"{request.user.username}:{selected}"
    else:
        collectionName = selected
    collection = db[collectionName]

    pageNumber = request.POST.get('page', 1)
    startdateString = request.GET.get('startdate', '')
    enddateString = request.GET.get('enddate', '')

    if (startdateString and enddateString):

        startdate = datetime.strptime(startdateString, '%Y-%m-%dT%H:%M')
        enddate = datetime.strptime(enddateString, '%Y-%m-%dT%H:%M')
        
        filteredData = collection.find({'datetime': {'$gte': startdate, '$lt': enddate}})
        print(filteredData)
        filteredDataList = list(filteredData)

        table = PVCellTable(filteredDataList)
        RequestConfig(request, paginate={'page': pageNumber, 'per_page': 20}).configure(table)

        # filtered_data_list = list(filtered_data)
        # try:
        #     filtered_paginator = Paginator(filtered_data_list, 20) # 20 items per page
        #     filtered_page_number = request.GET.get('page')
        #     #print("page is", filtered_page_number)
        #     filtered_page_data = filtered_paginator.get_page(filtered_page_number) 
        # except PageNotAnInteger:
        #      filtered_page_data = filtered_paginator.page(1)
        # except EmptyPage:
        #     filtered_page_data = filtered_paginator.page(filtered_paginator.num_pages)
        context = {
            'PVCellTable': table,
            'startdate': startdateString,
            'enddate': enddateString,
            'collectionNames': userCollectionNames,
            'collection': selected,
        }
    else: 
        dataList = list(collection.find())

        table = PVCellTable(dataList)
        RequestConfig(request, paginate={'page': pageNumber, 'per_page': 20}).configure(table)
        # data = collection.find()
        # data_list = list(data)
        # try:
        #     paginator = Paginator(data_list, 20) # 20 items per page
        #     page_number = request.GET.get('page')
        #     page_data = paginator.get_page(page_number) 
        # except PageNotAnInteger:
        #     page_data = paginator.page(1)
        # except EmptyPage:
        #     page_data = paginator.page(paginator.num_pages)
        context = {
            'PVCellTable': table,
            'isFiltered': 'false',
            'collectionNames': userCollectionNames,
            'collection': selected,
        }
    
    print(context)
    return render(request, 'appData/data.html', context)

def drop_collection(request):
    if request.method == 'POST':
        print("yippee")
        collection_name = request.POST.get('delete_data')
        target=f"{request.user.username}:{collection_name}"
        if(collection_name=="Admin"):
            messages.success(request, 'You cannot drop Admin collection!')
            return redirect('data')
        client = MongoClient('mongodb+srv://wannawanna:d1Dj8cOiWwUCIxQs@cluster0.htuap5h.mongodb.net/userdatabase?retryWrites=true&w=majority')
        db = client['data']
        db.drop_collection(target)
        messages.success(request, 'Collection dropped!')
        return redirect('data')
    else:
        return redirect('data')

@login_required
def upload(request):
    if request.method == 'POST' and request.FILES['csv_file'] and request.POST.get('name'):
        try:
            csvFile = request.FILES['csv_file']
            fileBytes = BytesIO(csvFile.read())
            df = pd.read_csv(fileBytes)
            # Connect to the MongoDB server
            client = MongoClient('mongodb+srv://wannawanna:d1Dj8cOiWwUCIxQs@cluster0.htuap5h.mongodb.net/userdatabase?retryWrites=true&w=majority')
            db = client['data']
            # Check if DataFrame contains the correct fields in the correct order
            expected_fields = ['datetime', 'year', 'month', 'day', 'hour', 'minute', 'second', 'Irradiance', 'Tm', 'Vdc', 'Idc', 'kWdc', 'kWhdc','Iac', 'Vln', 'VA', 'W', 'Var', 'pf','Hz', 'VAh', 'Whac', 'cloud_cover']
            print(set(df.columns))
            print(set(expected_fields))
            if set(df.columns) != set(expected_fields):
                print('Incorrect fields')
                return redirect('fail')
            df['datetime'] = pd.to_datetime(df['datetime'])
        except:
            print('Error uploading file')
            return redirect('fail')
        
        # Convert the DataFrame to a list of dictionaries
        data = df.to_dict('records')
        username = request.user.username
        try:
            collection_name = request.POST.get('name')
            print(collection_name)
            if not collection_name in db.list_collection_names():
                collection_name = f"{username}:{collection_name}"
                collection = db.create_collection(collection_name)
                collection.insert_many(data)
            else:
                print('Collection name already exists')
                return redirect('fail')

            #return render(request, 'appData/success.html')
            return redirect('success')
        except:
            print('Error inserting data into MongoDB')  
            return redirect('appData/upload.html')
    return render(request, 'appData/upload.html')

@login_required
def success_page(request):
    return render(request, 'appData/success.html')

@login_required
def fail_page(request):
    return render(request, 'appData/fail.html')