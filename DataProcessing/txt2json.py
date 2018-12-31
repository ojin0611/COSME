import os
import json
from collections import OrderedDict

# 내 디렉토리 내에 어떤 파일들이 있을까?
def search_dir(dir):
    files = os.listdir(dir)
    print("----- My File list -----")
    for file in files:
        print(file)

# column name 얻기
def getColNames(dir_name,file_name):
    # 첫 줄 읽기
    f=open(dir_name + file_name)
    line=f.readline()
    f.close
    
    line=line[:-1]
    colNames = line.split('|')

    return colNames

# 텍스트 left dequote
def dequote(s):
    if s[0]=="'" or s[0]=='"':
        s=s[1:]
    if s[-1]=="'" or s[-1]=='"':
        s=s[:-1]
    return s
    
# "|"로 구분
def getListFromLine(line):
    items = line.split('"|"')
    return items
    


# txt to json
def getJSONfromTxt(dir_name,file_name,col_name,save_type=False,end_cnt=0):
    # Ready for data
    total_data = []
    
    c=0
    delete_1st_line = True
    prev = False
    
    for line in open(dir_name + file_name, 'r'):
        if delete_1st_line:
            delete_1st_line = False
            continue
            
        # line 우측 개행문자 제거 & 따옴표 제거
        line=line[:-1]
        line = dequote(line)
        
        items = getListFromLine(line)

        # 바코드로 시작하지 않을 경우 합쳐주기.
            
        if len(items)<6 or prev:
            if dequote(items[0]).isnumeric():
                prev_line = line
                prev=True
                continue
            else:
                line = prev_line + line
                items = getListFromLine(line)
                
                if len(items) == 6:
                    prev=False
                    prev_line=''
                else:
                    continue
            

        # 각 item을 json에 넣어준다.
        cnt=0
        product = OrderedDict()
        for item in items:
            product[col_name[cnt]] = dequote(item)
            cnt+=1
            
            
            
        # total_data 에 상품 한 개씩 저장
        
        total_data.append(product)
        c+=1
        if end_cnt>0 and c>=end_cnt:
            break
    
    if not save_type:
        jsonString = json.dumps(total_data,ensure_ascii=False)
        print('JSON file save complete!')
    else:
        jsonString = json.dumps(total_data,ensure_ascii=False, indent='\t')
        print('JSON file prettify complete!')
    return jsonString

        
def writeJSON(jsonString, output_name='data.json'):
    with open(output_name,'w',encoding='UTF-8') as file:
        file.write(jsonString)
        
def compareTxtJSON(dir_name, file_name, json_name='data.json'):
    print('--------JSON Summary--------')
    json_data=open(dir_name + json_name,encoding='UTF8').read()
    jingoos = json.loads(json_data)#, encoding='utf-8')
    len_json=len(jingoos)
    print('JSON 항목 개수:', len_json)

    cnt=0
    for i in range(len(jingoos)):
        if len(jingoos[i])==6:
            cnt+=1
        else:
            print(i, jingoos[i])

    print('각 항목의 속성이 6개 모두 있는 개수:',cnt)    
    
    print('--------Text Summary--------')
    cnt=0
    for line in open(dir_name + file_name, 'r'):
        items=line.split('|')
        d_item = dequote(items[0])
        if d_item.isnumeric():
    #        if len(d_item)==13:
            cnt+=1
    print('텍스트에서 시작이 BARCODE(숫자)인 line 개수:',cnt)    
    
    cnt=0
    for line in open(dir_name + file_name, 'r'):
        cnt+=1
    print('개행문자 신경 안쓰고 읽을 때 line 개수:',cnt)    
    
