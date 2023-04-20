
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

async def predict_request(df):
    # Apply the TimeseriesGenerator to the input data
    batched = []
    for i in range(0, 64):
        batched.append(df[i:i+20])

    batched = np.array(batched)

    # Create the gRPC channel and stub
    channel = grpc.aio.insecure_channel('localhost:8500')
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

    # Create the predict request
    request = predict_pb2.PredictRequest()
    request.model_spec.name = 'LSTM6x64_cloud_cover'
    request.model_spec.signature_name = 'serving_default'

    request.inputs['input_7'].CopyFrom(tf.make_tensor_proto(batched, shape=(64, 20, 12), dtype=tf.float32))

    # Send the request and get the response
    response = await stub.Predict(request)

    # Get the prediction from the response
    # output_data = tf.make_ndarray(response.outputs['value'])

    return response

async def predict_beta(request):
    client = MongoClient('mongodb+srv://wannawanna:d1Dj8cOiWwUCIxQs@cluster0.htuap5h.mongodb.net/userdatabase?retryWrites=true&w=majority')
    db = client['data']
    collection = db['admin-1']

    # Retrieve data from collection
    cursor = collection.find({})
    data = list(cursor)

    # Convert cursor data to Pandas DataFrame
    df = pd.DataFrame(data)

    df_cleaned = df.drop(['_id', 'datetime', 'year', 'month', 'day', 'hour', 'minute', 'second'], axis = 1)
    df_selected = df_cleaned.drop(['Whac', 'VAh', 'Hz', 'kWhdc'], axis = 1)

    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df_selected)

    # Use sync_to_async to run the send_request coroutine asynchronously
    prediction = await predict_request(df_scaled)

    json_data = json.loads(MessageToJson(prediction))

    return JsonResponse(json_data)
