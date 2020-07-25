import pandas as pd
import itertools as it
import numpy as np
import sys
import getopt

args = sys.argv[1:]
opts, args = getopt.getopt(args, "s:t:r:h")

# Basic parameters

stn_opt = './sample_csv/df_2017_stn.csv'
trg_opt = './sample_csv/df_2018_trg.csv'
stn_year = str(2017)
trg_year = str(2018)
test_code = "None"

for opt, arg in opts:
    if opt == "-s":
        stn_year=str(arg)
        stn_opt = './sample_csv/' + 'df_' + stn_year +'_stn' + '.csv'  
    elif opt == "-t":
        trg_year=str(arg)
        trg_opt = './sample_csv/' + 'df_' + trg_year +'_trg' + '.csv' 
    elif opt == "-r":
        test_code = int(float(arg))
    elif opt == "-h":
        print("-s : standard data year ,built in year 2017")
        print("-t : merge target data year ,built in year 2018")
        print("-r : A company code from KS")
        sys.exit(1)



#data_open_using_pandas_type_Dataframe

df_standard = pd.read_csv (stn_opt, encoding = 'cp949')
df_to_add = pd.read_csv (trg_opt, encoding = 'cp949')


# check_the_test_code
if type(test_code) == int : 
    index_list = [test_code] 
    stn_opt == './sample_csv/df_2017_stn.csv' 
    trg_opt == './sample_csv/df_2018_trg.csv'
elif test_code == "None":
    if stn_opt == './sample_csv/df_2017_stn.csv' and trg_opt == './sample_csv/df_2018_trg.csv':
        while True:
                think_test_basic = str(input('Start this program with standard_2017 and target_2018 large data? [Y/N]'))
                if think_test_basic == 'Y':
                    index_code_standard=df_standard.drop_duplicates(['code'],keep='first')
                    index_list = index_code_standard.code.tolist()
                elif think_test_basic =='N':
                    exit()
    elif stn_opt == './sample_csv/' + 'df_' + stn_year +'_stn' + '.csv' and trg_opt == './sample_csv/' + 'df_' + trg_year +'_trg' + '.csv'  :
        while True:
            data_check_test = str(input('Start this program with standard_%s and target_%s large data? [Y/N]'%(stn_year,trg_year)))
            if data_check_test =='Y':
                index_code_standard=df_standard.drop_duplicates(['code'],keep='first')
                index_list = index_code_standard.code.tolist()
            elif data_check_test =='N' :
                exit()






def merge_func(code, standard_data, new_data):
    
    #Extract_key_value_from df_to_add
    df_to_add_key = new_data[['y%s'%stn_year,'y%s'%trg_year]]

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

#check_matched_data_sorting_function_by_df_to_add
def exception_func(code, standard_data, new_data):
    #Extract key value from df_to_add
    df_to_add_key = new_data[['Unnamed: 0','y%s'%stn_year,'y%s'%trg_year]]

    #df_to_add_listing
    to_add_list =[]
    for i in range(len(new_data)):
        indexing = df_to_add_key.iloc[i,0]
        data_2017 = df_to_add_key.iloc[i,1]
        data_2018 = df_to_add_key.iloc[i,2]
        to_add_list.append([indexing, data_2017, data_2018])

    #df_standard_listing
    standard_list = []
    for i in range(len(standard_data)):
        index_data_2017 = standard_data.iloc[i,6]
        standard_list.append(index_data_2017)
    
    #merge_data
    exist_2017=[]
    for i in range(len(standard_list)):
        for j in range(len(to_add_list)):
            index_data = to_add_list[j][1]
            if index_data == standard_list[i] : exist_2017.append(to_add_list[j][0])
    
    sorting_list=[]
    for i in exist_2017:
        if i not in sorting_list :sorting_list.append(i)    
   
    return sorting_list


### merging_func

#tracking_data_index_code
test_dummys=[]
for i in range(len(index_list)):
    temp_standard =df_standard[df_standard['code']==index_list[i]]
    temp_new =df_to_add[df_to_add['code']==index_list[i]]
    test_data = merge_func(index_list,temp_standard,temp_new)
    test_dummys.append(test_data)


#take_DataFrame
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
df_merge = pd.DataFrame({'Unnamed: 0':indexs,'y%s'%trg_year:y2018s})
merged_inner = pd.merge(left=df_standard, right=df_merge, left_on='Unnamed: 0', right_on='Unnamed: 0')
del merged_inner['y%s_x'%trg_year]
#merged_inner.columns = ['Unnamed: 0','code','code_a','company','item','item_name','y2017','y2018']
merged_inner.rename(columns = {'y%s_y'%trg_year : 'y%s'%trg_year}, inplace=True)

### tracking_unmatched_data

#produce_function_appending_code
test_dummys_except=[]
for i in range(len(index_list)):
    temp_standard =df_standard[df_standard['code']==index_list[i]]
    temp_new =df_to_add[df_to_add['code']==index_list[i]]
    exist_2017_data = exception_func(index_list,temp_standard,temp_new)
    test_dummys_except.append(exist_2017_data)

#data_conversion    
to_except_datas=list(it.chain(*test_dummys_except))
to_except_datas_nondouble=np.array(to_except_datas).flatten().tolist()
to_except_datas_nondouble.sort()
to_except_datas_nondouble.reverse()

#extract_total_index and remove_matched_data
total_index = df_to_add.index.tolist()

for to_except_list in to_except_datas_nondouble:
    total_index.remove(to_except_list)
non_match_data = df_to_add.loc[total_index,:]

#extract_csv
merged_inner.to_excel("./df_%s_stn.xlsx"%trg_year)
non_match_data.to_excel("./df_%s_exception.xlsx"%trg_year)
