import pandas as pd

#data open using pandas type Dataframe
df_standard = pd.read_csv ('../sample_csv/df_2017_stn.csv', encoding = 'cp949')
df_to_add = pd.read_csv ('../sample_csv/df_2018_trg.csv', encoding = 'cp949')

#extract_index_code_from_standard_data
index_code_standard=df_standard.drop_duplicates(['code'],keep='first')
index_list = index_code_standard.code.tolist()

def test_fu_only(code, standard_data, new_data):
    
    #Extract key value from df_to_add
    df_to_add_key = new_data[['y2017','y2018']]

    #df_to_add_listing
    to_add_list =[]
    for i in range(len(new_data)):
        data_2017 = df_to_add_key.iloc[i,0]
        data_2018 = df_to_add_key.iloc[i,1]
        to_add_list.append([data_2017,data_2018])

    #df_standard_listing
    standard_list = []
    for i in range(len(standard_data)):
        index_data_2017 = standard_data.iloc[i,6]
        standard_list.append(index_data_2017)

    #merge data
    for i in range(len(standard_list)):
        for j in range(len(to_add_list)):
            index_data = standard_list[i]
            if index_data == '0' :  standard_list[i] = [index_data,0]
            elif index_data == to_add_list[j][0] : standard_list[i] = [index_data, to_add_list[j][1]]

    #non data make 0    
    for i in range(len(standard_list)):
        non_data = standard_list[i]
        if type(standard_list[i]) != list : standard_list[i] = [non_data,0]

    #make index column
    for i in range(len(standard_list)):
        standard_list[i].insert(0,standard_data.iloc[i,0])
    
    #last_two_index_value
    standard_list[-1][2] = standard_data.iloc[-1,7]
    standard_list[-2][2] = standard_data.iloc[-2,7]
     
    return standard_list

test_dummys=[]
for i in range(len(index_list)):
    temp_standard =df_standard[df_standard['code']==index_list[i]]
    temp_new =df_to_add[df_to_add['code']==index_list[i]]
    test_data = test_fu_only(index_list,temp_standard,temp_new)
    test_dummys.append(test_data)

#df_origin_test=df_standard[df_standard['code'].isin([20,30,40])]

indexs=[] 
y2017s=[]
y2018s=[]
for test in test_dummys:
    for t in test:      
        index = t[0]
        y2017 = t[1]
        y2018 = t[2]
        indexs.append(index)
        y2017s.append(y2017)
        y2018s.append(y2018)
df_merge = pd.DataFrame({'Unnamed: 0':indexs,'y2018':y2018s})
merged_inner = pd.merge(left=df_standard, right=df_merge, left_on='Unnamed: 0', right_on='Unnamed: 0')

del merged_inner['y2018_x']
merged_inner.columns = ['Unnamed: 0','code','code_a','company','item','item_name','y2017','y2018']
merged_inner.to_excel("./Hello_Heo_Ssam_merged.xlsx")