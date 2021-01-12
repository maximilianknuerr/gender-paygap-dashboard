from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pandas import pandas as pd
import json

@api_view(['POST'])
def gender_data(request):

    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        data = body['Data']
        df = pd.DataFrame(data)
        gender = df["Gender"].value_counts()

        return Response(gender)

    return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def data(request):
    
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        education = ''
        if('Education' in body):
            education = body['Education']
        jobtitle = ''
        if('JobTitle' in body):
            jobtitle = body['JobTitle']
        gender = ''
        if('Gender' in body):
            gender = body['Gender']
        return Response(manipulateData(education, jobtitle, gender))

    return Response(status=status.HTTP_400_BAD_REQUEST)


def manipulateData(education, jobtitle, gender):
    df = pd.read_csv('data/genderPayGap.csv')
    df['PayPlusBonus'] = df['BasePay'] + df['Bonus']
    mdata = df
    female = 0
    male = 0
    if(education != "Alle anzeigen" and education != ''):
        mdata = mdata.loc[(df['Education'] == education)]
    if(jobtitle != "Alle anzeigen" and jobtitle != ''):
        mdata = mdata.loc[(df['JobTitle'] == jobtitle)]
    if(gender != "Alle anzeigen" and gender != ''):
        mdata = mdata.loc[(df['Gender'] == gender)]
    else:
        genderA = mdata["Gender"].value_counts()
        female = genderA.Female
        male = genderA.Male

    mdata_result = mdata.to_json(orient="records")
    mdata_json = json.loads(mdata_result)
    return mdata_json, male, female

