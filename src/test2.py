a = "December 16, 2020"
[month, day, year] = a.split()
day = day[:2]

if   month == 'January':
    month = '01'
elif month == 'February':
    month = '02'
elif month == 'March':
    month = '03'
elif month == 'April':
    month = '04'
elif month == 'May':
    month = '05'
elif month == 'June':
    month = '06'
elif month == 'July':
    month = '07'
elif month == 'August':
    month = '08'
elif month == 'September':
    month = '09'
elif month == 'October':
    month = '10'
elif month == 'November':
    month = '11'
elif month == 'December':
    month = '12'

date = '{}-{}-{}'.format(year, month, day)
print(date)