import pandas as pd
import urllib
from urllib.request import urlopen
import json
import wbgapi as wb

#Return as a dataFrame
source = pd.DataFrame(wb.source.list())

def IndicatorsMetaDataWB(IndicatorId):
    for i in list(source['id']):
    response = urlopen(f"https://api.worldbank.org/v2/en/sources/{i}/series/{IndicatorId}/metadata?format=json")
    json_data = response.read().decode('utf-8', 'replace')
    try:
        d = json.loads(json_data)
        dimGHO = pd.json_normalize(d["source"][0]["concept"][0]['variable'][0]['metatype'])
        break
    except ValueError:
        continue
    return dimGHO
