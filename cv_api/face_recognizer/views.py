from django.shortcuts import render

# Create your views here.
# import the necessary packages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import numpy as np
# import urllib # python 2
import urllib.request # python 3
import json
import cv2
import os

def facedetect(request):
    if request.method == "GET":
        detectedNameList=[] # a list to store detected name for searching
        item=''
        currenSectionTime= datetime.datetime.now().time()
        
        client = MongoClient("mongodb+srv://fathimanahada06:fnhd_681@cluster0.clnokkg.mongodb.net/?retryWrites=true&w=majority")
         #db
        db = client.get_database('emotion')
        #collection
        records = db.collection
        
        def add_data(name, time, avg_emotion):
             document = {
                 "Name": name,
                 "Time": time,
                 #"Dominant_emotion": dominant_emotion,
                 "Average_emotion": avg_emotion
             }
             return records.insert_one(document)
        
        class FaceRecognition:
