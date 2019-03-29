import csv
import xlrd
import numpy as np
import pandas as pd

# Table A-1. Annual Geographical Mobility Rates, By Type of Movement: 2018
annual_geographical_mobility_rates_type_movement = pd.read_excel( '../data/cps-historical-migration-geographic-mobility/tab-a-1.xls' )

# Table A-2. Annual Inmigration, Outmigration, Net Migration, and Movers from Abroad for Regions: 2018
annual_inmigration_outmigration_net_migration__movers_from_abroad_for_regions = pd.read_excel( '../data/cps-historical-migration-geographic-mobility/tab-a-2.xls' )

# Table A-3. Inmigration, Outmigration, and Net Migration by Metropolitan Status: 2018
inmigration_outmigration__net_migration_metropolitan_status = pd.read_excel( '../data/cps-historical-migration-geographic-mobility/tab-a-3.xls' )

# Table A-4. Geographical Mobility by Tenure: 2018
geographical_mobility_by_tenure = pd.read_excel( '../data/cps-historical-migration-geographic-mobility/tab-a-4.xls' )

# Table A-5. Reason for Move (Specific Categories): 2018
reason_for_move_specific_categories = pd.read_excel( '../data/cps-historical-migration-geographic-mobility/tab-a-5.xls' )

# Table A-6. Distance of Intercounty Move: 2018
distance_of_intercounty_move = pd.read_excel( '../data/cps-historical-migration-geographic-mobility/tab-a-6.xls' )


# copy dataframe , generalize name
df = annual_geographical_mobility_rates_type_movement.copy()

# drop columns without any non-NaN values
df = df.dropna(thresh= ( 1 ) )


# rename dataframe
df = annual_geographical_mobility_rates_type_movement.copy()

# drop columns with less than 2 non-NaN values
df = df.dropna( thresh= ( 2 ) )

# collect column names as pandas series
col_names_0to4_9 = df.iloc[ 0 ]
col_names_5to6 = df.iloc[ 1 ]
col_names7to8 = df.iloc[ 2 ]

# initialize list for column names
column_names = []

# fill list with first row of column names , no exceptions
for column_name in col_names_0to4_9:    
    column_names.append( column_name )

# set index count to -1 so column 0 == column 0
_ = -1

# replace items 5 and 6 in column_names with column names 5 and 6
for column_name in col_names_5to6:
    _ += 1
    # column_name is string (nan instances = float) and name is not 'Total'   
    if isinstance( column_name , str ) and column_name != 'Total':
        # column_name is aligned to replace a nan         
        if str( column_names[ _ ] ) == 'nan':
            # replace item in column_names with column_name             
            column_names[ _ ] = column_name

# set index count to -1 so column 0 == column 0
_ = -1

# replace items 7 and 8 in column_names with column names 7 and 8
for column_name in col_names7to8:
    _ += 1
    # column_name is string (nan instances = float) and name is not 'Total'   
    if isinstance( column_name , str ) and column_name != 'Total':
        # column_name is aligned to replace a nan         
        if str( column_names[ _ ] ) == 'nan':
            # replace item in column_names with column_name             
            column_names[ _ ] = column_name

# (re)set column names
df.columns = column_names

# drop rows used to extract column names
df = df[3:]

# reset dataframe index
df = df.reset_index( drop=True ) 



