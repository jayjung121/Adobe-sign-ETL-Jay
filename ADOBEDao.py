import pyodbc
from datetime import datetime
import dateparser
import pandas as pd
from string import digits, ascii_uppercase, ascii_lowercase

class ADOBEDao:
    def __init__(self, connection):
        self.conn = connection
        self.paramMarker = "?"
        self.column_names_w4 = ['completed', 'email', 'AddlWithholding', 'Address', 'Address2', 'Claiming', 'Exempt', 'FirstName', 'Group3', 'LastName', 'SSN']
        self.column_names_direct_deposit = ["completed","email","role","first","last","title","company","[% of Net Pay $ Amount 1]","[% of Net Pay $ Amount 2]","[Account Number 1]","[Account Number 2]","[Account Type 1]","[Account Type 2]","[Bank 1: Deposit Option]","[Bank 2: Deposit Options]","[Bank Name 1]","[Bank Name 2]","[Routing Number 1]","[Routing Number 2]","SSN","[Specific $ Amount $ 1]","[Specific $ Amount $ 2]","[Use Information On File]","agreementId"]
    
    def truncate_table(self, tablename):
        cursor = self.conn.cursor()
        cursor.execute("Truncate Table " + tablename +";")
        self.conn.commit()
    
    ## LET"S IMPLEMENT STORED PROCEJRE LATER~!!!!
    def add_or_update_records(self, tablename, df):
        cursor = self.conn.cursor()
        if tablename == 'dbo.AdobeSign_Direct_Deposit':
            insertStatement = self._get_query_string_direct_deposit(tablename)
        else:
            insertStatement = self._get_query_string_w4(tablename)
        #updateQuery, updateOrder = self._get_update_query_string(tablename, df.iloc[0])
        for index, row in df.iterrows():
            if index % 1000==0:
                print("Currently at index", index)
            try:
                cursor.execute(insertStatement, tuple(row))
            except pyodbc.Error as error:
                # if error.args[0] != '23000': # Duplicate primary key value. 
                #     try:
                #         cursor.execute(updateQuery, self._convert_to_tuple(row, updateOrder))
                #     except pyodbc.Error as error:
                #         print(error, row)
                # else:
                    print(error, row)   
        self.conn.commit()
    
    # 
    def _get_query_string_direct_deposit(self, tablename):
        # KeyList is list of name of columns
        #keyList = record.keys()
        query = "INSERT INTO " + tablename + " (" + ', '.join(self.column_names_direct_deposit) + ") VALUES ("
        typeList = [self.paramMarker for _ in self.column_names_direct_deposit]
        values = ', '.join(typeList)
        return(query + values + ")")

    # # Returns Update query and list of parameters in order.
    # def _get_update_query_string_w4(self, tablename):
    #     query = "UPDATE " + tablename + " SET "
    #     keyList = list(record.keys())
    #     columnList = [key+"="+self.paramMarker for key in keyList]
    #     values = ', '.join(columnList)
    #     querySuffix = " WHERE recordid = " + self.paramMarker
    #     keyList.append('recordid')
    #     return(query + values + querySuffix, keyList) 

    #     # Returns Update query and list of parameters in order.
    # def _get_update_query_string_direct_deposit(self, tablename):
    #     query = "UPDATE " + tablename + " SET "
    #     keyList = self.column_names_direct_deposit
    #     columnList = [key+"="+self.paramMarker for key in keyList]
    #     values = ', '.join(columnList)
    #     querySuffix = " WHERE recordid = " + self.paramMarker
    #     keyList.append('recordid')
    #     return(query + values + querySuffix, keyList) 

    def _get_query_string_w4(self, tablename):
        # KeyList is list of name of columns
        #keyList = record.keys()
        query = "INSERT INTO " + tablename + " (" + ', '.join(self.column_names_w4) + ") VALUES ("
        typeList = [self.paramMarker for _ in self.column_names_w4]
        values = ', '.join(typeList)
        return(query + values + ")")

    
    def _convert_to_datetimeString(self, dateString):
        if type(dateString) == datetime:
            return (dateString.strftime('%Y-%m-%d %H:%M:%S'))
        elif dateString:
            allowed_dateTimeChar = digits + ascii_lowercase + ascii_uppercase + '.,/:- '
            filteredString = ''.join(char if char in allowed_dateTimeChar else '' for char in dateString)
            return dateparser.parse(filteredString, languages=['en']).strftime('%Y-%m-%d %H:%M:%S')