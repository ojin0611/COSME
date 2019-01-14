import os
import pandas as pd
import json, csv, sys
from pandas.io.json import json_normalize
import time
import datetime
from operator import itemgetter 

def getJsonFileNameList(mydir):

    fileNameList =os.listdir(mydir)
    jsonFileNameList=[]
    for file in fileNameList:
        if file[-4:] == 'json':
            jsonFileNameList.append(file)
        
    return jsonFileNameList

def json2dataframe(mydir, jsonFile):
    with open(mydir + jsonFile,encoding='UTF8') as f:
        jsonData = json.load(f) # list 얻는다.
        
    df = pd.DataFrame.from_dict(json_normalize(jsonData), orient='columns')
    return df

def checkTime():
    time_check = time.time()
    now = datetime.datetime.now()
    print('---',now, '---')
    return time_check




def matchCheck(sentence, target):
    for word in sentence:
        if word not in target:
            return False
            
    return True

def matchLooseCheck(sentence, target):
    cnt=0
    for word in sentence:
        if word not in target:
            cnt+=1
            if cnt>1:
                return False
            
    return True

def perfectMatch(master, barcode, test=False):
    total_len = len(master)
    # Master 파일의 상품명, trim
    master_products = list(master['상품명 (한글)'])
    master_products_trim = [''.join(product.upper().split()) for product in master_products]

    # BARCODE 파일의 바코드와 상품명, trim
    barcode_barcode = list(barcode['BARCODE'])
    barcode_prnms = list(barcode['PRNM'])
    barcode_prnms_trim = [''.join(prnm.upper().split()) for prnm in barcode_prnms]

    # Time Check
    start_time = checkTime()
    print('--- Master Data 개수 :',total_len,'---')

    # 매칭 결과를 저장하는 list
    PRNM = [[] for i in range(total_len)]
    BARCODE = [[] for i in range(total_len)]

    # naive match start
    for idx, prod in enumerate(master_products_trim):
        matching = [i for i, prnm in enumerate(barcode_prnms_trim) if prod in prnm]
        if matching:
            BARCODE[idx].append(itemgetter(*matching)(barcode_barcode))
            PRNM[idx].append(itemgetter(*matching)(barcode_prnms))

        if idx == total_len//100:
            print("--- 예상 소요 시간 : %0.2f minutes" % float((time.time() - start_time)*100/60), '---')
            if test:
                break
        if idx % (total_len//50) == 0:
            print("%3.1f 퍼센트 진행중" % round(idx / total_len * 100))
            
    now = datetime.datetime.now()
    print('--- Match End :',now, '---')
    print("--- 전체 소요 시간 : %0.2f minutes ---" % float((time.time() - start_time)/60))
    master['BARCODE']=BARCODE
    master['PRNM']=PRNM

    return master

def naiveMatch(master, barcode, test=False):
    total_len = len(master)
    # Master 파일의 상품명, trim
    master_products = list(master['상품명 (한글)'])
    master_products_trim = [product.upper().split() for product in master_products]

    # BARCODE 파일의 바코드와 상품명, trim
    barcode_barcode = list(barcode['BARCODE'])
    barcode_prnms = list(barcode['PRNM'])
    barcode_prnms_trim = [''.join(prnm.upper().split()) for prnm in barcode_prnms]

    # Time Check
    start_time = checkTime()
    print('--- Master Data 개수 :',total_len,'---')

    # 매칭 결과를 저장하는 list
    PRNM = [[] for i in range(total_len)]
    BARCODE = [[] for i in range(total_len)]

    # match start    
    for i, prod in enumerate(master_products_trim):
        for j, prnm in enumerate(barcode_prnms_trim):
            if len(prod)<=3:
                if matchCheck(prod, prnm):
                    PRNM[i].append(barcode_prnms[j])
                    BARCODE[i].append(barcode_barcode[j])
            else:
                if matchLooseCheck(prod, prnm):
                    PRNM[i].append(barcode_prnms[j])
                    BARCODE[i].append(barcode_barcode[j])
                    
        if i == total_len//100 + 1:
            print("--- 예상 소요 시간 : %0.2f minutes" % float((time.time() - start_time)*100/60), '---')
            if test:
                break

        if i % (total_len//50) == 0:
            print("%3.1f 퍼센트 진행중" % round(i / total_len * 100))

    now = datetime.datetime.now()
    print('--- Match End :',now, '---')
    print("--- 전체 소요 시간 : %0.2f minutes ---" % float((time.time() - start_time)/60))

    master['BARCODE']=BARCODE
    master['PRNM']=PRNM

    return master



# 브랜드별 결과 보기
def matchingResult(master):
    brands = master.groupby('브랜드명 (한글)')
    brands = [brands.get_group(x) for x in brands.groups]

    sum1=0
    sum2=0
    for brand in brands:
        brand_total = len(brand)
        brand_match = 0
        
        for match in brand['PRNM']:
            if match:
                brand_match+=1
        
        sum1+=brand_total
        sum2+=brand_match
        print(brand['브랜드명 (한글)'].iloc[0],':', brand_match,'/', brand_total)
    print('전체 상품 개수 :',sum1)
    print('매칭된 상품 수 :',sum2)

# Match 안된 상품 모아보기
def notMatched(master):
    TF = [False for i in range(len(master))]

    for n,m in enumerate(master['BARCODE']):
        if not m:
            TF[n]=True
#    master = master[['브랜드명 (한글)','상품명 (한글)','원상품명']].loc[TF]
    return master.loc[TF]

