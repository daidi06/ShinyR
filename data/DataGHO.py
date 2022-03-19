import urllib
from urllib.request import urlopen
import json
import numpy as np
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

def IndicatorsDataGHO(IndicatorCode):
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
    
    df_merged_afro = df_merged[df_merged.ParentTitle=="Africa"]
    df_merged_afro = df_merged[df_merged.ParentTitle=="Africa"][["Title", 'IndicatorCode', 'Dim1', 'TimeDim', 'NumericValue']]
    df_merged_afro.rename(columns={'Title': 'Country', 'IndicatorCode': 'Indicator_Name', 'Dim1': 'Options',
                               'TimeDim': 'Start_Period', 'NumericValue': 'Value_received' }, inplace=True)
    
    df_merged_afro.drop(df_merged_afro[df_merged_afro.Country.isin(['Saint Helena', 'Mayotte', 'Reunion'])].index, inplace=True)
    
    df_merged_afro.loc[:,'Options'] = np.where(df_merged_afro.Options=="MLE", "Male",
                                           np.where(df_merged_afro.Options=="FMLE", "Female",
                                                    np.where(df_merged_afro.Options=="BTSX", "Both sexes",df_merged_afro.Options)))
    df_merged_afro.loc[:,'Options'] = np.where(df_merged_afro.Options=="URB", "Urban",
                                           np.where(df_merged_afro.Options=="RUR", "Rural",
                                                    np.where(df_merged_afro.Options=="TOTL", "Total",df_merged_afro.Options)))
    
    df_merged_afro = df_merged_afro[["Country", "Options", "Start_Period", "Value_received"]]
    return df_merged_afro