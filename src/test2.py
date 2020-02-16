import pickle
import lxml.html
from lxml import etree
import requests
import re
import entity_references as er

# page = requests.get('https://www.cell.com/cell/fulltext/S0092-8674(20)30055-6')
# page.encoding = page.apparent_encoding
# with open('log/page_source_ca2.binf','wb') as f:
#      pickle.dump(page,f)

def format_abstract(abstract):
    abstract = re.sub(r'\n +<.+?>',"",abstract)
    abstract = re.sub(r'<.+?>', "", abstract)

    # remove space sequence
    abstract = re.sub(r'^ +| +$',"",abstract, flags=re.MULTILINE)

    # remove newline
    abstract = re.sub(r'-\n|-\r',"-",abstract)

    # remove newline
    abstract = re.sub(r'\n|\r'," ",abstract)

    return abstract

with open('log/page_source_ca2.binf','rb') as f:
    page = pickle.load(f)

html = lxml.html.fromstring(page.content)
sum_sec = html.xpath("//h2[@data-left-hand-nav='Summary']/following-sibling::div/div")

replace_text = er.change_entity_references_to_utf8_in_text(lxml.html.tostring(sum_sec[0]).decode('utf-8'))
abstract = format_abstract(replace_text)

print(abstract)