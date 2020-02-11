import re

abstract = '''sleep<sup>5,6</sup> and depression<sup>7</sup>,<sup>1–4,8,9</sup>. Despite their'''

abstract = re.sub(r'<sup>[\d,–]+?</sup>',"",abstract)
abstract = re.sub(r',.', ".", abstract)

print(abstract)