date = 'First published:March 12, 2020'

if 'First published' in date:
    #delete 'First published:'
    date = date[16:]

[month, day, year] = date.split()
day = day[:2]

print(month)
print(day)
print(year)