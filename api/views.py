#Import necessary libraries
import pickle
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
import numpy as np

# Create your views here.
@api_view(['GET'])
def index_page(request):
    return_data = {
        "error" : "0",
        "message" : "Successful",
    }
    return Response(return_data)

@api_view(["POST"])
def predict_diabetictype(request):
    try:
        age = request.data.get('age',None)
        bs_fast = request.data.get('bs_fast',None)
        bs_pp = request.data.get('bs_pp',None)
        plasma_r = request.data.get('plasma_r',None)
        plasma_f = request.data.get('plasma_f',None)
        hbA1c = request.data.get('hbA1c',None)
        if age != None and bs_fast != None and bs_pp != None and plasma_r != None and plasma_f != None and hbA1c != None:
            #Datapreprocessing Convert the values to float
            age = float(age)
            bs_fast = float(bs_fast)
            bs_pp = float(bs_pp)
            plasma_r = float(plasma_r)
            plasma_f = float(plasma_f)
            hbA1c = float(hbA1c)
            result = [age,bs_fast,bs_pp,plasma_r,plasma_f,hbA1c]
            #Passing data to model & loading the model from disks
            model_path = 'ml_model/model.pkl'
            classifier = pickle.load(open(model_path, 'rb'))
            prediction = classifier.predict([result])[0]
            conf_score =  np.max(classifier.predict_proba([result]))*100
            predictions = {
                'error' : '0',
                'message' : 'Successfull',
                'prediction' : prediction,
                'confidence_score' : conf_score
            }
        else:
            predictions = {
                'error' : '1',
                'message': 'Invalid Parameters'                
            }
    except Exception as e:
        predictions = {
            'error' : '2',
            "message": str(e)
        }
    
    return Response(predictions)