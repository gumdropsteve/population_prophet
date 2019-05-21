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
- Model
  - Prophet
    - About
    - Why it was used
  - Specifications
- [Results](https://github.com/gumdropsteve/project-capstone/blob/master/README.md#results)
  - Diagnostics
    - cross_validation
    - performance_metrics
  - Plots & Predictions
    - Bentonville, AR
    - Pleasanton, CA
    - San Francisco, CA
    - New Orleans, LA
    - Houston, TX
    - New York City, NY
    - Sidney, NE
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

## Results
### Prophet
#### Bentonville, Arkansas
![Bentonville, Arkansas Prophet Plot](https://github.com/gumdropsteve/project-capstone/blob/master/presentation/images/bentonville_prophet.png)
#### Pleasanton, California
![Pleasanton, California Prophet Plot](https://github.com/gumdropsteve/project-capstone/blob/master/presentation/images/pleasanton_prophet.png)

## Future Work
#### Theoretical Continued Purpose:
When listing any house, the numerous measurements any 
good REALTOR® will consider range from the condition of 
the property to what’s for lunch that day. Most prevalent, though, 
is their assessment of demand; after all, a million-dollar mansion 
(or million-dollar shed in San Francisco), is only worth $1,000,000 
if someone will purchase it at that price. 

As humans take up space, one main driver of demand in any 
housing market is population. The more people seek to live in
any location, the more valuable that location is.

While it is entirely reasonable for you to build a $7.9m single-family 
resort in Sidney, Nebraska, you may encounter a few difficulties 
trying to sell it in 2019.
 
On the other hand, however, if you were the individual who bought 
the modest 4 bed, 4 bath, 4,437 sqft abode at [24 Clarendon Ave](https://www.realtor.com/realestateandhomes-detail/24-Clarendon-Ave_San-Francisco_CA_94114_M28366-36605),
San Francisco, CA 94114 on August 5th, 1996 for $588,000,
![alt text](https://github.com/gumdropsteve/project-capstone/blob/master/presentation/images/Screenshot_2019-04-11%20project_capstone_1pager.png)

you could comfortably list it for a mere $4,400,000 and expect to
sell in about 40 days, while moaning about how you should have 
bought the [house down the street](https://www.zillow.com/homedetails/140-Clarendon-Ave-San-Francisco-CA-94114/15129075_zpid/?utm_source=email&utm_medium=email&utm_campaign=emo-sendtofriend-similar-homes-image&rtoken=558bffa9-675a-4f63-94d0-c46d8aee2893~X1-ZUyeh68ohf1og9_9skq8), currently listed at $5,995,000.

The goal of this project is to utilize machine learning on combined
US Census and American Community Survey datasets to predict
future population of a given place in the United States. With the results
we can move on to assess property values and how they relate.

Wording incomplete 
- project in 12 words
    - Predicting population growth or decline on scalable communities in the United States. (12)
    - Predicting trend for any selected US population with Census data. (10)
    - Assessing the current and future states of population for given zip code(s) with Census data and machine learning. (18) 

Galvanize Data Science Immersive Capstone Project (Spring 2019, San Francisco, g88)

- population by place (e.g. Pleasanton, California ; Bentonville, Arkansas)
    - based on Census 1970 to 2010
- population by county (e.g. Alameda County, California ; Benton County, Arkansas)
    - based on Census 1790 to 2010
- population by zip code (e.g. 94566 ; 72710)
    - based on American Community Survey 5-year estimates 2011-2017
