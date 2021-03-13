'''
Jay Jung
09/24/19
The function get_access_
'''

import requests
import json
from adobe_sign_api_jay import AdobeSignAPIJay
import pandas as pd
import re
from config_helper import Config
import pyodbc
from ADOBEDao import ADOBEDao

'''
Return connection. If fail, return error message in a string
'''
def connect(sqlConfig):
    server = sqlConfig["host"]
    user = sqlConfig["user"]
    password = sqlConfig["password"]
    db = sqlConfig["db"]
    try:
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'+
                        'SERVER='+ server +';'+
                        'DATABASE='+ db +';' +
                        'uid='+ user + ';' +
                        'pwd=' + password + ';')
    except pyodbc.Error as error:
        return(str(error))
    return conn

def get_nextCursor(json):
    page = json['page']
    try:
        return page['nextCursor']
    except:
        return ''

def get_signed_ids(final_agreements, documentType):
    signed_ids = []
    for agreements in final_agreements:
        for doc in agreements:
            name = doc['name']
            status_signed = doc['status']
            if name.startswith(documentType) and status_signed == "SIGNED":
                signed_ids.append(doc['id'])
    return signed_ids

def get_agreements(adobe_sign_token):
    final_agreements = []
    # Edge Case
    headers = {'Authorization': "Bearer "+ adobe_sign_token}
    response1 = requests.get('https://api.na2.echosign.com:443/api/rest/v6/agreements', headers=headers)
    agreements = response1.json()['userAgreementList']
    final_agreements.append(agreements)
    nextCursor = get_nextCursor(response1.json())

    # Navigate through cursors to get all the data
    while nextCursor != '':
        params =  {'cursor':nextCursor}
        response2 = requests.get('https://api.na2.echosign.com:443/api/rest/v6/agreements', headers=headers, params=params)
        agreements = response2.json()['userAgreementList']
        final_agreements.append(agreements)
        nextCursor = get_nextCursor(response2.json())
    return final_agreements

# THIS FUNCTION NEEDS TO BE UPDATED SUCH TAHT IT GENERATES ACCESSTOEKN AND REFRESH TOKEN FIRST.
def get_access_token():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {
        'refresh_token': '3AAABLblqZhAePfGl2V-0ctSLYUTEHaj-S7D-cwCOjhtMdWemJod1KY1fJz48WD-aryTZmN1QJMY*',
        'client_id': 'CBJCHBCAABAAY2mkNnOxJSnxNJg3Zh0FDxy4RhtEbSK3',
        'client_secret': '0kU5btCbKNwcNfL_yWoUpK42mPZe6-SJ',
        'grant_type': 'refresh_token',
    }
    url = 'https://api.na2.echosign.com/oauth/refresh'
    r = requests.post(url, headers=headers, data= payload)
    if r.status_code in (200, 201):
        return r.json()['access_token']
    else:
        return ("ERROR! Can't get the access token. Status code is ", r.status_code)
    
def df_cleaning(df, columns):
    df = df[df['role'] != 'APPROVER']
    df = df[columns]
    ssn = list(df['SSN'])
    for i in range(len(ssn)-1):
        try:
            ssn[i] = ssn[i][-4:]
        except Exception as e:
            print(e)
    df['SSN'] = ssn
    return df

def main_w4():
    adobe_sign_token = get_access_token()
    headers = {'Authorization': "Bearer "+ adobe_sign_token}
    # Used to store data extracted from API
    final_agreements = get_agreements(adobe_sign_token)
    # Extract only the ids with 'W-4' and 'Signed'
    w4_signed_ids = get_signed_ids(final_agreements,'W-4') # document_type
    # Create dataframe
    columns = ["completed","email","role","first","last","title","company","A","AddlWithholding","Address","Address2","B","C","Claiming","D","E","EIN","Eight","Exempt","F","Field1","Field2","Field3","Field4","Field5","Field6","Field7","Field8","Field9","FirstName","Five","Four","G","Group3","H","Last.Name.Differs.From.SSCard","LastName","OfficeCode","One","SSN","Seven","Six","Ten","Three","Two","agreementId","mpNameAddress"]
    
    # Used to create dataframe
    double_list = []
    
    for id in w4_signed_ids:
        # Extract data 
        r = requests.get('https://api.na2.echosign.com:443/api/rest/v6/agreements/'+str(id)+'/formData', headers=headers)
        r.encoding = 'utf-8-sig'
        text = r.text
        text_list = text.split('\n')
        for i in text_list[1:3]:
            singe_value = re.findall(r'\"(.*?)\"', i)
            # if len(singe_value) != 0:
            #     singe_value.append("")
            double_list.append(singe_value)

    df = pd.DataFrame(double_list, columns=columns)
    df = df_cleaning(df,['completed', 'email', 'AddlWithholding', 'Address', 'Address2', 'Claiming', 'Exempt', 'FirstName', 'Group3', 'LastName', 'SSN'])

    config = Config()
    conn = connect(config.get("Database"))
    
    adobeDao = ADOBEDao(conn)
    adobeDao.truncate_table(config.get('Database')['tablename'])
    adobeDao.add_or_update_records(config.get("Database")['tablename'], df)
    print("ETL to " + config.get('Database')['tablename'] + ' successfully completed.')

def main_direct_deposit():
    adobe_sign_token = get_access_token()
    headers = {'Authorization': "Bearer "+ adobe_sign_token}
    final_agreements = get_agreements(adobe_sign_token)
    
    # Extract only the ids with 'W-4' and 'Signed'
    direct_deposit_signed_ids = get_signed_ids(final_agreements, 'Direct Deposit - New Hire Agreement')

    # Create dataframe
    columns = ["completed","email","role","first","last","title","company","% of Net Pay $ Amount 1","% of Net Pay $ Amount 2","Account Number 1","Account Number 2","Account Type 1","Account Type 2","Bank 1: Deposit Option","Bank 2: Deposit Options","Bank Name 1","Bank Name 2","Routing Number 1","Routing Number 2","SSN","Specific $ Amount $ 1","Specific $ Amount $ 2","Use Information On File","agreementId"]
    
    # Used to create dataframe
    double_list = []

    for id in direct_deposit_signed_ids:
        # Extract data 
        r = requests.get('https://api.na2.echosign.com:443/api/rest/v6/agreements/'+str(id)+'/formData', headers=headers)
        r.encoding = 'utf-8-sig'
        text = r.text
        text_list = text.split('\n')
        writer = text_list[1]
        # try:
        #     writer = text_list[1]
        # except Exception as e:
        #     print(e)
        singe_value = re.findall(r'\"(.*?)\"', writer)
        if len(singe_value) == 25:
            singe_value = singe_value[:24]
        double_list.append(singe_value)
        # for i in text_list[1]:
        #     singe_value = re.findall(r'\"(.*?)\"', i)
        #     # if len(singe_value) != 0:
        #     #     singe_value.append("")
        #     double_list.append(singe_value)

    df = pd.DataFrame(double_list, columns=columns)
    df = df_cleaning(df, columns)

    config = Config()
    conn = connect(config.get("Database2"))
    adobeDao = ADOBEDao(conn)
    adobeDao.truncate_table(config.get('Database2')['tablename'])
    adobeDao.add_or_update_records(config.get("Database2")['tablename'], df)
    print("ETL to " + config.get('Database2')['tablename'] + ' successfully completed.')

if __name__ == '__main__':
    main_direct_deposit()
    main_w4()
    #print(get_access_token())
