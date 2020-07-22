import pandas as pd
import itertools as it
import numpy as np


#data open using pandas type Dataframe
df_standard = pd.read_csv ('./sample_csv/fd_basic_F.csv', encoding = 'cp949')
df_to_add = pd.read_csv ('./sample_csv/fd_2018_F.csv', encoding = 'cp949')

#extract_index_code_from_standard_data
index_code_standard=df_standard.drop_duplicates(['code'],keep='first')
index_list = index_code_standard.code.tolist()

#check_matched_data_sorting_function_by_df_to_add
def test_fu_only(code, standard_data, new_data):
    
    #Extract key value from df_to_add
    df_to_add_key = new_data[['Unnamed: 0','y2017','y2018']]

    #df_to_add_listing
    to_add_list =[]
    for i in range(len(new_data)):
        test_index = df_to_add_key.iloc[i,0]
        data_2017 = df_to_add_key.iloc[i,1]
        data_2018 = df_to_add_key.iloc[i,2]
        to_add_list.append([test_index, data_2017, data_2018])

    #df_standard_listing
    standard_list = []
    for i in range(len(standard_data)):
        index_data_2017 = standard_data.iloc[i,6]
        standard_list.append(index_data_2017)
    
    #merge data
    exist_2017=[]
    for i in range(len(standard_list)):
        for j in range(len(to_add_list)):
            index_data = to_add_list[j][1]
            if index_data == standard_list[i] : exist_2017.append(to_add_list[j][0])
    sorting_list=[]
    for i in exist_2017:
        if i not in sorting_list :sorting_list.append(i)    
    
    return sorting_list

#produce_function
test_dummys=[]
for i in range(len(index_list)):
    temp_standard =df_standard[df_standard['code']==index_list[i]]
    temp_new =df_to_add[df_to_add['code']==index_list[i]]
    exist_2017_data = test_fu_only(index_list,temp_standard,temp_new)
    test_dummys.append(exist_2017_data)

#data_conversion    
to_except_datas=list(it.chain(*test_dummys))
to_except_datas_nondouble=np.array(to_except_datas).flatten().tolist()
to_except_datas_nondouble.sort()
to_except_datas_nondouble.reverse()

#extract_total_index and remove_matched_data
total_index = df_to_add.index.tolist()

for to_except_list in to_except_datas_nondouble:
    total_index.remove(to_except_list)

#take_DataFrame
non_match_data = df_to_add.loc[total_index,:]
non_match_data.to_excel("./Hello_Heo_Ssam_exception.xlsx")

