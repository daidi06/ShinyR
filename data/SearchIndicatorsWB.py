import pandas as pd
import matplotlib.pyplot as plt
import wbgapi as wb
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

#Return as a dataFrame
source = pd.DataFrame(wb.source.list())

def SearchIndicatorsWB(userInput):
    Id = []
    Name = []
    MetaData = []

    for i in list(source['id']):
        wb.db = i
        for k,v in wb.search(userInput).metadata.items():
            for elem in v:
                if elem.id not in Id:
                    Id.append(elem.id)
                    Name.append(elem.name)
                    MetaData.append(elem.metadata.get('Longdefinition'))
    searchData = pd.DataFrame({'CodeId':Id, 'Name':Name, 'Metadata':MetaData})
    return(searchData)