#!/usr/bin/env python
# coding: utf-8

# In[1]:


import urllib
from urllib.request import urlopen
import json
import numpy as np
import pandas as pd
import os



def IndicatorGHO(IndicatorCode, Indicator_Name, fileName, SourceName):
    response = urlopen("https://ghoapi.azureedge.net/api/DIMENSION/COUNTRY/DimensionValues")
    json_data = response.read().decode('utf-8', 'replace')
    d = json.loads(json_data)
    df_Code = pd.json_normalize(d['value'])
    df_Code.rename(columns={'Code': 'SpatialDim'}, inplace=True)
    API = "https://ghoapi.azureedge.net/api/"
    response = urlopen(API + IndicatorCode)
    json_data = response.read().decode('utf-8', 'replace')
    d = json.loads(json_data)
    df = pd.json_normalize(d['value'])
    df_merged = pd.merge(df, df_Code, how='outer', on='SpatialDim')
    
    df_merged['Title'] = np.where((df_merged.SpatialDim=="AFR") | (df_merged.SpatialDim=="WHO_LMI_AFR"), "Africa", df_merged.Title)
    df_merged['ParentTitle'] = np.where((df_merged.SpatialDim=="AFR") | (df_merged.SpatialDim=="WHO_LMI_AFR"), "Africa", df_merged.ParentTitle)
    #df_merged['Title'] = np.where(df_merged.SpatialDim=="AFR", "Africa", df_merged.Title)
    #df_merged['ParentTitle'] = np.where(df_merged.SpatialDim=="AFR", "Africa", df_merged.ParentTitle)
    
    df_merged_afro = df_merged[df_merged.ParentTitle=="Africa"]
    df_merged_afro = df_merged[df_merged.ParentTitle=="Africa"][["Title", 'IndicatorCode', 'Dim1', 'TimeDim', 'NumericValue']]
    df_merged_afro.rename(columns={'Title': 'Country', 'IndicatorCode': 'Indicator_Name', 'Dim1': 'Options',
                               'TimeDim': 'Start_Period', 'NumericValue': 'Value_received' }, inplace=True)
    
    df_merged_afro.drop(df_merged_afro[df_merged_afro.Country.isin(['Saint Helena', 'Mayotte', 'Reunion'])].index, inplace=True)
    #df_merged_afro = df_merged_afro.dropna()
    
    df_merged_afro.loc[:,'Indicator_Name'] = Indicator_Name
    df_merged_afro.loc[:,'Measure_type'] = "Numeric"
    df_merged_afro.loc[:,'Source'] = SourceName
    df_merged_afro.loc[:,'Options'] = np.where(df_merged_afro.Options=="MLE", "Male",
                                           np.where(df_merged_afro.Options=="FMLE", "Female",
                                                    np.where(df_merged_afro.Options=="BTSX", "Both sexes",df_merged_afro.Options)))
    df_merged_afro.loc[:,'Options'] = np.where(df_merged_afro.Options=="URB", "Urban",
                                           np.where(df_merged_afro.Options=="RUR", "Rural",
                                                    np.where(df_merged_afro.Options=="TOTL", "Total",df_merged_afro.Options)))
    df_merged_afro.loc[:,'End_Period'] = df_merged_afro.loc[:,'Start_Period']
    
    #cols = ['Start_Period', 'End_Period']
    #df_merged_afro[cols] = df_merged_afro[cols].applymap(np.int32)
    #df_merged_afro
    
    df_merged_afro = df_merged_afro[["Country", 'Indicator_Name', 'Options', 'Start_Period', 'End_Period',
                                "Value_received", 'Measure_type', 'Source']]
    path = r'D:\PERSONNEL\OMS\TRAVAIL\Indicateur\Demo\Output'

    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    
    if not isExist:
        # Create a new directory because it does not exist 
        os.makedirs(path)
    df_merged_afro.to_csv (path + '\\' + fileName + '.csv', index = False, header=True)


# # Loop through all the indicators

# In[46]:


ListOfIndicators = pd.read_csv(r'D:\PERSONNEL\OMS\TRAVAIL\Indicateur\Demo\Files\IndicatorsCodeGHO.csv', encoding='iso-8859-1')

# In[47]:


for index, row in ListOfIndicators.iterrows():
    try:
        IndicatorGHO(row['IndicatorCodeGHO'], row['Indicator'], row['FileName'], row['Source'])
        print(f"The indicator number {index+1} is processed, please go and check to D:\DownloadTest2")
    except ValueError:
        print(f"The indicator number {index+1} is not processed because of ValueError")
    except urllib.request.HTTPError:
        print(f"The indicator number {index+1} is not processed because of HTTPError")


# In[ ]:




