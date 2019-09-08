import numpy as np
import pandas as pd


def load_data(train=True, test=True, sort='common'):
    #load Train data
    if train == True:
        # population by Place Census 1970-2010 measurements
        load_census_place = pd.read_csv('../data/NHGIS/nhgis0002_csv/nhgis0002_ts_nominal_place.csv',encoding='ISO-8859-1')
        # population by Place ACS 2011
        load_acs_2011 = pd.read_csv('../data/American_Community_Survey/ACS_11_5YR_S0101/ACS_11_5YR_S0101_with_ann.csv',encoding='ISO-8859-1',low_memory=False) 
        # population by Place ACS 2012
        load_acs_2012 = pd.read_csv('../data/American_Community_Survey/ACS_12_5YR_S0101/ACS_12_5YR_S0101_with_ann.csv',encoding='ISO-8859-1',low_memory=False) 
        # population by Place ACS 2013
        load_acs_2013 = pd.read_csv('../data/American_Community_Survey/ACS_13_5YR_S0101/ACS_13_5YR_S0101_with_ann.csv',encoding='ISO-8859-1',low_memory=False) 
        # population by Place ACS 2014
        load_acs_2014 = pd.read_csv('../data/American_Community_Survey/ACS_14_5YR_S0101/ACS_14_5YR_S0101_with_ann.csv',encoding='ISO-8859-1',low_memory=False) 
        # population by Place ACS 2015
        load_acs_2015 = pd.read_csv('../data/American_Community_Survey/ACS_15_5YR_S0101/ACS_15_5YR_S0101_with_ann.csv',encoding='ISO-8859-1',low_memory=False) 
        # collect all
        train_data = [load_census_place,load_acs_2011,load_acs_2012,load_acs_2013,load_acs_2014,load_acs_2015]
    # load Test data
    if test == True:
        # population by Place ACS 2016
        load_acs_2016 = pd.read_csv('../data/American_Community_Survey/ACS_16_5YR_S0101/ACS_16_5YR_S0101_with_ann.csv',encoding='ISO-8859-1',low_memory=False) 
        # population by Place ACS 2017
        load_acs_2017 = pd.read_csv('../data/American_Community_Survey/ACS_17_5YR_S0101/ACS_17_5YR_S0101_with_ann.csv',encoding='ISO-8859-1',low_memory=False)
        # collect all
        test_data = [load_acs_2016,load_acs_2017]

    # find common places across Census and each train ACS
    if sort == 'common':
        # 2011 - 2015
        if train == True:
            # identify Places measured in 2011 ACS [0 == 'Geography'] (# 29517)
            acs11places = [place for place in load_acs_2011['GEO.display-label'][1:]]
            # identify Places measured in 2012 ACS  (# 29510)
            acs12places = [place for place in load_acs_2012['GEO.display-label']]
            # identify Places measured in 2013 ACS (# 29510)
            acs13places = [place for place in load_acs_2013['GEO.display-label']]
            # identify Places measured in 2014 ACS (# 29550)
            acs14places = [place for place in load_acs_2014['GEO.display-label']]
            # identify Places measured in 2015 ACS (# 29575)
            acs15places = [place for place in load_acs_2015['GEO.display-label']]
            # cross 2011-2015, keep coexisting Places (# 29475)
            train_places = [place for place in acs11places if place in acs12places and acs13places and acs14places and acs15places]

        # 2016, 2017
        if test == True:
            # identify Places measured in 2016 ACS (# 29574) [0 == 'Geography']
            acs16places = [place for place in load_acs_2016['GEO.display-label'][1:]]
            # identify Places measured in 2017 ACS (# 29577)
            acs17places = [place for place in load_acs_2017['GEO.display-label']]
            # cross 2017 Places w/ 2016 Places, keep coexisting Places (# 29550)
            test_places = [place for place in acs17places if place in acs16places]

        if len(train_places) < 1:
            train_places = test_places
            print(f'len(train_places) == {len(train_places)}')
        if len(test_places) < 1:
            test_places = train_places
            print(f'len(test_places) == {len(test_places)}')
        # tag common places
        places = [place for place in test_places if place in train_places]
    
        return [train_data, test_data, places]


