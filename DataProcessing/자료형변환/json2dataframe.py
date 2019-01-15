import json
import pandas as pd
from pandas.io.json import json_normalize

def json2dataframe(mydir, jsonFile):
    with open(mydir + jsonFile,encoding='UTF8') as f:
        jsonData = json.load(f) # list 얻는다.
        
    df = pd.DataFrame.from_dict(json_normalize(jsonData), orient='columns')
    return df