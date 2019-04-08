def prophet_by_county(years=20):
    # total population by county (1790 to 2010)
    by_state_county=pd.read_csv('../data/NHGIS/nhgis0003_csv/nhgis0003_ts_nominal_county.csv',encoding='ISO-8859-1')

    """
    input) years
        >> number of years to forecast 
    
    - generate DataFrame of population:
        > from 1790 to 2010
        > by unique county (use GIS Join as Id)
    - drop 
        > counties with less than 2 measurements
            > can only predict counties which have been measured 2+ times 
    - extract list of counties
        > each as a DataFrame ready for prediction 
        > column0='ds' , column1='y'
    """

    # df by GIS Join Match Code with measurements by decade (4050 rows × 24 columns)
    unique_counties = by_state_county.copy()[['GISJOIN','A00AA1790','A00AA1800','A00AA1810','A00AA1820','A00AA1830','A00AA1840','A00AA1850','A00AA1860',
                   'A00AA1870','A00AA1880','A00AA1890','A00AA1900','A00AA1910','A00AA1920','A00AA1930','A00AA1940','A00AA1950',
                    'A00AA1960','A00AA1970','A00AA1980','A00AA1990','A00AA2000','A00AA2010']]

    # drop NaN rows @ thresh = 3 due to GISJOIN being non-NaN (3408 rows × 24 columns ; 642 non-predictable counties (dropped)) 
    measureable_unique_counties = unique_counties.dropna(axis=0,thresh=3)
    # convert NaN values to 0 (note: there are 270 'dead' counties ('A00AA2010' == 0))
    measureable_unique_counties = measureable_unique_counties.fillna(0)

    # generate list of remaining GISJOIN codes 
    codes_of_measureable_unique_counties = [code for code in measureable_unique_counties.GISJOIN]
    # drop GISJOIN column
    measureable_unique_counties=measureable_unique_counties.drop('GISJOIN',axis=1)

    # list of str column names as years (for conversion to datetime)
    year_only_columns = [i[5:] for i in measureable_unique_counties.columns]
    # convert year_only_columns to DatetimeIndex of Timestamps
    dt_columns = pd.to_datetime(arg=year_only_columns)
    # convert dt_columns into dataframe 
    datetime_df = pd.DataFrame(dt_columns).T
    # w/ columns, so concatable with measureable_unique_counties
    datetime_df.columns = measureable_unique_counties.columns

    # generate list of remaining counties (each as pd.Series)
    dfs_of_measureable_unique_counties = [measureable_unique_counties.iloc[county] for county in range(len(measureable_unique_counties))]

    # add datetime_df to each dataframe as first row
    prophet_counties = [pd.concat((datetime_df,pd.DataFrame(county).T),axis=0) for county in dfs_of_measureable_unique_counties]
    # then transpose to 2 rows x 23 columns 
    prophet_almost_ready_counties = [county.T for county in prophet_counties]

    # set collection of prophets 
    prophet_by_county = []

    # run prophet model on each county 
    for county in range(len(prophet_almost_ready_counties)):
        # make the prophet model
        county_prophet = fbprophet.Prophet(changepoint_prior_scale=0.15)
        # identify county 
        a = prophet_almost_ready_counties[county]
        # rename county df's columns to agree with prophet formatting
        a.columns = ['ds','y']
        # fit county on prophet model 
        b = county_prophet.fit(a)
        # make a future dataframe for 20 years
        county_forecast = county_prophet.make_future_dataframe( periods=1*years, freq='Y' )
        # establish predictions
        county_forecast = county_prophet.predict(county_forecast)
        # add to collection 
        prophet_by_county.append(county_forecast)
    
    # output collection of forecasts
    return prophet_by_county