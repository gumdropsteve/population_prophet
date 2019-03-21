from us import states
from census import Census
from api_key import api_key

c = Census( api_key )
x = c.acs5.get( ( 'NAME' , 'B25034_010E' ) , { 'for': f'state:{states.MD.fips}' } )

print(x)
