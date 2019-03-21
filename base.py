from api-key import api_key
from census import Census
from us import states

c = Census(api_key)
x = c.acs5.get(('NAME', 'B25034_010E'),
          {'for': 'state:{}'.format(states.MD.fips)})
print(x)
