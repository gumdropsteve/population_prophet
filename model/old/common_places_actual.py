def common_places_actual():
    """
    > extract common places 
        >> and their population 
            > for years 2011-2017
            > from ACS population data (by Place)
    """
    # load 2017
    actual7 = pd.read_csv('../../data/American_Community_Survey/ACS_17_5YR_S0101/ACS_17_5YR_S0101_with_ann.csv',encoding='ISO-8859-1',low_memory=False) 
    # load 2016
    actual6 = pd.read_csv('../../data/American_Community_Survey/ACS_16_5YR_S0101/ACS_16_5YR_S0101_with_ann.csv',encoding='ISO-8859-1',low_memory=False) 
    # load 2015
    actual5 = pd.read_csv('../../data/American_Community_Survey/ACS_15_5YR_S0101/ACS_15_5YR_S0101_with_ann.csv',encoding='ISO-8859-1',low_memory=False) 
    # load 2014
    actual4 = pd.read_csv('../../data/American_Community_Survey/ACS_14_5YR_S0101/ACS_14_5YR_S0101_with_ann.csv',encoding='ISO-8859-1',low_memory=False) 
    # load 2013
    actual3 = pd.read_csv('../../data/American_Community_Survey/ACS_13_5YR_S0101/ACS_13_5YR_S0101_with_ann.csv',encoding='ISO-8859-1',low_memory=False) 
    # load 2012
    actual2 = pd.read_csv('../../data/American_Community_Survey/ACS_12_5YR_S0101/ACS_12_5YR_S0101_with_ann.csv',encoding='ISO-8859-1',low_memory=False) 
    # load 2011
    actual1 = pd.read_csv('../../data/American_Community_Survey/ACS_11_5YR_S0101/ACS_11_5YR_S0101_with_ann.csv',encoding='ISO-8859-1',low_memory=False) 
    
    # make 2017 df containing only Place names (GEO.display-label) and population (HC01_EST_VC01)
    a17 = actual7.copy()[['GEO.display-label','HC01_EST_VC01']][1:]
    # make 2016 df containing only Place names (GEO.display-label) and population (HC01_EST_VC01)
    a16 = actual6.copy()[['GEO.display-label','HC01_EST_VC01']][1:]
    # make 2015 df containing only Place names (GEO.display-label) and population (HC01_EST_VC01)
    a15 = actual5.copy()[['GEO.display-label','HC01_EST_VC01']][1:]
    # make 2014 df containing only Place names (GEO.display-label) and population (HC01_EST_VC01)
    a14 = actual4.copy()[['GEO.display-label','HC01_EST_VC01']][1:]
    # make 2013 df containing only Place names (GEO.display-label) and population (HC01_EST_VC01)
    a13 = actual3.copy()[['GEO.display-label','HC01_EST_VC01']][1:]
    # make 2012 df containing only Place names (GEO.display-label) and population (HC01_EST_VC01)
    a12 = actual2.copy()[['GEO.display-label','HC01_EST_VC01']][1:]
    # make 2011 df containing only Place names (GEO.display-label) and population (HC01_EST_VC01)
    a11 = actual1.copy()[['GEO.display-label','HC01_EST_VC01']][1:]
    
    # collect each Place for 2017
    a17places = [place for place in a17['GEO.display-label']]
    # collect each Place for 2016
    a16places = [place for place in a16['GEO.display-label']]
    # collect each Place for 2015
    a15places = [place for place in a15['GEO.display-label']]
    # collect each Place for 2014
    a14places = [place for place in a14['GEO.display-label']]
    # collect each Place for 2013
    a13places = [place for place in a13['GEO.display-label']]
    # collect each Place for 2012
    a12places = [place for place in a12['GEO.display-label']]
    # collect each Place for 2011
    a11places = [place for place in a11['GEO.display-label']]
    
    # set collection of each Place if occouring in... 
    combo_places=[]
    # 2017
    for place in a17places:
        # 2016
        if place in a16places:
            # 2015
            if place in a15places:
                # 2014
                if place in a14places:
                    # 2013
                    if place in a13places:
                        # 2012
                        if place in a12places:
                            # 2011
                            if place in a11places:
                                # add Place to collection 
                                combo_places.append(place)
    
    # convert DataFrames to only contain shared values (len == 29341)
    a17=a17.loc[a17['GEO.display-label'].isin(combo_places)]  # 2017
    a16=a16.loc[a16['GEO.display-label'].isin(combo_places)]  # 2016
    a15=a15.loc[a15['GEO.display-label'].isin(combo_places)]  # 2015
    a14=a14.loc[a14['GEO.display-label'].isin(combo_places)]  # 2014
    a13=a13.loc[a13['GEO.display-label'].isin(combo_places)]  # 2013
    a12=a12.loc[a12['GEO.display-label'].isin(combo_places)]  # 2012
    a11=a11.loc[a11['GEO.display-label'].isin(combo_places)]  # 2011
    
    # return list containing each dataframe
    return [a17,a16,a15,a14,a13,a12,a11]
    