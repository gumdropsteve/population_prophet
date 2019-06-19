import fbprophet 
import pandas as pd
from fbprophet.diagnostics import cross_validation, performance_metrics


def prophet_place():
    """forecast 2016 and 2017 populations using model for each sample Place
    """
    # set out route for forecast tables
    forecasts = []
    # set out route for 2016 & 2017 Train predictions
    train_preds = []
    # set out for plots
    plots = []
    # record cross vals
    metrics=[]
    # record prophets
    prophets = []

    # make DataFrame of column values as datetime (first converting to Series)
    datetimes = pd.DataFrame(data=pd.to_datetime(pd.Series(data=train_df.columns)))

    # go though each place in train_df
    for i in range(len(train_df)):
        # extract DataFrame for that place
        df = train_df.iloc[i]
        # add datetime values to forge place specific DataFrame
        df = pd.concat([df.reset_index(),datetimes],axis=1)
        
        # use fbprophet to make Prophet model
        place_prophet = fbprophet.Prophet(changepoint_prior_scale=0.15,
                                          daily_seasonality=False,
                                          weekly_seasonality=False,
                                          yearly_seasonality=True,
                                          n_changepoints=7)
        
        # rename Place df's columns to agree with prophet formatting
        df.columns = ['drop','y','ds']
        # adjust df ; forget index column (drop)
        df = df[['ds','y']]
        
        # fit place on prophet model 
        place_prophet.fit(df)
        
        # cross validate 
        
        df_cv = cross_validation(place_prophet, initial='14235 days', period='180 days', horizon = '365 days')
        # full metrics from crass validation
        df_p = performance_metrics(df_cv) 
        # add them to the list
        metrics.append(df_p)
        
        # make a future dataframe for 2016 & 2017 years
        place_forecast = place_prophet.make_future_dataframe(periods=3, 
                                                            freq='Y')
        
        # establish predictions
        forecast = place_prophet.predict(place_forecast)
        # tag and bag (forecast table)
        forecasts.append(forecast)    
        # store 2016 and 2017 predictions
        train_preds.append([
            forecast.loc[forecast.ds == '2016-12-31'].yhat.values[0],
            forecast.loc[forecast.ds == '2017-12-31'].yhat.values[0]])
        
        # model plot the forecase
        m_plot = place_prophet.plot(forecast, 
                                    ax=None, 
                                    uncertainty=True, 
                                    plot_cap=True, 
                                    xlabel='Time (Years)', 
                                    ylabel='Total Population')
        # add to plots
        plots.append(m_plot)

    # output all
    return forecasts, train_preds, plots, metrics, prophets
