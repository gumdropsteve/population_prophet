import numpy as np
import pandas as pd
from data_processing import train_places, base_places


class CleanPlaces:
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
    def __init__(self, train, test):
        self.train = train
        self.test = test

    """find common Places across the Places our model will train on {train_places} 
        and the Places our model can predict on {base_places}
    """
    # identify Places we can compare our predictions with (# 29341)
    pre_measureable_places = [place for place in self.train if place in self.test]

    """clean Census 1970-2010 df (Train)
    """
    # identify columns needed to make GEO.display-label column (so can pair with ACS DataFrames) 
    for_geo_displays = ['PLACE','STATE']
    # pull those columns 
    to_geo_displays = load_census_place[for_geo_displays]

    # mold PLACE column into list with Place formatted as is in GEO.display-label
    places_70_10 = [place + ', ' for place in to_geo_displays.PLACE]

    # list paired State for each Place
    states_70_10 = [state for state in to_geo_displays.STATE]

    # merge places_70_10 and states_70_10 into list formatted as GEO.display-label column
    GEO_display_label = [ places_70_10[i] + states_70_10[i] for i in range(len(places_70_10))]

    # identify columns relevant to our end goal of predicting population for a given place
    place_cols_of_interest = ['AV0AA1970', 'AV0AA1980', 'AV0AA1990', 'AV0AA2000', 'AV0AA2010']
    # set base dataframe using Census (1970-2010) measurements 
    pop_place_70_10_ = load_census_place[place_cols_of_interest]

    # add GEO.display-label column from GEO_display_label list (# 31436)
    pop_place_70_10_['GEO.display-label'] = GEO_display_label

    # forget places without measurements for at least 3 of the 5 census measurement years (# 23027)
    at_least_3_70_10_ = pop_place_70_10_.dropna(axis=0) #,thresh=4)
    # forget places with measurements of 0 for 2000 (# 23018)
    not_0_for_2000_ = at_least_3_70_10_.loc[at_least_3_70_10_.AV0AA2000 != 0]
    # forget places with measurements of 0 for 2010 (# 23016)
    pop_place_70_10_ = not_0_for_2000_.loc[not_0_for_2000_.AV0AA2010 != 0]

    # note the remaining places (total # = 23016)
    census_places = [place for place in pop_place_70_10_['GEO.display-label']]
    # adjust measurable places to reflect places with census measurements (total # = 22506)
    measureable_places = [place for place in pre_measureable_places if place in census_places]

    """clean American Community Survey (ACS) 2011-2015 dataframes (Train)
    """
    # ID columns we will be using
    columns = ['GEO.display-label', 'HC01_EST_VC01']
    # convert 2011
    acs_20l1 = load_acs_20l1[columns]
    # convert 2012
    acs_20l2 = load_acs_20l2[columns]
    # convert 2013
    acs_20l3 = load_acs_20l3[columns]
    # convert 2014
    acs_20l4 = load_acs_20l4[columns]
    # convert 2015
    acs_20l5 = load_acs_20l5[columns]

    """convert Train years to reflect Places only seen in measureable_places
    """
    # drop Census Places not ideal for measurement (29346)
    census_place_populations = pop_place_70_10_.loc[pop_place_70_10_['GEO.display-label'].isin(measureable_places)]
    # drop 2011 ACS Places not ideal for measurement (29341)
    acs_2011_place_populations = acs_20l1.loc[acs_20l1['GEO.display-label'].isin(measureable_places)]
    # drop 2012 ACS Places not ideal for measurement (29341)
    acs_2012_place_populations = acs_20l2.loc[acs_20l2['GEO.display-label'].isin(measureable_places)]
    # drop 2013 ACS Places not ideal for measurement (29341) 
    acs_2013_place_populations = acs_20l3.loc[acs_20l3['GEO.display-label'].isin(measureable_places)]
    # drop 2014 ACS Places not ideal for measurement (29341) 
    acs_2014_place_populations = acs_20l4.loc[acs_20l4['GEO.display-label'].isin(measureable_places)]
    # drop 2015 ACS Places not ideal for measurement (29341) 
    acs_2015_place_populations = acs_20l5.loc[acs_20l5['GEO.display-label'].isin(measureable_places)]

    """clean ACS 2016 & 2017 dataframes (Test)
        take a sample of n Places to score our model
    """
    # identify 2016/2017 columns of interest (to measure against)
    test_col_of_i = ['GEO.display-label', 'HC01_EST_VC01']

    # shrink ACS 2017 df to columns to measure against only 
    testd_16_ = load_acs_20l6[test_col_of_i]
    # realize ACS 2016 combined measureable_places DataFrame (Baseline) dataframe 
    test_16_df_ = testd_16_.loc[testd_16_['GEO.display-label'].isin(measureable_places)]

    # shrink ACS 2017 df to columns to measure against only 
    testd_17_ = load_acs_20l7[test_col_of_i]
    # realize ACS 2017 combined measureable_places DataFrame (Baseline) dataframe 
    test_17_df_ = testd_17_.loc[testd_17_['GEO.display-label'].isin(measureable_places)]
    # conver
    test_17_1000_pops = [float(population) for population in test_17_df_.HC01_EST_VC01]
    # convert test_17_df_ populations to floats (numbers, from strings) 
    test_17_df_.HC01_EST_VC01 = test_17_1000_pops
    # forget Places with 2017 measured population less than 1,000 (13218 places remain)
    test_17_df_ = test_17_df_.loc[test_17_df_.HC01_EST_VC01 >= 1000]

