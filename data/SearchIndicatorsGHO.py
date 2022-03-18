from urllib.request import urlopen
import json
import numpy as np
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

def SearchIndicatorsGHO(userInput):
    userInput = userInput.replace(" ", "%20")
    response = urlopen(f"https://ghoapi.azureedge.net/api/Indicator?$filter=contains(IndicatorName,'{userInput}')")
    json_data = response.read().decode('utf-8', 'replace')
    d = json.loads(json_data)
    df_Indicators = pd.json_normalize(d['value'])
    return(df_Indicators)