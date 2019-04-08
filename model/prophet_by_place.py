import pandas as pd
import fbprophet 

def population_by_place(years=20,n_places=1000,changepoint_prior=0.15,indicate=False,time=False):
    # total population by place (1970 to 2010)
    pop_by_place=pd.read_csv('../../data/NHGIS/nhgis0002_csv/nhgis0002_ts_nominal_place.csv',encoding='ISO-8859-1')
    """
    inputs) 
    >> years
        > number of years to forecast
    >> places
        > number of places to forecast +1 
            >> e.g. 99 = first 100 places (max==25102)
    >> changepoint_prior
        > set changepoint_prior_scale for prophet model
    >> indicate
        > default False
        > if True, print number of place forecasted after each forecast
    >> time
        > default False
        > if True, prints time the function took to run right before returning output
    
    function: 
    >> generate DataFrame of population:
        > from 1970 to 2010
        > by unique place (use NHGISCODE as Id)
    >> drop 
        > places with less than 2 measurements
            > can only predict places which have been measured 2+ times 
    >> extract list of places
        > each as a DataFrame ready for prediction 
        > column0='ds' , column1='y'
    >> make and fit prophet model on each place
    >> return prophet model's predictions
        > of each place
        > for {years} years
    """
    if time==True:
        import time
        now=time.time()

    # df by NHGISCODE with measurements by decade (31436 rows × 5 columns)
    unique_places = pop_by_place.copy()[['NHGISCODE','AV0AA1970','AV0AA1980','AV0AA2000','AV0AA2010']]

    # drop NaN rows @ thresh = 3 due to NHGISCODE being non-NaN (25103 rows × 5 columns ; 6333 non-measurable) 
    measureable_unique_places = unique_places.dropna(axis=0,thresh=3)
    # convert NaN values to 0 (note: there are 270 'dead' counties ('A00AA2010' == 0))
    measureable_unique_places = measureable_unique_places.fillna(0)

    # generate list of remaining NHGISCODE codes 
    codes_of_measureable_unique_places = [code for code in measureable_unique_places.NHGISCODE]
    # drop NHGISCODE column (25103 rows × 4 columns)
    measureable_unique_places = measureable_unique_places.drop('NHGISCODE',axis=1)

    # list of str column names as years (for conversion to datetime)
    year_only_columns = [i[5:] for i in measureable_unique_places.columns]
    # convert year_only_columns to DatetimeIndex of Timestamps
    dt_columns = pd.to_datetime(arg=year_only_columns)

    # convert dt_columns into dataframe 
    datetime_df = pd.DataFrame(dt_columns).T
    # w/ columns, so concatable with measureable_unique_counties
    datetime_df.columns = measureable_unique_places.columns

    # generate list of remaining places (each as pd.Series)
    dfs_of_measureable_unique_places = [measureable_unique_places.iloc[place] for place in range(len(measureable_unique_places))]

    # add datetime_df to each dataframe as first row
    prophet_places = [pd.concat((datetime_df,pd.DataFrame(place).T),axis=0) for place in dfs_of_measureable_unique_places]
    # then transpose to 2 rows x 23 columns 
    prophet_almost_ready_places = [place.T for place in prophet_places]

    # set collection of prophets 
    prophet_by_place = []

    # run prophet model on first 1000 places
    for place in range(len(prophet_almost_ready_places[:n_places])):
        # make the prophet model
        place_prophet = fbprophet.Prophet(changepoint_prior_scale=changepoint_prior)
        # identify county 
        a = prophet_almost_ready_places[place]
        # rename place df's columns to agree with prophet formatting
        a.columns = ['ds','y']
        # fit place on prophet model 
        b = place_prophet.fit(a)
        # make a future dataframe for 20 years
        place_forecast = place_prophet.make_future_dataframe( periods=1*years, freq='Y' )
        # establish predictions
        place_forecast = place_prophet.predict(place_forecast)
        # add to collection 
        prophet_by_place.append(place_forecast)
        # did we ask for indication (hint: do this if calculating for > 1000 places unless you enjoy anxiety)
        if indicate==True:
            # let us know the count
            print(place)
            
    if time==True:
        then=time.time()
        print(f'now = {now}\nthen = {then}\ntime = {now-then}')
        
    # return forecasts
    return prophet_by_place
