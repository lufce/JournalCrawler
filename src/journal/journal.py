import re

class journal:
    
    re_exp = []
    pat_article = ''
    pat_title = ''
    pat_url = ''
    pat_article_type = ''
    pat_publish_date = ''
    pat_author = ''
    pat_abstract = ''
    
    journal_name = ''
    journal_url = ''
    latest_articles_url = ''

    def format_text(self, text):
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

    def format_abstract(self, abstract):

        #delete reference number
        abstract = re.sub(r'<sup>[\s\S]+?</sup>',"",abstract)

        #delete html tag
        abstract = re.sub(r'<.+?>', "" ,abstract)

        abstract = re.sub(r'\s+?', " ", abstract)
        abstract = re.sub(r'\s+?\.', ".", abstract)
        abstract = re.sub(r'\s+?\,', ",", abstract)

        return abstract