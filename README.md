# Forecasting Population by Place with Facebook Prophet
- Version 0.1.08
- Winston Robson, April 2019
## Purpose
This project aims to utilize machine learning on combined Census and American Community Survey datasets to accurately predict the future population of any place in the United States.
## Table of Contents
- Overview
  - [Presentation](https://github.com/gumdropsteve/project-capstone/blob/master/README.md#presentation) 
  - [Dependencies](https://github.com/gumdropsteve/project-capstone/blob/master/README.md#dependencies)
  - Results (Summary)
- [Process](https://github.com/gumdropsteve/project-capstone/blob/master/README.md#process)
- [Prophet](https://github.com/gumdropsteve/project-capstone/blob/master/README.md#prophet)
    - [About](https://github.com/gumdropsteve/project-capstone/blob/master/README.md#about)
      - [Why it was used](https://github.com/gumdropsteve/project-capstone/blob/master/README.md#why-it-was-used)
    - [Model](https://github.com/gumdropsteve/project-capstone/blob/master/README.md#model)
    - [Specifications](https://github.com/gumdropsteve/project-capstone/blob/master/README.md#specifications)
- [Results](https://github.com/gumdropsteve/project-capstone/blob/master/README.md#results)
  - [Diagnostics](https://github.com/gumdropsteve/project-capstone/blob/master/README.md#diagnostics)
    - [cross_validation](https://github.com/gumdropsteve/project-capstone/blob/master/README.md#cross-validation)
    - [performance_metrics](https://github.com/gumdropsteve/project-capstone/blob/master/README.md#preformance-metrics)
  - [Plots & Predictions](https://github.com/gumdropsteve/project-capstone/blob/master/README.md#plots--predictions)
    - Sample Cities(https://github.com/gumdropsteve/project-capstone/blob/master/README.md#sample-cities)
- [Future Work](https://github.com/gumdropsteve/project-capstone/blob/master/README.md#future-work)
### Presentation
- [One Pager](https://github.com/gumdropsteve/project-capstone/blob/master/presentation/project_capstone_1pager.pdf)
- [Resume](https://github.com/gumdropsteve/project-capstone/blob/master/presentation/may_2019.pdf)
- [Slides](https://docs.google.com/presentation/d/13fey4Nzs-MHNS3qDf0GmpccINqg_SIVSE6mhTkwsUiM/edit?usp=sharing)
### Dependencies <img align="right" width="372.6" height="253.8" src="https://github.com/gumdropsteve/project-capstone/blob/master/presentation/images/tech-used-Screenshot_2019-04-11%20project_capstone_1pager.png">
 - Python 3.7.2  
 - fbprophet 0.4.post2
 - pandas 0.24.1
 - NumPy 1.16.2
 - scikit-learn 0.20.3
 - Matplotlib 3.0.3
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
Prophet, an open source forecasting tool by Facebook available in Python and R. 
### About
Forecasting is a data science task that is central to many activities within an organization. 

For instance, large organizations like Facebook must engage in capacity planning to efficiently allocate scarce resources and goal setting in order to measure performance relative to a baseline. 

Producing high quality forecasts is not an easy problem for either machines or for most analysts. 

We have observed two main themes in the practice of creating a variety of business forecasts:
- Completely automatic forecasting techniques can be brittle and they are often too inflexible to incorporate useful assumptions or heuristics.
- Analysts who can produce high quality forecasts are quite rare because forecasting is a specialized data science skill requiring substantial experience.
#### Why it was used
### Model
#### Specifications

## Results  
### Diagnostics
### Cross Validation
#### Performance Metrics
### Plots & Predictions
#### Sample Cities
##### Bentonville, Arkansas
![Bentonville, Arkansas Prophet Plot](https://github.com/gumdropsteve/project-capstone/blob/master/presentation/images/bentonville_prophet.png)
##### Pleasanton, California
![Pleasanton, California Prophet Plot](https://github.com/gumdropsteve/project-capstone/blob/master/presentation/images/pleasanton_prophet.png)

## Future Work:
