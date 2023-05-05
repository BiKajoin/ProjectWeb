from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from asgiref.sync import sync_to_async, async_to_sync

from django_tables2 import RequestConfig
import json
from google.protobuf.json_format import MessageToJson

import tensorflow as tf
import numpy as np
import pandas as pd
from pymongo import MongoClient
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objects as go

import grpc
from tensorflow_serving.apis import predict_pb2, prediction_service_pb2_grpc

from appData.models import PVCellTable

# Create your views here.


@login_required
def model(request):
    return render(request, 'appModel/model.html')

@login_required
def predict(request):
    client = MongoClient('mongodb+srv://wannawanna:d1Dj8cOiWwUCIxQs@cluster0.htuap5h.mongodb.net/userdatabase?retryWrites=true&w=majority')
    db = client['data']
    userCollectionNames = request.GET.get('collectionName')

    if(userCollectionNames == None):
        userCollectionNames = [name for name in db.list_collection_names() if f"{request.user.username}:" in name]
        tempList = []
        for col in userCollectionNames:
            temp = col.split(':')[1]
            tempList.append(temp)
        userCollectionNames = sorted(tempList)
    
    if request.method == 'GET':
        selected = request.GET.get('collection', userCollectionNames[0])

        if(request.GET.get('makePrediction') == 'True'):
            return async_to_sync(makePrediction)(request)
        
        collection = db[f"{request.user.username}:{selected}"]
        pageNumber = request.POST.get('page', 1)

        # convert cursor to list of dictionaries
        dataList = list(collection.find())
        
        table = PVCellTable(dataList)
        RequestConfig(request, paginate={'page': pageNumber, 'per_page': 20}).configure(table)

        context = {
            'PVCellTable': table,
            'collectionNames': userCollectionNames,
            'collection': selected,
            'page': pageNumber,
        }
        
    return render(request, 'appModel/predict.html', context)

@login_required
def result(request):
    graph = request.session.get('graph', None)
    request.session.pop('graph', None)
    print(graph)
    return render(request, 'appModel/result.html', context = {'graph': graph})

# to run tensorflow serving,  follow these steps
# 1. install docker desktop
# 2. in any terminal, run $docker pull tensorflow/serving
# 3. in tfserving directory terminal, run $docker run -p 8500:8500 -p 8501:8501 --mount type=bind,source=absolute\path\to\work\folder\Web\tfserving\models\LSTM6x64_cloud_cover,target=/models/LSTM6x64_cloud_cover  -e MODEL_NAME=LSTM6x64_cloud_cover -t tensorflow/serving
# for Wanna is $docker run -p 8500:8500 -p 8501:8501 --mount type=bind,source=C:\University\Year-4\Project\Python\Web\tfserving\models\LSTM6x64_cloud_cover,target=/models/LSTM6x64_cloud_cover  -e MODEL_NAME=LSTM6x64_cloud_cover -t tensorflow/serving
#               docker run -p 8500:8500 -p 8501:8501 --mount type=bind,source=D:\ProjectWeb\tfserving\models\LSTM6x64_cloud_cover,target=/models/LSTM6x64_cloud_cover  -e MODEL_NAME=LSTM6x64_cloud_cover -t tensorflow/serving
async def makePredictionRequest(data):
    predictionResult = []
    # Create the gRPC channel and stub
    channel = grpc.aio.insecure_channel('localhost:8500')
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

    for batch in data:
        # Create the predict request
        request = predict_pb2.PredictRequest()
        request.model_spec.name = 'LSTM6x64_cloud_cover'
        request.model_spec.signature_name = 'serving_default'

        request.inputs['input_7'].CopyFrom(tf.make_tensor_proto(batch, shape = (64, 20, 12), dtype = tf.float32))

        # Send the request and get the response
        response = await stub.Predict(request)
        batch_result = (json.loads(MessageToJson(response)))["outputs"]["dense_6"]["floatVal"]
        predictionResult.extend(batch_result)

    return predictionResult

