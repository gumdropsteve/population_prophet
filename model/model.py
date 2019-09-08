import fbprophet 
import pandas as pd
from fbprophet.diagnostics import cross_validation, performance_metrics

def prophet_place(df):
    """forecast place populations 
        > currently processes 1 place
            >> future version may multiple place processing
    """
    collection = []
    # make DataFrame of column values as datetime (first converting to Series)
    datetimes = pd.DataFrame(data=pd.to_datetime(pd.Series(data=df.columns)))

    # go though each place in df
    for i in range(len(df)):
        # extract DataFrame for that place
        df = df.iloc[i]
        # add datetime values to forge place specific DataFrame
        df = pd.concat([df.reset_index(),datetimes],axis=1)
        
        # use fbprophet to make Prophet model
        prophet = fbprophet.Prophet(changepoint_prior_scale=0.15,
                                    daily_seasonality=False,
                                    weekly_seasonality=False,
                                    yearly_seasonality=True,
                                    n_changepoints=7)
        
        # rename Place df's columns to agree with prophet formatting
        df.columns = ['drop','y','ds']
        # adjust df ; forget index column (drop)
        df = df[['ds','y']]
        print(df)
        
        # fit place on prophet model 
        prophet.fit(df)
        
        # cross validate 
        cross_val = cross_validation(prophet,
                                     initial='14235 days', 
                                     period='180 days', 
                                     horizon='365 days')
        # full metrics from crass validation
        metrics = performance_metrics(cross_val) 
        
        # make a future dataframe for 2016 & 2017 years
        future_df = prophet.make_future_dataframe(periods=3,freq='Y')
        
        # establish predictions
        forecast = prophet.predict(future_df)
 
        # store 2016 and 2017 predictions
        preds = [forecast.loc[forecast.ds == '2016-12-31'].yhat.values[0],
                 [forecast.loc[forecast.ds == '2017-12-31'].yhat.values[0]]]
        
        # model plot the forecase
        m_plot = prophet.plot(fcst=forecast, 
                              ax=None, 
                              uncertainty=True, 
                              plot_cap=True, 
                              xlabel='Time (Years)', 
                              ylabel='Total Population')

        # add instance to collection
        # client = [forecast, metrics, preds, m_plot, prophet]
        # collection.append(client)

    # output all
    # return collection
    return [forecast, metrics, preds, m_plot, prophet]


# default sampler
if __name__=='__main__':
    from data_processing import clean_places
    # check for prefered target
    ask = input('searching for any place in particular? (y/n) ')
    if ask == 'y':
        # is user familiar with input options?
        ask = input('are you familiar with the palce directory? (y/n) ')
        if ask == 'y':
            # get prefered target
            ask = input('POI: ')
            train, test, places = clean_places(n_places=1, place=ask)
        else:
            # to be built out
            raise Exception('ERROR')
    # default
    else:
        train, test, places = clean_places(n_places=1, place="Bentonville city, Arkansas")
            
    print(prophet_place(train))
