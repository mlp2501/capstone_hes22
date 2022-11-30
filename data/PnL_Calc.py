
# coding: utf-8

# ## PnL and Performance Metrix Calculation Sctipt

# In[2]:


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def PnL(position_table, return_table, points_table, number_of_pairs, x_date, return_method = 0, long_short_only = 0):
    
    ########################### Whole Period Result ###################################################
    # Result tables and Performance Metrix
    PnL_Table = position_table * return_table.T - position_table * points_table.T
    PnL_Table = PnL_Table.dropna(axis = 'columns', how = 'all')
    if return_method == 0:
        PnL_Accum_Table = PnL_Table.cumsum(axis = 1)
    if return_method == 1:
        PnL_Accum_Table = PnL_Table + 1
        PnL_Accum_Table = PnL_Accum_Table.cumprod(axis = 1) - 1
        PnL_Accum_Table = PnL_Accum_Table.T.fillna(method='ffill').T
    PnL_Monthly_Vol = PnL_Table.sum().std()
    
    # Max Drawdown
    Max_drawdown = 0
    for i in range(len(PnL_Accum_Table.sum())):
        max_diff = PnL_Accum_Table.sum()[i] - PnL_Accum_Table.sum()[i+1:].min()
        if max_diff > Max_drawdown:
            Max_drawdown = max_diff
    
    # Annulized return
    year_ret = (PnL_Accum_Table.sum()[-1]/len(PnL_Accum_Table.sum())) * (12)
    
    # Annulized vol
    PnL_Annul_Vol = PnL_Monthly_Vol * (12**0.5)
    
    # Sharp Ratio = Annulized Ret / Annulized Vol
    Sharp_Ratio = year_ret / PnL_Annul_Vol
    
    Results_Summary = [PnL_Accum_Table.sum()[i], year_ret, PnL_Monthly_Vol, PnL_Annul_Vol, Sharp_Ratio,  Max_drawdown ]
    
    ########################### Training Period Result ###################################################
    # Result tables and Performance Metrix
    PnL_Table_Train = position_table.loc[:,:x_date] * return_table.loc[:x_date,:].T - position_table.loc[:,:x_date] * points_table.loc[:x_date,:].T
    PnL_Table_Train = PnL_Table_Train.dropna(axis = 'columns', how = 'all')
    if return_method == 0:
        PnL_Accum_Table_Train = PnL_Table_Train.cumsum(axis = 1)
    if return_method == 1:
        PnL_Accum_Table_Train = PnL_Table_Train + 1
        PnL_Accum_Table_Train = PnL_Accum_Table_Train.cumprod(axis = 1) - 1
        PnL_Accum_Table_Train = PnL_Accum_Table_Train.T.fillna(method='ffill').T
    PnL_Monthly_Vol_Train = PnL_Table_Train.sum().std()
    
    # Max Drawdown
    Max_drawdown_Train = 0
    for i in range(len(PnL_Accum_Table_Train.sum())):
        max_diff = PnL_Accum_Table_Train.sum()[i] - PnL_Accum_Table_Train.sum()[i+1:].min()
        if max_diff > Max_drawdown_Train:
            Max_drawdown_Train = max_diff
    
    # Annulized return
    year_ret_Train = (PnL_Accum_Table_Train.sum()[-1]/len(PnL_Accum_Table_Train.sum())) * (12)
    
    # Annulized vol
    PnL_Annul_Vol_Train = PnL_Monthly_Vol_Train * (12**0.5)
    
    # Sharp Ratio = Annulized Ret / Annulized Vol
    Sharp_Ratio_Train = year_ret_Train / PnL_Annul_Vol_Train
    
    Results_Summary_Train = [PnL_Accum_Table_Train.sum()[i], year_ret_Train, PnL_Monthly_Vol_Train, PnL_Annul_Vol_Train, Sharp_Ratio_Train,  Max_drawdown_Train ]
    
    ########################### Testing Period Result ###################################################
    # Result tables and Performance Metrix
    PnL_Table_Test = position_table.loc[:,x_date:] * return_table.loc[x_date:,:].T - position_table.loc[:,x_date:] * points_table.loc[x_date:,:].T
    PnL_Table_Test = PnL_Table_Test.dropna(axis = 'columns', how = 'all')
    if return_method == 0:
        PnL_Accum_Table_Test = PnL_Table_Test.cumsum(axis = 1)
    if return_method == 1:
        PnL_Accum_Table_Test = PnL_Table_Test + 1
        PnL_Accum_Table_Test = PnL_Accum_Table_Test.cumprod(axis = 1) - 1
        PnL_Accum_Table_Test = PnL_Accum_Table_Test.T.fillna(method='ffill').T
    PnL_Monthly_Vol_Test = PnL_Table_Test.sum().std()
    
    # Max Drawdown
    Max_drawdown_Test = 0
    for i in range(len(PnL_Accum_Table_Test.sum())):
        max_diff = PnL_Accum_Table_Test.sum()[i] - PnL_Accum_Table_Test.sum()[i+1:].min()
        if max_diff > Max_drawdown_Test:
            Max_drawdown_Test = max_diff
    
    # Annulized return
    year_ret_Test = (PnL_Accum_Table_Test.sum()[-1]/len(PnL_Accum_Table_Test.sum())) * (12)
    
    # Annulized vol
    PnL_Annul_Vol_Test = PnL_Monthly_Vol_Test * (12**0.5)
    
    # Sharp Ratio = Annulized Ret / Annulized Vol
    Sharp_Ratio_Test = year_ret_Test / PnL_Annul_Vol_Test
    
    Results_Summary_Test = [PnL_Accum_Table_Test.sum()[i], year_ret_Test, PnL_Monthly_Vol_Test, PnL_Annul_Vol_Test, Sharp_Ratio_Test,  Max_drawdown_Test ]
    
    ####################################################################################################
    
    metrics_name =['Accumulative Return', 'Annulized Return','Monthly Vol', 'Annulized Vol','Sharp Ratio','Max Drawdown']
    summary_df = pd.DataFrame(index = metrics_name)
    summary_df['Whole Period'] = Results_Summary
    summary_df['Train Period'] = Results_Summary_Train
    summary_df['Test Period'] = Results_Summary_Test
    
    ####################################################################################################
    
    # Long / Short ccy List
    #positions_new = position_table.droplevel(level = 1)
    short_list = []
    long_list = []
    for i in position_table.columns:
        short_ccy = position_table.loc[position_table[i] == -1].index
        long_ccy = position_table.loc[position_table[i] == 1].index
        short_list.append(short_ccy)
        long_list.append(long_ccy)
    if long_short_only == 0:
        short_df = pd.DataFrame(short_list, columns = ['Short'] * number_of_pairs, index = position_table.columns)
        long_df = pd.DataFrame(long_list, columns = ['Long'] * number_of_pairs, index = position_table.columns)
        long_short_df = short_df.join(long_df)
    if long_short_only == 1:
        long_short_df = pd.DataFrame(long_list, columns = ['Long'] * number_of_pairs, index = position_table.columns)
    if long_short_only == 2:
        long_short_df = pd.DataFrame(short_list, columns = ['Short'] * number_of_pairs, index = position_table.columns)
    
    
    
    
    return PnL_Table, PnL_Accum_Table, long_short_df, summary_df

