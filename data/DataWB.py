import pandas as pd
import matplotlib.pyplot as plt
import wbgapi as wb
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

#Return as a dataFrame
source = pd.DataFrame(wb.source.list())

def IndicatorsDataWB(IndicatorId):
    for i in list(source['id']):
        wb.db = i
        try:
            data=wb.data.DataFrame(IndicatorId,
                                   wb.region.members('AFR'),
                                   #time = range(2000, 2023,1),
                                   skipBlanks=True,
                                   columns='series',
                                   labels = True)
            data.reset_index()
            break
        except ValueError:
            continue
    return(data)