import re

a = '<p>a</p>'

b = re.sub(r'<.+?>','',a)
print(b)