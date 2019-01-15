import os # listdir (get filelist)
import pandas as pd
import ast # to convert a string to dict
import csv
from collections import Counter
from matplotlib import pyplot as plt
from matplotlib import font_manager, rc

font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)

# Import ---------------------------------------------------------------------

# csv to dataframe
def csv2df(mydir,inp):
    print(inp,'reading')
    try:
        data = pd.read_csv(mydir+inp, encoding='UTF-8')
    except:
        data = pd.read_csv(mydir+inp, encoding='cp949')
    return data

# dataframe 저장
def saveAllFile(dir_data, filelist):
    data={}
    for i in range(len(filelist)):
        inputfilename= filelist[i]
        if inputfilename[-3:] != 'csv':
            continue
        df = csv2df(dir_data,inputfilename)
        data[inputfilename]=df
        
    return data

# User ---------------------------------------------------------------------

def setUser(user):
    age = []
    gender   = []
    skinTone = []
    skinType = []
    skinConcern1 = []
    skinConcern2 = []
    skinConcern3 = []

    for i in range(len(user)):
        # 나이, 성별

        try:
            userAge = 2020 - int(ast.literal_eval(user['profileproperties'][i])['birthday'][:4])
            userGender = ast.literal_eval(user['profileproperties'][i])['gender']
        except:
            userAge = 0
            userGender = '#'

        # skinTone, skinType, skinConcerns
        try:
            userSkinTone = ast.literal_eval(user['basicskininfo'][i])['skinTone']
            userSkinType = ast.literal_eval(user['basicskininfo'][i])['skinType']
            userSkinConcerns = ast.literal_eval(user['basicskininfo'][i])['skinConcerns']
        except:
            userSkinTone = '#'
            userSkinType = '#'
            userSkinConcerns = ['#','#','#']


        while len(userSkinConcerns) < 3:
            userSkinConcerns.append('#')

        age.append(userAge)
        gender.append(userGender)
        skinTone.append(userSkinTone)
        skinType.append(userSkinType)
        skinConcern1.append(userSkinConcerns[0])
        skinConcern2.append(userSkinConcerns[1])
        skinConcern3.append(userSkinConcerns[2])
        
    # column 추가
    user['age']         = age
    user['gender']      = gender
    user['skinTone']    = skinTone
    user['skinType']    = skinType
    user['skinConcern1']= skinConcern1
    user['skinConcern2']= skinConcern2
    user['skinConcern3']= skinConcern3
    user = user.drop(columns=['basicskininfo','profileproperties'])
    
    return user

def change_skinConcerns(user):
    skinConcerns_list=[]
    for skinConcerns in user['skinConcerns']:
        while skinConcerns[-3:]=='"#"':
            if len(skinConcerns)<4:
                break
            skinConcerns = skinConcerns[:-4]
        skinConcerns_list.append('['+skinConcerns+']')    
    user['skinConcerns'] = skinConcerns_list
    return user



# Tag ---------------------------------------------------------------------

def join_tags_activity(dic_data, activity):
    caller = dic_data[activity]
    other  = dic_data['posts_tags.csv']
    try:
        tags_activity = caller.set_index('postid').join(other.set_index('postid'))
    except:
        tags_activity = caller.set_index('targetid').join(other.set_index('postid'))
        tags_activity.index.name = 'postid'

    tags_activity = tags_activity.reset_index()
    tags_activity = tags_activity.drop_duplicates()
    tags_activity = tags_activity.dropna(subset=['name'])

    tags_activity = tags_activity.sort_values(by=['authorid'])
    tags_activity = tags_activity.reset_index(drop=True)
    
    print(activity,'join complete!')
    return tags_activity

# Analysis ---------------------------------------------------------------------

def getTagSummary(postUserSurvey, brand=False):
    if brand:
        TF=[]
        for i in range(len(postUserSurvey)):
            my_tag = postUserSurvey['name'][i]
            if my_tag[:len(brand)]==brand:
                TF.append(True)
            else:
                TF.append(False)
        postUserSurvey=postUserSurvey.iloc[TF,:]
    
    
    
    # 해당 브랜드 관련 posting 한 user의 중복 제거!!
    postUserSurvey = postUserSurvey.drop_duplicates(subset='userid')
    postUserSurvey = postUserSurvey.drop(columns=['userid','postid','name'])
    # 여기서 원하는 속성 선택하는거야!
    # 어떤 속성??
    
    # sort int,str impossible <<<<<<<<<<<< ???
    summary = postUserSurvey.apply(pd.value_counts)
    return summary

