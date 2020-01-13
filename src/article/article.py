import re

def format_text(text):
    #replace newline with space
    text = re.sub(r'\n', " ", text)

    #replace sequential space with single space
    text = re.sub(r'\s+', " ", text)

    #delete spaces at start of string
    text = re.sub(r'^\s+', "", text)

    #delete space before period
    text = re.sub(r'\s+\.', ".", text)

    #delete space before comma
    text = re.sub(r'\s+\,', ",", text)

    return text

def format_abstract(abstract):

    #delete reference number
    abstract = re.sub(r'<sup>[\s\S]+?</sup>',"",abstract)

    #delete html tag
    abstract = re.sub(r'<.+?>', "" ,abstract)

    abstract = re.sub(r'\s+?', " ", abstract)
    abstract = re.sub(r'\s+?\.', ".", abstract)
    abstract = re.sub(r'\s+?\,', ",", abstract)

    return abstract

class Aritcle:
    item_number_except_abstract = 5

    title    = ''
    url      = ''
    kind     = ''
    date     = ''
    authors  = ''
    abstract = ''

    item_list = []
    item_list += [title, url, kind, date, authors, abstract]