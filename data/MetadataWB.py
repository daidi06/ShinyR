import pandas as pd
import wbgapi as wb


#Return as a dataFrame
source = pd.DataFrame(wb.source.list())

def IndicatorsMetaDataWB(IndicatorId):
    for i in list(source['id']):
        wb.db = i
        for k,v in wb.search(userInput).metadata.items():
            for elem in v:
                if elem.id == IndicatorId:
                    metadata = wb.series.metadata.get(IndicatorId)
        break 
    return(metadata)