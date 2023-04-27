from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from appData.models import PVCellData
from pymongo import MongoClient
from datetime import datetime, timedelta

import csv
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from io import BytesIO
import pandas as pd

# Create your views here.
@login_required
def data(request):
    client = MongoClient('mongodb+srv://wannawanna:d1Dj8cOiWwUCIxQs@cluster0.htuap5h.mongodb.net/userdatabase?retryWrites=true&w=majority')
    db = client['data']
    collection_names = db.list_collection_names()

    # get a list of collection names in your database
    # get the selected collection name from the form submission
    filtered_collection_names = [name for name in collection_names if f"{request.user.username}:" in name]
    splited_collection_names = []
    for col in filtered_collection_names:
        temp = col.split(':')[1]
        splited_collection_names.append(temp)
    
    splited_collection_names.append("Admin")
    splited_collection_names = sorted(splited_collection_names)
    print(splited_collection_names)
    selected = request.GET.get('collection', 'Admin')
    if(selected != 'Admin'):
        selected_collection = f"{request.user.username}:{selected}"
    else:
        selected_collection = selected
    #collection = db['admin-1']
    collection = db[selected_collection]
    print("selected:",selected_collection)
    
    startdate = request.GET.get('startdate', '')
    enddate = request.GET.get('enddate', '')

    if (startdate and enddate):

        startdate = datetime.strptime(startdate, '%Y-%m-%d')
        enddate = datetime.strptime(enddate, '%Y-%m-%d')

        enddateNew = enddate + timedelta(days=1)
        
        filtered_data = collection.find({'datetime': {'$gte': startdate, '$lte': enddateNew}})
        filtered_data_list = list(filtered_data)
        try:
            filtered_paginator = Paginator(filtered_data_list, 20) # 20 items per page
            filtered_page_number = request.GET.get('page')
            #print("page is", filtered_page_number)
            filtered_page_data = filtered_paginator.get_page(filtered_page_number) 
        except PageNotAnInteger:
             filtered_page_data = filtered_paginator.page(1)
        except EmptyPage:
            filtered_page_data = filtered_paginator.page(filtered_paginator.num_pages)
        context = {
            'filtereddata': filtered_page_data,
            'startdateString': datetime.strftime(startdate, '%Y-%m-%d'),
            'enddateString': datetime.strftime(enddate, '%Y-%m-%d'),
            'collection_names': splited_collection_names,
            'selected_collection': selected, 
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
            'collection_names': splited_collection_names,
            'selected_collection': selected,
        }
        return render(request, 'appData/data.html', context)   

"""     
@login_required
def upload(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        data = csv.reader(csv_file)
        client = MongoClient()
        db = client['userdatabase']
            for row in data:
            # assume the CSV file has two columns: "name" and "age"
            name, age = row
            collection.insert_one({'name': name, 'age': age})
        return render(request, 'success.html')
    return render(request, 'appData/upload.html')
"""

@login_required
def upload(request):
    if request.method == 'POST' and request.FILES['csv_file'] and request.POST.get('name'):
        try:
            csv_file = request.FILES['csv_file']
            file_bytes = BytesIO(csv_file.read())
            df = pd.read_csv(file_bytes)
            df['datetime'] = pd.to_datetime(df['datetime'])
        except:
            print('Error uploading file')
            return redirect('fail')

        # Connect to the MongoDB server
        client = MongoClient('mongodb+srv://wannawanna:d1Dj8cOiWwUCIxQs@cluster0.htuap5h.mongodb.net/userdatabase?retryWrites=true&w=majority')
        #client = MongoClient('localhost', 27017)
        db = client['data']
        #collection = db['test']

        # Convert the DataFrame to a list of dictionaries
        data = df.to_dict('records')
        username = request.user.username
        try:
            """latest_collection = db["latestcollection"].find_one({"username": username})

            if latest_collection is None:
                # create a new collection for the user if no previous collection exists
                collection_num = 1
                collection_name = f"{username}:{collection_num}"
                collection = db.create_collection(collection_name)
                db["latestcollection"].insert_one({"username": username, "latest_collection": collection_name})
            else:
                # get the latest collection name for the user
                collection_name = latest_collection["latest_collection"]
                username, collection_num = collection_name.split(":")
                collection_num = int(collection_num)
                collection_num += 1
                collection_name = f"{username}:{collection_num}"
                collection = db.create_collection(collection_name)
                db["latestcollection"].update_one({"username": username}, {"$set": {"latest_collection": collection_name}})
            """
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