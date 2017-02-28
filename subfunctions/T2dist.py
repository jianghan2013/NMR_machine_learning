import numpy as np
import pandas as pd

def get_weight_mean_t2(x_t2,y_t2):
    # mean = sum(x*weight)/sum(weight)
    return np.dot(y_t2,x_t2)/sum(y_t2) # weight average for x
	
def get_std_t2(x,x_mean):
    return np.sqrt( np.dot(x-x_mean,x-x_mean)/(len(x)-1))
	
def get_mean_std(x_t2,y_t2):
    '''
    combine get_weight_mean_t2 and get_std_t2 to process vector x_t2 and  y_t2
    '''
    mean_x_t2 = get_weight_mean_t2(x_t2,y_t2)
    std_x_t2 = get_std_t2(x_t2,mean_x_t2)
    return mean_x_t2,std_x_t2

def get_mean_std_from_df(x_t2_1d,y_t2_2d):
    '''
    using get_mean_std to process NMR t2 in dataframe
    '''
    n_row = len(y_t2_2d)
    mean_log10_t2 = np.zeros(n_row)
    std_log10_t2 = np.zeros(n_row)
    
    for i in range(n_row):
        mean_log10_t2[i],std_log10_t2[i] = get_mean_std(x_t2_1d,y_t2_2d[i])
    
    return {'t2_mean_log10':mean_log10_t2,'t2_std_log10':std_log10_t2}
	
##get_mean_std(np.array([1,2,3]),np.array([7,9,6])) ## (1.9545454545454546, 0.81776083445537184)

def t2_dist_process(df_t2_dist):
    '''
    using get_mean_std_from_df to create mean and std in dataframe
    '''
    # get t2 dist in x direction
    t2_x = list(df_t2_dist.columns.values[1:]) 
    t2_x_log10 =np.log10(t2_x)
    t2_y = np.array(df_t2_dist.iloc[:,1:])
    # calculate the stats of the nmr t2 distribution
    result = get_mean_std_from_df(t2_x_log10,t2_y)
    df_t2_dist_stats = pd.DataFrame(result)
    df_t2_dist_stats['DEPTH(m)'] = df_t2_dist['DEPTH(m)']
    print(df_t2_dist_stats.loc[0]) #  
    print('test: mean 1.596769, std 0.961485')
    return df_t2_dist_stats