def dequote(string):
    if len(string)<=1:
        return string
    if string[0] in ['"',"'"]:
        string = string[1:]
    if string[-1] in ['"',"'"]:
        string = string[:-1]
    return string
    
def age_result(mydata, col):
    result_dic = {}
    bins = range(max(mydata.index)+1)
    cnt=0
    for b in bins:
        if mydata.index[cnt]==b:
            result_dic[b]=mydata.iloc[cnt]
            cnt+=1
        else:
            result_dic[b]=0
    
    age_range = 5
    result_keys = []
    result_values = [0] * (len(result_dic) // age_range + 1)
    for i, value in enumerate(result_dic.values()):
        if i % age_range==0:
            result_keys.append('%d - %d' % (i,i+age_range-1))
        result_values[i//age_range]+=value



    result_dic = {}
    for i in range(len(result_values)):
        result_dic[result_keys[i]]=result_values[i]


    return result_dic

def skingender_result(mydata, col):
    result_dic = {}
    labels = mydata.index
    sizes = mydata
    for i, label in enumerate(labels):
        result_dic[label] = sizes[i]
        
    return result_dic


def survey_result(mydata, col):
    labels=[]
    for n, index in enumerate(mydata.index):
        index = index[1:-1]
        index = index.split('","') * int( mydata[n] )
        for item in index:
            item = dequote(item)
            labels.append(item)
    counter = Counter(labels)
    return dict(counter.most_common())


def ignoreSmall(result, mydata):
    larger = {}
    smaller= {'기타':0}
    for key,value in result.items():
        if value < sum(result.values()) * max(0.02, 1/int(sum(mydata))):
            smaller['기타'] += value
        else:
            larger[key] = value
    result=larger
    if smaller['기타']>0:
        result.update(smaller)
        
        
    return result

def drawPie(result):
    fig, ax1 = plt.subplots()
    ax1.pie(result.values(), labels=result.keys(), autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    return fig, ax1

def result_brand(brand, brandname, survey_questions, topN = 10):
    for col in brand.columns:
        mydata = brand[col]
        mydata = mydata.dropna()
        mydata = mydata.sort_index()

        # 성별
        if col=='age':
            result = age_result(mydata, col)
            result = ignoreSmall(result, mydata)
            fig, ax1 = drawPie(result)            
            

        # skinTone, Type, Gender
        elif col in ['skinTone','skinType','gender']:
            result = skingender_result(mydata, col)
            fig, ax1 = drawPie(result)            
        # skinConcerns
        elif col =='skinConcerns':
            result = survey_result(mydata, col)
            fig, ax1 = drawPie(result)            
        
        # survey
        else:
            result = survey_result(mydata, col)
            result = ignoreSmall(result, mydata)
            fig, ax1 = drawPie(result)            
            for i, question in enumerate(survey_questions['questionId (S)']):
                if col==question:
                    col = col + ' : ' + survey_questions['description (S)'][i]
                    break
                    
        plt.title((brandname+' '+col).upper())
        
        print('-*'*15)
        print('ASK =>', col)
        print('유저 수 =>', int(sum(mydata)))
        print('답변 수(중복포함) =>',int(sum(result.values())))
        
        # See Top 5 result
        topNresult = dict(Counter(result).most_common(5))
        for key, value in topNresult.items():
            topNresult[key] = '%0.1f' % float(value / sum(result.values())*100)
        print('Top %d =>' % min(5, len(result)), topNresult)
        
            
        while False:
            plt.savefig(dir_output+brandname+col+'.png')
            with open(brandname+'.csv', 'a') as f:  # Just use 'w' mode in 3.x
                w = csv.writer(f)
                w.writerow(result.keys())
                w.writerow(result.values())
        plt.show()
        
        
