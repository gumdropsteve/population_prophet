import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

# default cleaning method until proven otherwise
def clean_census_frame(csv_path , head=False , reset=True , set_index=False ):
    '''
    inputs) 
        >> csv_path
            > path to csv
        >> head
            > default=False
                >> if != False
                    > integer
                        >> returns the first {head} rows (using .head() method) 
                            > instead of enitre dataframe
        >> reset
            > default=True
                >> resets index after taking out rows
            > if set to False
                >> will not reset index
        >> set_index
            > default=False
            > if != False
                >> will set_index of new df to set_index
    output)
        >> dataframe cleaned like 2000 Census age&sex by 5-digit Zip Code (also how 2010 for same is cleaned)
    how)
        1. reads in csv , assumes it's large
        2. makes a copy for editing 
            > and potential future use
        3. locates readable column names  and non-readable names 
            > readable
                    > e.g. Estimate; SEX AND AGE - Total population
                >> assumes they are currently in row 0
            > non-readable
                    > e.g. HC01_VC03
                >> assumes they are currently == dataframe.columns
        4. replaces dataframe.columns (non-readable) with readable column names
            > and drops the old 0th column (column where readable names were stored)
        
    '''
    # load data
    df = pd.read_csv( csv_path , low_memory=False )

    # and copy
    _df = df.copy()

    # reset column names to current 0th row values
    _df.columns = _df.iloc[0]
    # new 2000 dataframe without row where values are from
    clean_df = _df[1:]
    
    # default
    if reset==True:
        # reset index
        clean_df = clean_df.reset_index()
        
    # set_index
    if set_index:
        clean_df = clean_df.set_index(set_index)
    
    if head:
        # return first {head} rows of dataframe
        return clean_df.head(head)
    else:
        # return dataframe
        return clean_df
    
def test_non_unique(column_names):
    '''
    input) 
        >> list of column names {column_names}
            > columns to check for duplicate instances
    output)
        >> indexed list of names occouring more than once 
    '''
    # store first instance
    first_occour = []
    # store 2nd+ instance(s)
    non_unique = []
    # we're going to want index
    for i,_ in enumerate(column_names):
        # not first time
        if _ not in first_occour:
            first_occour.append(_)
        # if not first, tag&bag
        else:
            non_unique.append([i,_])
    # output index w/ non-first instances
    return non_unique


def bring_the_5yr_acs_2k11_thru_2k17():
    '''
    inputs)
        >> list_of_paths
            > paths to each raw dataframe
    output)
        >> list of modified dataframes
    function)
        1. load and copy data
        2. 
    '''
    # load 2011 
    y2k11 = clean_census_frame('../data/acs/aff_download/ACS_11_5YR_DP05_with_ann.csv',reset=False)
    # copy
    y11 = y2k11.copy()
    # 2012
    y2k12 = clean_census_frame('../data/acs/aff_download/ACS_12_5YR_DP05_with_ann.csv',reset=False)
    y12 = y2k12.copy()
    #2013
    y2k13 = clean_census_frame('../data/acs/aff_download/ACS_13_5YR_DP05_with_ann.csv',reset=False)
    y13 = y2k13.copy()
    # 2014
    y2k14 = clean_census_frame('../data/acs/aff_download/ACS_14_5YR_DP05_with_ann.csv',reset=False)
    y14 = y2k14.copy()
    # 2015
    y2k15 = clean_census_frame('../data/acs/aff_download/ACS_15_5YR_DP05_with_ann.csv',reset=False)
    y15 = y2k15.copy()
    #2016
    y2k16 = clean_census_frame('../data/acs/aff_download/ACS_16_5YR_DP05_with_ann.csv',reset=False)
    y16 = y2k16.copy()
    #2017
    y2k17 = clean_census_frame('../data/acs/aff_download/ACS_17_5YR_DP05_with_ann.csv',reset=False)
    y17 = y2k17.copy()

    '''identify columns'''
    # 2011
    tags11 = y11.columns  
    # 2012
    tags12 = y12.columns  
    #2013
    tags13 = y13.columns  
    # 2014
    tags14 = y14.columns  
    # 2015
    tags15 = y15.columns  
    #2016
    tags16 = y16.columns  
    # 2017
    tags17 = y17.columns 

    '''identify common columns'''
    # collection of columns appearing in all 7 dataframes 2011-2017
    common_tags = [tag for tag in tags17 if tag in tags11 & tags12 & tags13 & tags14 & tags15 & tags16]

    '''identify non common columns for specific frames'''
    # 2011
    uncommon_11 = [tag for tag in y11.columns if tag not in common_tags]
    # 2012
    uncommon_12 = [tag for tag in y12.columns if tag not in common_tags]
    # 2013
    uncommon_13 = [tag for tag in y13.columns if tag not in common_tags]
    # 2014
    uncommon_14 = [tag for tag in y14.columns if tag not in common_tags]
    # 2015
    uncommon_15 = [tag for tag in y15.columns if tag not in common_tags]
    # 2016
    uncommon_16 = [tag for tag in y16.columns if tag not in common_tags]
    # 2017
    uncommon_17 = [tag for tag in y17.columns if tag not in common_tags]

    """drop each frame's uncommon columns, reset index"""
    # 2011
    y11 = y11.drop(uncommon_11,axis=1).reset_index()
    # # 2012
    y12 = y12.drop(uncommon_12,axis=1).reset_index()
    # # 2013
    y13 = y13.drop(uncommon_13,axis=1).reset_index()
    # # 2014
    y14 = y14.drop(uncommon_14,axis=1).reset_index()
    # # 2015
    y15 = y15.drop(uncommon_15,axis=1).reset_index()
    # # 2016
    y16 = y16.drop(uncommon_16,axis=1).reset_index()
    # # 2017
    y17 = y17.drop(uncommon_17,axis=1).reset_index()
    
    """don't forget, 2011 and 2012 have extra repeats, check for non-unique column instances in new dfs"""
    # 2011
    a=test_non_unique(y11.columns)
    # 2012
    b=test_non_unique(y12.columns)
    # 2013
    c=test_non_unique(y13.columns)
    # 2014
    d=test_non_unique(y14.columns)
    # 2015
    e=test_non_unique(y15.columns)
    # 2016
    f=test_non_unique(y16.columns)
    # 2017
    g=test_non_unique(y17.columns)

    # collection of all repeats which occour in all 7 dataframes (len==8)
    common_repeats = [_ for _ in g if _ in a and b and c and d and e and f]
    """[[80, 'Estimate; SEX AND AGE - 18 years and over'],
    [81, 'Margin of Error; SEX AND AGE - 18 years and over'],
    [82, 'Percent; SEX AND AGE - 18 years and over'],
    [83, 'Percent Margin of Error; SEX AND AGE - 18 years and over'],
    [84, 'Estimate; SEX AND AGE - 65 years and over'],
    [85, 'Margin of Error; SEX AND AGE - 65 years and over'],
    [86, 'Percent; SEX AND AGE - 65 years and over'],
    [87, 'Percent Margin of Error; SEX AND AGE - 65 years and over']]"""
    
    # identify repeats occouring only in 2011 and 2012 (already checked are not unique to self)
    first_two_only = [i for i in a if i not in common_repeats and i in b]

    instances = [100,101,102,103,188,189,190,191]
    # adjust 2011
    y11 = y11.drop(y11.columns[instances], axis=1)
    # adjust 2012
    y12 = y12.drop(y12.columns[instances], axis=1)

    
    return common_repeats,first_two_only  # [y11,y12,y13,y14,y15,y16,y17]