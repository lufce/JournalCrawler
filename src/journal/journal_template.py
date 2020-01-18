import re, time
import requests as webs
import article.article as article_module
import translation

class JournalTemplate:
    article_list = []

    journal_name = ''
    journal_url = ''
    latest_articles_url = ''
    sql_database_path = ''

    pat_article = ''
    pat_title = ''
    pat_url = ''
    pat_article_kind = ''
    pat_publish_date = ''
    pat_authors = ''
    pat_abstract = ''

    def article_url (self):
        return self.journal_url + self.latest_articles_url

    def check_items_in_article(self, item_list):
        if len(item_list) == 0:
            return ""
        else:
            return item_list[0]
    
    def format_item_of_authors(self, item_list):
        #### This method may be overrided for each journals
        return ', '.join(item_list)

    def format_text(self, text):
        #### This method may be overrided for each journals

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
        #### This method may be overrided for each journals

        #delete reference number
        abstract = re.sub(r'<sup>[\s\S]+?</sup>',"",abstract)

        #delete html tag
        abstract = re.sub(r'<.+?>', "" , abstract)

        abstract = re.sub(r'\n|\r', "", abstract)

        abstract = re.sub(r'\s+', " ", abstract)
        abstract = re.sub(r'\s+\.', ".", abstract)
        abstract = re.sub(r'\s+\,', ",", abstract)

        return abstract
    
    def format_date(self, date):
        #### This method should be overrided for each journals
        #### Date format is yyyy-mm-dd, filling 0 if less digit.
        #### ex.) 1990-07-01

        return date

    def store_article_list(self):
        ##### get latest articles
        time.sleep(1)
        page = webs.get(self.journal_url + self.latest_articles_url)
        aritcle_htmls = re.findall(self.pat_article, page.text)

        ###### get article items
        counter = 0

        for html in aritcle_htmls:
            a = article_module.Aritcle()
            
            # get items in article
            a.title_e = self.check_items_in_article(re.findall( self.pat_title,        html))
            a.url     = self.check_items_in_article(re.findall( self.pat_url,          html))
            a.kind    = self.check_items_in_article(re.findall( self.pat_article_kind, html))
            a.date    = self.check_items_in_article(re.findall( self.pat_publish_date, html))

            # format items
            a.authors = self.format_item_of_authors(re.findall( self.pat_authors,      html))
            a.title_e = self.format_text(a.title_e)
            a.date    = self.format_date(a.date)

            a.title_j = translation.translation_en_into_ja(a.title_e)
            
            self.article_list.append(a)
            counter += 1

            if counter == 5:
                break

        ##### convert relative urls into absolute urls, and rewrite url items
        for a in self.article_list:
            a.url = self.journal_url + a.url
        
        ##### get abstracts of articles
        for a in self.article_list:

            time.sleep(1)
            page2 = webs.get(a.url)
            
            a.abstract_e = self.check_items_in_article(re.findall( self.pat_abstract, page2.text))
            a.abstract_e = self.format_abstract(a.abstract_e)
            
            a.abstract_j = translation.translation_en_into_ja(a.abstract_e)