# master py file
import time
import numpy as np
import pandas as pd

def convert(a='../data/2000/age-groups-and-sex-census-DEC_00_SF1_QTP1/DEC_00_SF1_QTP1_with_ann.csv',
           b='../data/2010/age-groups-and-sex-census-DEC_10_SF1_QTP1/DEC_10_SF1_QTP1_with_ann.csv'):
    # load 2000 data
    y2k = pd.read_csv( a , low_memory=False )
    # load 2010 data
    y2k10 = pd.read_csv( b , low_memory=False )

    # 2000 Census
    b = y2k.copy()
    # 2010 Census
    o = y2k10.copy()

    # reset 2000 columns to current 0th row values
    b.columns = b.iloc[0]
    # new 2000 dataframe without row where values are from
    b = b[1:]
    # reset index
    b = b.reset_index()

    # reset 2010 columns to current 0th row values
    o.columns = o.iloc[0]
    # new 2010 dataframe without row where values are from
    o = o[1:]
    # reset index
    o = o.reset_index()

    # identify zip codes from 2000 .Geography (last 5 chars of string)
    zip_2000_codes = [q[-5:] for q in b.Geography]  # ValueError: invalid literal for int() with base 10: '006HH'
    # identify zip codes from 2010 .Geography (last 5 chars of string)
    zip_2010_codes = [q[-5:] for q in o.Geography]

    # from 2000.Geography , instance is not seen in 2010.Geography  -- sample: zip_code = (2, 'c')
    in_2000_but_not_2010_from_2000 = [zip_code for zip_code in enumerate(zip_2000_codes) if zip_code[1] not in zip_2010_codes]
    # from 2010.Geography , instance is not seen in 2000.Geography  -- sample: zip_code[1] = 'c'
    in_2010_but_not_2000_from_2010 = [zip_code for zip_code in enumerate(zip_2010_codes) if zip_code[1] not in zip_2000_codes]

    # from 2000.Geography , instance is seen in 2010.Geography
    in_2000_and_2010_from_2000 = [zip_code for zip_code in enumerate(zip_2000_codes) if zip_code[1] in zip_2010_codes]
    # from 2010.Geography , instance is seen in 2000.Geography
    in_2010_and_2000_from_2010 = [zip_code for zip_code in enumerate(zip_2010_codes) if zip_code[1] in zip_2000_codes]

    # index of objects coexisting in 2000 and 2010
    of_2000_indexes = [i for i,j in in_2000_and_2010_from_2000]
    # index of objects coexisting in 2010 and 2000 
    of_2010_indexes = [i for i,j in in_2010_and_2000_from_2010]
    # ^note: these are different lists, if took j instead of i, then would be same list
    if [j for i,j in in_2000_and_2010_from_2000] != [j for i,j in in_2010_and_2000_from_2010]:
        # like is seen here, j for j == True
        raise Exception(f'FLAWED ASSUMPTION , [j for i,j in 2000] != [j for i,j in 2010]\n'
                        f'len {len(in_2000_and_2010_from_2000)} {len(in_2010_and_2000_from_2010)}')
    # however i for i == False
    if of_2000_indexes == of_2010_indexes:
        # cheers
        raise Exception('FLAWED ASSUMPTION , of_2000_indexes != of_2010_indexes\n'
                        f'len y2k {len(of_2000_indexes)} 2k10 {len(of_2010_indexes)}')  

    # thin 2000 to shared geo
    b = b.iloc[of_2000_indexes]
    # thin 2010 to shared geo
    o = o.iloc[of_2010_indexes]

    # out 
    return b , o


print(convert())
