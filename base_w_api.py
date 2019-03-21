from us import states
from census import Census
from api_key import api_key

'''
Datasets accessable via Census
    ACS 5 Year Estimates (2016, 2015, 2014, 2013, 2012, 2011, 2010)
        acs5
    ACS 1 Year Estimates, Data Profiles (2016, 2015, 2014, 2013, 2012)
        acs1dp
    Census Summary File 1 (2010, 2000, 1990)
        sf1
    Census Summary File 3 (2000, 1990)
        sf3
'''

c = Census( api_key )
x = c.acs5.get( ( 'NAME' , 'B25034_010E' ) , { 'for': f'state:{states.MD.fips}' } )

print(x)
