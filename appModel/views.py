
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

import json
from google.protobuf.json_format import MessageToJson

import numpy as np
import pandas as pd
from pymongo import MongoClient
from sklearn.preprocessing import MinMaxScaler

import tensorflow as tf
import grpc
from tensorflow.keras.preprocessing import sequence
from tensorflow_serving.apis import predict_pb2, prediction_service_pb2_grpc
from asgiref.sync import sync_to_async
# Create your views here.


@login_required
def model(request):
    return render(request, 'appModel/model.html')

@login_required
def predict(request):
    return render(request, 'appModel/predict.html')

# to run tensorflow serving,  follow these steps
# 1. install docker desktop
# 2. in any terminal, run docker pull tensorflow/serving
# 3. in tfserving directory terminal, run docker run -p 8500:8500 -p 8501:8501 --mount type=bind,source=absolute\path\to\work\folder\Web\tfserving\models\LSTM6x64_cloud_cover,target=/models/LSTM6x64_cloud_cover  -e MODEL_NAME=LSTM6x64_cloud_cover -t tensorflow/serving
# for Wanna is docker run -p 8500:8500 -p 8501:8501 --mount type=bind,source=C:\University\Year-4\Project\Python\Web\tfserving\models\LSTM6x64_cloud_cover,target=/models/LSTM6x64_cloud_cover  -e MODEL_NAME=LSTM6x64_cloud_cover -t tensorflow/serving

async def predict_request(data):
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

async def make_prediction_beta(request):
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
    batchSize = 64
    dataHorizon = 20

    batchedData = np.empty((0, batchSize, dataHorizon, 11))
    for i in range(0, dataframeScaled.shape[0] - batchSize, batchSize):
        if i + batchSize + dataHorizon > dataframeScaled.shape[0]:
            # Last element in batchedData has different shape
            otherSize = dataframeScaled.shape[0] - i - dataHorizon
            batch = np.empty((0, dataHorizon, 11))
            for j in range(i, i + otherSize):
                group = dataframeScaled[j:j+dataHorizon]
                batch = np.concatenate((batch, np.expand_dims(group, axis=0)), axis=0)
            pad_size = ((0, batchSize - otherSize), (0, 0), (0, 0))
            batch = np.pad(batch, pad_size, mode='constant', constant_values=0)
        else:
            batch = np.empty((0, dataHorizon, 11))
            for j in range(i, i + batchSize):
                group = dataframeScaled[j:j+dataHorizon]
                batch = np.concatenate((batch, np.expand_dims(group, axis=0)), axis=0)

        # Add batch to batchedData
        batchedData = np.concatenate((batchedData, np.expand_dims(batch, axis=0)), axis=0)


    # Use sync_to_async to run the send_request coroutine asynchronously
    prediction = await predict_request(batchedData)

    return JsonResponse(json.dumps(prediction), safe=False)

async def make_prediction(request):
    if request.method == 'POST':
        # Retrieve database information from request
        databaseInfo = json.loads(request.body)
        databaseName = databaseInfo['databaseName']
        collectionName = databaseInfo['collectionName']

        # Connect to MongoDB database with requested database information
        client = MongoClient('mongodb+srv://pvcell:IXLCBUqW6U8FGUFr@cluster0.htuap5h.mongodb.net/userdatabase?retryWrites=true&w=majority')
        database = client[databaseName]
        collection = database[collectionName]

        # Retrieve data from collection
        dataframe = pd.DataFrame(list(collection.find({})))

        # Drop unnecessary and unneeded data
        dataframeCleaned = dataframe.drop(['_id', 'datetime', 'year', 'month', 'day', 'hour', 'minute', 'second'], axis = 1)
        dataframeSelected = dataframeCleaned.drop(['Whac', 'VAh', 'Hz', 'kWhdc'], axis = 1)

        # Scale data 
        scaler = MinMaxScaler()
        dataframeScaled = scaler.fit_transform(dataframeSelected)

         # Batch data for prediction
        batchSize = 1
        dataHorizon = 20

        batchedData = np.empty((0, batchSize, dataHorizon, 11))
        for i in range(0, dataframeScaled.shape[0] - batchSize - dataHorizon, batchSize):
            batch = np.empty((0, dataHorizon, 11))
            for j in range(i, i + batchSize):
                group = dataframeScaled[j:j+dataHorizon]
                batch = np.concatenate((batch, np.expand_dims(group, axis = 0)), axis = 0)
            batchedData = np.concatenate((batchedData, np.expand_dims(batch, axis = 0)), axis = 0)

        # Use sync_to_async to run the send_request coroutine asynchronously
        predictionResult = await predict_request(batchedData)

        return JsonResponse(predictionResult, safe = False)
    else:
        return HttpResponseServerError()
