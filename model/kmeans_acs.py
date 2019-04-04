import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split

"""
STEP 0 
>> imports; def clean_census & other functions
"""

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

'''
STEP 1 
>> load data, reset; make copies/**sample
'''

def load_clean_frames(i=0,n=False):
    '''
    function) loads data
    
    input)
        >> i
            > if 0
                >> .reset_index() after deleting row contining column names
            > if 1
                >> do not .reset_index()
        >> head
            > default=False (ignore)
            > if != False
                >> must be int
                    > dataframe = dataframe.head(n)
    '''
    if i==0:
        # load with reset
        # 2011 
        twenty_eleven = clean_census_frame('../../data/American_Community_Survey/aff_download/ACS_11_5YR_DP05_with_ann.csv')
        # 2012
        twenty_twelve = clean_census_frame('../../data/American_Community_Survey/aff_download/ACS_12_5YR_DP05_with_ann.csv')
        #2013
        twenty_thirteen = clean_census_frame('../../data/American_Community_Survey/aff_download/ACS_13_5YR_DP05_with_ann.csv')
        # 2014
        twenty_fourteen = clean_census_frame('../../data/American_Community_Survey/aff_download/ACS_14_5YR_DP05_with_ann.csv')
        # 2015
        twenty_fifteen = clean_census_frame('../../data/American_Community_Survey/aff_download/ACS_15_5YR_DP05_with_ann.csv')
        #2016
        twenty_sixteen = clean_census_frame('../../data/American_Community_Survey/aff_download/ACS_16_5YR_DP05_with_ann.csv')
        #2017
        twenty_seventeen = clean_census_frame('../../data/American_Community_Survey/aff_download/ACS_17_5YR_DP05_with_ann.csv')
    if i==1:
        # load without reset
        # 2011 
        twenty_eleven = clean_census_frame('../../data/American_Community_Survey/aff_download/ACS_11_5YR_DP05_with_ann.csv',reset=False)
        # 2012
        twenty_twelve = clean_census_frame('../../data/American_Community_Survey/aff_download/ACS_12_5YR_DP05_with_ann.csv',reset=False)
        #2013
        twenty_thirteen = clean_census_frame('../../data/American_Community_Survey/aff_download/ACS_13_5YR_DP05_with_ann.csv',reset=False)
        # 2014
        twenty_fourteen = clean_census_frame('../../data/American_Community_Survey/aff_download/ACS_14_5YR_DP05_with_ann.csv',reset=False)
        # 2015
        twenty_fifteen = clean_census_frame('../../data/American_Community_Survey/aff_download/ACS_15_5YR_DP05_with_ann.csv',reset=False)
        #2016
        twenty_sixteen = clean_census_frame('../../data/American_Community_Survey/aff_download/ACS_16_5YR_DP05_with_ann.csv',reset=False)
        #2017
        twenty_seventeen = clean_census_frame('../../data/American_Community_Survey/aff_download/ACS_17_5YR_DP05_with_ann.csv',reset=False)
    
    # default
    if n==False:
        # copy 
        # 2011 
        _y2k11 = twenty_eleven.copy()
        # 2012
        _y2k12 = twenty_twelve.copy()
        #2013
        _y2k13 = twenty_thirteen.copy()
        # 2014
        _y2k14 = twenty_fourteen.copy()
        # 2015
        _y2k15 = twenty_fifteen.copy()
        #2016
        _y2k16 = twenty_sixteen.copy()
        #2017
        _y2k17 = twenty_seventeen.copy()
        
    # non default, want only first n rows
    if n:
        # adjust frames to .head(n) 
        # 2011 
        _y2k11 = twenty_eleven.copy().head(n)
        # 2012
        _y2k12 = twenty_twelve.copy().head(n)
        #2013
        _y2k13 = twenty_thirteen.copy().head(n)
        # 2014
        _y2k14 = twenty_fourteen.copy().head(n)
        # 2015
        _y2k15 = twenty_fifteen.copy().head(n)
        #2016
        _y2k16 = twenty_sixteen.copy().head(n)
        #2017
        _y2k17 = twenty_seventeen.copy().head(n)
    
    # output list of copied frames
    return [_y2k11,_y2k12,_y2k13,_y2k14,_y2k15,_y2k16,_y2k17]

