# from journal.cell_press import CancerCell
# cc = CancerCell()
# pass

import re

a = '<sup>1,2,3,4,5</sup>'
b = '<sup>1</sup>'

print(re.sub(r'<sup>(\d+,)*\d</sup>',"",a))
print(re.sub(r'<sup>\d+</sup>',"",b))