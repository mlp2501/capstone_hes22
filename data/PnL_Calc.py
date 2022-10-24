
# coding: utf-8

# ## PnL and Performance Metrix Calculation Sctipt

# In[3]:


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def PnL(position_table, return_table, points_table, number_of_pairs, return_method = 0, long_short_only = 0):
    
    # Result tables and Performance Metrix
    PnL_Table = position_table * return_table.T - position_table * points_table.T
    PnL_Table = PnL_Table.dropna(axis = 'columns', how = 'all')
    if return_method == 0:
        PnL_Accum_Table = PnL_Table.cumsum(axis = 1)
    if return_method == 1:
        PnL_Accum_Table = PnL_Table + 1
        PnL_Accum_Table = PnL_Accum_Table.cumprod(axis = 1) - 1
        PnL_Accum_Table = PnL_Accum_Table.T.fillna(method='ffill').T
    PnL_Vol = PnL_Table.sum().std()
    Sharp_Ratio = PnL_Table.sum().mean() / PnL_Vol
    
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
    
    
    # Max Drawdown
    Max_drawdown = 0
    for i in range(len(PnL_Accum_Table.sum())):
        max_diff = PnL_Accum_Table.sum()[i] - PnL_Accum_Table.sum()[i+1:].min()
        if max_diff > Max_drawdown:
            Max_drawdown = max_diff
    
    # Annulized return
    year_ret = (PnL_Accum_Table.sum()[-1]/len(PnL_Accum_Table.sum())) * (12**0.5)
    
    return PnL_Table, PnL_Accum_Table, PnL_Vol, Sharp_Ratio, long_short_df, Max_drawdown, year_ret