'''
STEP 2 
>> identify unique (mostly used in testing); 
>> convert DataFrame to numeric; convert Geography (Zip Codes) && Ids
'''

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


def to_numeric_but(dataframe,save_these_columns='none'):
    '''
    split into 2 df and rejoin after convert to int
    
    inputs:
        >> save_these_columns=number of columns to save
            > currently must include one end of df 
                >> might could run function multiple times to edit slices
                >> single number, not range (yet)
                    > if 'none', saves no columns
        >> dataframe
            > dataframe to shif to numeric (but)
    output:
        >> concatted pd.DataFrame of 
            > og columns you chose to save
            > columns converted to numeric
    '''
    # copy df for editing
    k = dataframe.copy()
    
    # split
    if save_these_columns != 'none':
        # columns to save
        save_k = k[k.columns[:save_these_columns]]
        # columns to edit
        switch_k = k[k.columns[save_these_columns:]]
    # don't split
    else:
        # k as is
        switch_k = k

    # edited columns  # coerce , ignore , raise
    swapped_k = switch_k.apply(pd.to_numeric, errors='coerce')
    
    # check saving columns
    if save_these_columns != 'none':
        # new (edited) dataframe (ogsave|swapped)
        new_k = pd.concat( [save_k,swapped_k] ,axis=1 )
    else:
        new_k = swapped_k

    return new_k


def geography_to_zipcode_ids_to_numeric(dataframe):
    '''
    convert 
        >> .Geography values 
            > like 'ZCTA5 00601' 
            > to int(00601)
        >> .Id values
            > like '8600000US00601' 
            > to int(860000000601)
        >> .Id2 values
            > like '00601'
            > to int(00601)
    '''
    # copy
    df = dataframe.copy()
    
    # set old Geography
    geo = df.Geography
    # set old Id
    _id = df.Id
    # set old Id2
    __id2 = df.Id2
    
    # make new 'Geography' values
    new_geos = [int(i[-5:]) for i in geo]
    # new 'Id' values
    new_id = [int(''.join(i.split('US'))) for i in _id]
    # new .Id2 instances
    new__id2 = [int(d) for d in __id2]
    
    # convert dataframe
    new_df = df.copy()
    new_df.Geography = new_geos
    new_df.Id = new_id
    new_df.Id2 = new__id2
    
    # return new df
    return new_df

'''
STEP 3
>> run KMeans on dataframe
'''

def kmeans_by(dataframe,n_clusters=10,converted=False):
    '''
    inputs:
        >> dataframe
            > dataframe to be edited
        >> n_clusters 
            > default = 10
            > number of clusters for KMeans
        >> converted
            > default = False
            > assumes data is not ready for KMeans 
                >> if True, assumes df is ready for KMeans
    output:
        > pd.Dataframe of 
    '''
    # copy data 
    d = dataframe.copy()  
    
    '''df conversion'''
    # default
    if converted!=True:
        # copy data for editing
        _data_ = d.copy()
        
        # convert first 3 columns ('Id', 'Id2', 'Geography')
        _data = geography_to_zipcode_ids_to_numeric(dataframe=_data_)
        
        # convert remainder of dataframe
        data = to_numeric_but(save_these_columns='none', dataframe=_data)

    # dataframe has already been converted / otherwise
    
    '''KMeans'''
    # fill NaN values
    t = d.copy().fillna(0)
    
    # convert DataFrame to matrix
    mat = t.values
    
    # sklearn
    '''source: https://bit.ly/2I7OekQ
    n_clusters : int, optional, default: 8
    The number of clusters to form as well as the number of centroids to generate.
    n_jobs : int or None, optional (default=None)
        The number of jobs to use for the computation. This works by computing
        each of the n_init runs in parallel.'''
    km = KMeans(n_clusters,max_iter=1000.n_jobs=2)
    # fit our matrix
    km.fit(mat)
    
    # cluster assignment tags
    labels = km.labels_
    
    # out as a DataFrame
    results = pd.DataFrame([t.index,labels]).T

    # display out
    return results


if __name__ == '__main__':
    # load first 10,000 rows w/o reset
    f = load_clean_frames( i=1 , n=1000 )

    # store out
    out = []
    
    # run kmeans on each dataframe
    for i in range(len(f)):
        z = kmeans_by( dataframe=f[i] , n_clusters=10 )
        # store the output in out
        out.append(z)
        
    return out