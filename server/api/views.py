from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pandas import pandas as pd
import json




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
        age = ''
        if('Age' in body):
            age = body['Age']
        return Response(manipulateData(education, jobtitle, age))

    return Response(status=status.HTTP_400_BAD_REQUEST)


def manipulateData(education, jobtitle, age):
    df = pd.read_csv('data/genderPayGap.csv')
    df['PayPlusBonus'] = df['BasePay'] + df['Bonus']
    mdata = df
    if(education != "Alle anzeigen" and education != ''):
        mdata = mdata.loc[(df['Education'] == education)]
    if(jobtitle != "Alle anzeigen" and jobtitle != ''):
        mdata = mdata.loc[(df['JobTitle'] == jobtitle)]
    if(age != "Alle anzeigen" and age != ''):
        min, max = min_max_age(age)
        mdata = mdata.loc[(df['Age'] > min) & (df['Age'] < max)]
    gender = mdata["Gender"].value_counts()
    female = gender.Female
    male = gender.Male
    mdata_result = mdata.to_json(orient="records")
    mdata_json = json.loads(mdata_result)
    return mdata_json, male, female

def min_max_age(age):
    age = age.split(" - ")
    min, max = int(age[0]), int(age[1])
    return min, max