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

def create_dummy_article_list(article_number):
    article_list = []

    for i in range(article_number):
        a = Aritcle()

        a.title_e = 'title {}'.format(i+1)
        a.title_j = 'タイトル {}'.format(i+1)
        a.abstract_e = 'abstract {}'.format(i+1)
        a.abstract_j = '要約 {}'.format(i+1)
        a.authors = 'author1, author2, author3'
        a.kind = 'article'
        if i < 3:
            a.date = '2019-11-30'
        else:
            a.date = '2019-12-01'
        a.url = 'https://www.nature.com/articles/s41586-019-1799-6'

        article_list.append(a)

    return article_list

class Aritcle:

    title_e    = ''
    title_j    = ''
    url        = ''
    kind       = ''
    date       = ''
    authors    = ''
    abstract_e = ''
    abstract_j = ''