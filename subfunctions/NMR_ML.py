def merge_excel(input_filename,sheetname_list,output_filename='merge_log.csv',depth_name='DEPTH(m)'):
    '''
        
    '''
    import pandas as pd
    
    rawdata = dict()
    # read all excel files
    for sheetname in sheetname_list:
        rawdata[sheetname] = pd.read_excel(input_filename,sheetname=sheetname)
    
    # get the min_depth and max_depth 
    min_depth = max([rawdata[elem][depth_name][0]   for elem in rawdata])
    max_depth = min([rawdata[elem][depth_name][len(rawdata[elem])-1]   for elem in rawdata])
    print('mindepth ',min_depth,'max depth ',max_depth)
    
    # data cleaning, select data between min and max depth
    for elem in rawdata:
    #print(elem,'  raw length',len(rawdata[elem]))
        rawdata[elem] =rawdata[elem][(rawdata[elem][depth_name]<= max_depth) & (rawdata[elem][depth_name] >= min_depth) ] #
        rawdata[elem]=rawdata[elem].reset_index()    #del rawdata[elem]['index']
        del rawdata[elem]['index']
    #print(elem,'  processed length',len(rawdata[elem]))
    
    # merge to single dataframe 
    df_logs_merge = pd.DataFrame()
    for i,elem in enumerate(rawdata):
        columns = list(rawdata[elem].columns.values) 
        print(columns)
        if i>0: # only select depth once
            columns.remove(depth_name)
        df_logs_merge[columns] = rawdata[elem][columns]
    # save to csv file
    df_logs_merge.to_csv(output_filename,index=False)
    print('merge excel finished')