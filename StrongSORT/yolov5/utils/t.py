import re

s1=re.compile('^(-?[1-9]{1}\d*)|0$')
r1=s1.findall('-1')

print(r1)