async def batchData(data, batchSize, featureHorizon):
    batchedData = np.empty((0, batchSize, featureHorizon, 12))

    for i in range(0, data.shape[0] - batchSize, batchSize):
        # Last element in batchedData has different shape
        if i + batchSize + featureHorizon > data.shape[0]:
            otherSize = data.shape[0] - i - featureHorizon
            batch = np.empty((0, featureHorizon, 11))
            for j in range(i, i + otherSize):
                group = data[j:j+featureHorizon]
                batch = np.concatenate((batch, np.expand_dims(group, axis=0)), axis=0)
            pad_size = ((0, batchSize - otherSize), (0, 0), (0, 0))
            batch = np.pad(batch, pad_size, mode='constant', constant_values=0)
        
        else:
            batch = np.empty((0, featureHorizon, 12))
            for j in range(i, i + batchSize):
                group = data[j:j+featureHorizon]
                batch = np.concatenate((batch, np.expand_dims(group, axis=0)), axis=0)

        # Add batch to batchedData
        batchedData = np.concatenate((batchedData, np.expand_dims(batch, axis=0)), axis=0)
    return batchedData

async def testPrediction(request):
    # Connect to MongoDB database with requested database information
    client = MongoClient('mongodb+srv://pvcell:IXLCBUqW6U8FGUFr@cluster0.htuap5h.mongodb.net/userdatabase?retryWrites=true&w=majority')
    db = client['data']
    collection = db['Admin-1']

    # Retrieve data from collection
    dataframe = pd.DataFrame(list(collection.find({})))

    dataframeCleaned = dataframe.drop(['_id', 'datetime', 'year', 'month', 'day', 'hour', 'minute', 'second'], axis = 1)
    dataframeSelected = dataframeCleaned.drop(['Whac', 'VAh', 'Hz', 'kWhdc'], axis = 1)

    scaler = MinMaxScaler()
    dataframeScaled = scaler.fit_transform(dataframeSelected)

    # Batch data for prediction
    batchedData = await batchData(data = dataframeScaled, batchSize = 64, featureHorizon = 20)   

    # Use sync_to_async to run the send_request coroutine asynchronously
    prediction = await makePredictionRequest(batchedData)

    return JsonResponse(json.dumps(prediction), safe=False)

async def makePrediction(request):
    # Retrieve database information from request
    selectedCollection = request.GET.get('collection')

    # Connect to MongoDB database with requested database information
    client = MongoClient('mongodb+srv://pvcell:IXLCBUqW6U8FGUFr@cluster0.htuap5h.mongodb.net/userdatabase?retryWrites=true&w=majority')
    database = client['data']
    username = await sync_to_async(lambda: request.user.username)()
    collection = database[f"{username}:{selectedCollection}"]

    # Retrieve data from collection
    dataframe = pd.DataFrame(await sync_to_async(list)(collection.find({})))

    # Drop unnecessary and unneeded data
    dataframeCleaned = dataframe.drop(['_id', 'datetime', 'year', 'month', 'day', 'hour', 'minute', 'second'], axis = 1)
    dataframeSelected = dataframeCleaned.drop(['Whac', 'VAh', 'Hz', 'kWhdc'], axis = 1)

    # Scale data 
    scalers = dict()
    for col in dataframeSelected.columns:
        scaler = MinMaxScaler()
        scaler.fit(dataframeSelected[[col]])
        scalers[col] = scaler

    dataframeScaled = pd.DataFrame()
    for col in dataframeSelected.columns:
        scaler = scalers[col]
        dataframeScaled[col] = scaler.transform(dataframe[[col]]).reshape(-1)

    # Batch data for prediction
    batchedData = await batchData(data = dataframeScaled, batchSize = 64, featureHorizon = 20)

    # Use sync_to_async to run the send_request coroutine asynchronously
    predictionResult = await makePredictionRequest(batchedData)

    # trim result from last batch since it's from padded value
    predictionResult = predictionResult[:dataframeScaled.shape[0] - 20]

    # re-rescale data to real value
    predictionResult = scalers['W'].inverse_transform(np.array(predictionResult).reshape(-1, 1))

    # add date back to prediction result
    predictionResult = pd.DataFrame(predictionResult, columns = ['W'])
    predictionResult['datetime'] = dataframe['datetime'].iloc[25:].reset_index(drop = True)

    # plot scaled real value compare to prediontion result
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = dataframe.index, y = dataframe['W'], name = 'Real Value'))
    fig.add_trace(go.Scatter(x = predictionResult.index + 25, y = predictionResult['W'], name = 'Prediction Result'))
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

    graph = fig.to_html(full_html = False)
    request.session['graph'] = graph

    return redirect(reverse('result'))