def clean_places(n_places=10, place=False):
    """
    >> takes in 
        > Census 1970-2010 dataframe (1 df)
            >> total population by Place measurements
        > American Community Survey (ACS) 2011-2017 dataframes (7 dfs)
            >> total population (age & sex) by Place 

    >> forges DataFrame of places that have 
        > at least one (1) recording for Census years 1970-2010
        > at least one (1) recording for ACS years 2011-2015
    """
    train, test, places = load_data(train=True, test=True, sort='common')

    # unzip data
    load_census_place = train[0]

    load_acs_2011 = train[1]
    load_acs_2012 = train[2]
    load_acs_2013 = train[3]
    load_acs_2014 = train[4]
    load_acs_2015 = train[5]

    load_acs_2016, load_acs_2017 = test[0], test[1]

    """clean Census 1970-2010 df (Train)
    """
    # identify columns needed to make GEO.display-label column (so can pair with ACS DataFrames) 
    geo_display = ['PLACE','STATE']
    # pull those columns 
    to_geo_displays = load_census_place[geo_display]

    # mold PLACE column into list with Place formatted as is in GEO.display-label
    places_70_10 = [place + ', ' for place in to_geo_displays.PLACE]

    # list paired State for each Place
    states_70_10 = [state for state in to_geo_displays.STATE]

    # merge places_70_10 and states_70_10 into list formatted as GEO.display-label column
    GEO_display_label = [places_70_10[i] + states_70_10[i] for i in range(len(places_70_10))]
    load_census_place['GEO.display-label'] = GEO_display_label

    # identify columns relevant to our end goal of predicting population for a given place
    cols_of_interest = ['GEO.display-label','AV0AA1970', 'AV0AA1980', 'AV0AA1990', 'AV0AA2000', 'AV0AA2010']
    # set base dataframe using Census (1970-2010) measurements 
    census_years = load_census_place[cols_of_interest]
    # rename census years for later conformity 
    census_years.columns = ['GEO.display-label','1970', '1980', '1990', '2000', '2010']

    # forget places without measurements for at least 3 of the 5 census measurement years (# 23027)
    census_years = census_years.dropna(axis=0)  # ,thresh=4
    # forget places with measurements of 0 for 2000 or 2010
    conditions = ((census_years['2000'] != 0) & (census_years['2010'] != 0))
    census_years = census_years.loc[conditions]

    # note the remaining places (total # = 23016)
    census_places = [place for place in census_years['GEO.display-label']]
    
    # adjust measurable places to reflect places with census measurements
    measureable_places = [i for i in census_places if i in places]
    
    # drop 2017 ACS Places not ideal for measurement
    acs_2017 = load_acs_2017.loc[load_acs_2017['GEO.display-label'].isin(measureable_places)]
   
    # convert 2017 populations to floats (numbers, from strings) 
    acs_2017['HC01_EST_VC01'] = acs_2017['HC01_EST_VC01'].astype(float)
    # forget places with 2017 measured population less than 1,000 
    test2017 = acs_2017.loc[acs_2017.HC01_EST_VC01 > 1000]    
    
    # do we have a target?
    if place:
        # well, focus target
        test_2017 = acs_2017.loc[acs_2017['GEO.display-label'] == place]
        if len(test_2017) != 1:
            raise Exception(f'ERROR len(test_2017) != 1 == {len(test_2017)}')
    else:
        # sample baseline data for places to evaluate model 
        test_2017 = acs_2017.sample(n_places)
        
    # list places for conversion of other dataframes
    sample_places = [place for place in test_2017['GEO.display-label']]

    # adjust dataframes to sampled places
    _s_census_ = census_years.loc[census_years['GEO.display-label'].isin(sample_places)]
    acs_2011 = load_acs_2011.loc[load_acs_2011['GEO.display-label'].isin(sample_places)]
    acs_2012 = load_acs_2012.loc[load_acs_2012['GEO.display-label'].isin(sample_places)]
    acs_2013 = load_acs_2013.loc[load_acs_2013['GEO.display-label'].isin(sample_places)]
    acs_2014 = load_acs_2014.loc[load_acs_2014['GEO.display-label'].isin(sample_places)]
    acs_2015 = load_acs_2015.loc[load_acs_2015['GEO.display-label'].isin(sample_places)]
    test2016 = load_acs_2016.loc[load_acs_2016['GEO.display-label'].isin(sample_places)]

    # remaining columns of interest
    columns = ['GEO.display-label', 'HC01_EST_VC01']
    # convert train years
    acs_2011 = acs_2011[columns]
    acs_2012 = acs_2012[columns]
    acs_2013 = acs_2013[columns]
    acs_2014 = acs_2014[columns]
    acs_2015 = acs_2015[columns]
    # convert test years
    test2016 = test2016[columns]
    test2017 = test2017[columns]

    # set Census index to Places, and forget Place column 
    s_census = _s_census_.set_index(_s_census_['GEO.display-label'])
    # rename Census columns to years for later datetime conversion
    s_census = s_census[['1970','1980','1990','2000','2010']]

    # set 2011 index to Places, add year column, drop extra columns
    acs_2011 = acs_2011.set_index(acs_2011['GEO.display-label'])
    acs_2011['2011'] = acs_2011.HC01_EST_VC01
    acs_2011 = acs_2011['2011']

    # set 2012 index to Places, add year column, drop extra columns
    acs_2012 = acs_2012.set_index(acs_2012['GEO.display-label'])
    acs_2012['2012'] = acs_2012.HC01_EST_VC01
    acs_2012 = acs_2012['2012']

    # set 2013 index to Places, add year column, drop extra columns
    acs_2013 = acs_2013.set_index(acs_2013['GEO.display-label'])
    acs_2013['2013'] = acs_2013.HC01_EST_VC01
    acs_2013 = acs_2013['2013']

    # set 2014 index to Places, add year column, drop extra columns
    acs_2014 = acs_2014.set_index(acs_2014['GEO.display-label'])
    acs_2014['2014'] = acs_2014.HC01_EST_VC01
    acs_2014 = acs_2014['2014']

    # set 2015 index to Places, add year column, drop extra columns
    acs_2015 = acs_2015.set_index(acs_2015['GEO.display-label'])
    acs_2015['2015'] = acs_2015.HC01_EST_VC01
    acs_2015 = acs_2015['2015']

    # add & continue with year column only
    test2016 = test2016.set_index(test2016['GEO.display-label'])
    test2016['2016'] = test2016.HC01_EST_VC01
    test2016 = test2016['2016']

    # add & continue with year column only
    test2017 = test2017.set_index(test2017['GEO.display-label'])
    test2017['2017'] = test2017.HC01_EST_VC01
    test2017 = test2017['2017']

    # base full df off census years
    combined_df = s_census.fillna(0)
    # and 0 out null values 
    combined_df['2011'] = acs_2011.fillna(0)
    combined_df['2012'] = acs_2012.fillna(0)
    combined_df['2013'] = acs_2013.fillna(0)
    combined_df['2014'] = acs_2014.fillna(0)
    combined_df['2015'] = acs_2015.fillna(0)
    combined_df['2016'] = test2016.fillna(0)
    combined_df['2017'] = test2017.fillna(0)

    # split train_df from combined_df
    train = combined_df[['1970', '1980', '1990', '2000', '2010', '2011', '2012', '2013', '2014','2015']]
    # split test_df form combined_df
    test = combined_df[['2016', '2017']]

    return train, test, sample_places

                    
# default run
if __name__ =='__main__':
    pass
