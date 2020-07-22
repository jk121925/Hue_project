import pandas as pd

#data open using pandas type Dataframe
df_standard = pd.read_csv ('fd_origin.csv', encoding = 'cp949')
df_to_add = pd.read_csv ('fd_2018_5.csv', encoding = 'cp949')

#df_samsung_0 = df_standard[df_standard['code']==5930]
#df_samsung_1 = df_to_add[df_to_add['code']==5930]

#Extract key value from df_to_add
df_to_add_key = df_to_add[['y2017','y2018']]

#df_to_add_listing
df_to_add_list =[]
for i in range(len(df_to_add)):
    data_2017 = df_to_add_key.iloc[i,0]
    data_2018 = df_to_add_key.iloc[i,1]
    df_to_add_list.append([data_2017,data_2018])

#df_standard_listing
df_standard_list = []
for i in range(len(df_standard)):
    index_data_2017 = df_standard.iloc[i,7]
    df_standard_list.append(index_data_2017)

#merge data
for i in range(len(df_standard_list)):
    for j in range(len(df_to_add_list)):
        index_data = df_standard_list[i]
        if index_data == df_to_add_list[j][0] : df_standard_list[i] = [index_data, df_to_add_list[j][1]]
for i in range(len(df_standard_list)):
    non_data = df_standard_list[i]
    if type(df_standard_list[i]) != list : df_standard_list[i] = [non_data,0]

# setting with copy warning
df_dummy = df_standard.copy()

# merge data using df_standard
for i in range(len(df_standard)):
    origin_index = df_standard.iloc[i,7]
    refer_index = df_standard.iloc[i,8]
    for j in range(len(df_standard_list)):
        match_index = df_standard_list[j][0]
        new_index = df_standard_list[j][1]
        if origin_index == match_index and df_standard.iloc[i,4] != 'SCF':  df_dummy.iloc[i,8] = new_index
        elif origin_index == match_index and df_standard.iloc[i,4] == 'SCF':  df_dummy.iloc[i,8] = refer_index

df_dummy