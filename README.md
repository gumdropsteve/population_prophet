# Forecasting Population by Place with Facebook Prophet
- Version 0.1
- [One pager](https://github.com/gumdropsteve/project-capstone/blob/master/presentation/one_pager.pdf)
- Spring 2019
## Purpose
This project aims to utilize machine learning on combined Census and American Community Survey datasets to accurately predict the future population of any place in the United States.
## Table of Contents
- Executive Summary
  - [Presentation](https://github.com/gumdropsteve/project-capstone/blob/master/README.md#presentation) 
  - [Dependencies](https://github.com/gumdropsteve/project-capstone/blob/master/README.md#dependencies-)
  - [Results](https://github.com/gumdropsteve/project-capstone/blob/master/README.md#results) (Overview)
- [Process](https://github.com/gumdropsteve/project-capstone/blob/master/README.md#process)
- [Prophet](https://github.com/gumdropsteve/project-capstone/blob/master/README.md#prophet)
    - [Model](https://github.com/gumdropsteve/project-capstone/blob/master/README.md#model)
    - [Specifications](https://github.com/gumdropsteve/project-capstone/blob/master/README.md#specifications)
- [Results](https://github.com/gumdropsteve/project-capstone/blob/master/README.md#results)
  - [Sample Places](https://github.com/gumdropsteve/project-capstone/blob/master/README.md#sample-places)
### Presentation
- [One Pager](https://github.com/gumdropsteve/project-capstone/blob/master/presentation/one_pager.pdf)
- [Resume](https://github.com/gumdropsteve/project-capstone/blob/master/presentation/may_2019.pdf)
### Dependencies <img align="right" width="372.6" height="253.8" src="https://github.com/gumdropsteve/project-capstone/blob/master/presentation/images/tech-used-Screenshot_2019-04-11%20project_capstone_1pager.png">
- Python 3.7.2  
- fbprophet 0.4.post2
- pandas 0.24.1
- NumPy 1.16.2
- scikit-learn 0.20.3
- Matplotlib 3.0.3
### Results
***Overview***
- The model preformed with an average 2.29% cross validated Mean Absolute Percentage Error
    - Calculated by compairing the final training year's actual values with the Model's predictions for that year
- Predictions on test years 2016 and 2017 proved consistently better than this
    - Averaged 1.826% and 1.993% MAPE (respectively)
    - Slightly more accurate than Baseline in 2016, and much more accurate than Baseline in 2017 
        - Averaged 2.052% and 3.855% MAPE (respectively)
        - Baseline predicted change equal to the largest year-to-year change seen in the past 5 years
## Process
#### 1. Exploratory Data Analysis 
  - Examined large number of Geographic filters on Total Population
    - E.g. Place, 5-digit Zip, County
  - Determined Place to be most usable
    - Why Place?
      - Maximum census measurements was 5
      - A large majority of Places had at least 3 measurements 
        - Almost all had at least 2
    - Counties were too ranged in Number of Measurements
      - East Coast having many being measured since 1790 and having 20+ 
      - Numerous others having less than 10, some restricted to 1 or 2 measurements
    - 5-digit Zip measurements were initialized too recently
      - No multi-decade historical data 
#### 2. Forged, then Combined DataFrames
  - US Census 
    - 1970-2010 
  - ACS 5-year Estimate 
    - 2011, '12, '13, '14, '15, '16, '17  

#### 3. Defined Baseline as assuming Continued Trend from Place’s population change  
  - Turned out to be incredibly difficult to beat
    - Especially in highly populated areas (e.g. New York City)

#### 4. Engineered Generalized Additive Model 
 - Made use of Facebook’s Prophet to forecast Total Population 
   - Required conversion of data to time-series format

#### 5. Randomly sampled 100 places
  - Allows interpretation on per year and decades-long basis
    - Did not consider places with Total Population less than 1,000
      - Neither Baseline nor Model preformed close to as well as on other areas
  - Fit Model on each sample place

#### 6. Measured Model Outcomes v. Baseline Assumptions
  - Compared to Actual 2016 & 2017 Populations
  - Model consistently outperformed when randomly sampling places (largest sample was 5,000)
    - In specific instances, however, it does come up short
      - "Sweet spots" seemed in Places with total population below 150,000 or above 650,000
        - Model struggled with mid-sized metropolises (e.g. New Orleans)
        
#### 7. Repeat 
  - Hint: repeat
## Prophet
Prophet is a procedure for forecasting time series data based on an additive model where non-linear trends are fit with yearly, weekly, and daily seasonality, plus holiday effects. The method was first open sourced by Facebook in late 2017, and is available in Python and R. 
### Model
Prophet makes use of a decomposable time series model with three main model components: trend, seasonality, and holidays.
`y(t) = g(t) + s(t) + h(t) + e(t)`
where:
- g(t)
    - *trend* models non-periodic changes (i.e. growth over time)
- s(t)
    - *seasonality* presents periodic changes (i.e. weekly, monthly, yearly)
- h(t)
    - ties in effects of *holidays* (on potentially irregular schedules ≥ 1 day(s))
- e(t)
    - covers idiosyncratic changes not accommodated by the model
- For more on the equation behind the procedure, check out [The Math of Prophet](https://medium.com/future-vision/the-math-of-prophet-46864fa9c55a) [10 min]
- To learn more about how to use Prophet, see [Intro to Facebook Prophet](https://medium.com/future-vision/intro-to-prophet-9d5b1cbd674e) [9 min]
### Specifications
As the question at hand relied on decennial and yearly datapoints, `Prophet`, was set to exclude daily and weekly seasonality while staying alert when identifying year-to-year trends and shifts in those trends over time. This was achieved;  
```
# use fbprophet to make Prophet model
place_prophet = fbprophet.Prophet(changepoint_prior_scale=0.15,
                                  daily_seasonality=False,
                                  weekly_seasonality=False,
                                  yearly_seasonality=True,
                                  n_changepoints=10)
```
## Results  
- The model preformed with an average 2.29% cross validated Mean Absolute Percentage Error
    - Calculated by compairing the final training year's actual values with the Model's predictions for that year
- Predictions on test years 2016 and 2017 proved consistently better than this
    - Averaged 1.826% and 1.993% MAPE (respectively)
    - Slightly more accurate than Baseline in 2016, and much more accurate than Baseline in 2017 
        - Averaged 2.052% and 3.855% MAPE (respectively)
        - Baseline predicted change equal to the largest year-to-year change seen in the past 5 years
- Results are based on averages from 5 random samples of 100 Places
### Sample Places
#### Pleasanton, California
- Cross Validated MAPE = 2.6964%
![Pleasanton, California Prophet Plot](https://github.com/gumdropsteve/project-capstone/blob/master/presentation/images/pleasanton_prophet.png)
- 2000 actual: 63,654    
- 2016
    - actual: 77,046
    - model: 79,398
- 2017
    - actual: 79,341
    - model: 82,084
- 2020 forecast: 87,920                    
- 2040 forecast: 130,530
#### Houston, Texas
- Cross Validated MAPE = 1.5751%
![Houston, Texas Prophet Plot](https://github.com/gumdropsteve/project-capstone/blob/master/presentation/images/houston_prophet.png)
- 2000 actual: 1,953,631  
- 2016
    - actual: 2,240,582
    - model: 2,314,358
- 2017
    - actual: 2,267,336
    - model: 2,398,134
- 2020 forecast: 2,394,410                  
- 2040 forecast: 2,794,675 
