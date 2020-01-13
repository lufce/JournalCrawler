import re, time
import requests as webs
import article.article as article_module
import translation

class Journal_Template:
    article_list = []

    pat_article = ''
    pat_title = ''
    pat_url = ''
    pat_article_kind = ''
    pat_publish_date = ''
    pat_authors = ''
    pat_abstract = ''
    
    journal_name = ''
    journal_url = ''
    latest_articles_url = ''

    def __init__(self, journal_name, journal_url, latest_articles_url, \
                 pat_article, pat_title, pat_url, pat_article_kind, \
                 pat_publish_date, pat_authors, pat_abstract):
        
        self.pat_article = pat_article

        self.pat_title = pat_title
        self.pat_url = pat_url
        self.pat_article_type = pat_article_kind
        self.pat_publish_date = pat_publish_date
        self.pat_author = pat_authors
        self.pat_abstract = pat_abstract
        
        self.journal_name = journal_name
        self.journal_url = journal_url
        self.latest_articles_url = latest_articles_url

    def article_url (self):
        return self.journal_url + self.latest_articles_url

    def __check_items_in_article(self, item_list):

        if len(item_list) > 1:
            # for items of authors
            return ', '.join(item_list)

        elif len(item_list) == 1:
            return item_list[0]
        else:
            return ""

    def store_article_list(self):
        ##### get latest articles
        #self.reg_exps += [pat_title, pat_url, pat_article_kind, pat_publish_date, pat_author, pat_abstract]
        time.sleep(1)
        page = webs.get(self.journal_url + self.latest_articles_url)
        aritcle_htmls = re.findall(self.pat_article, page.text)

        ###### get article items
        counter = 0

        for html in aritcle_htmls:
            a = article_module.Aritcle()
            
            a.title_e = self.__check_items_in_article(re.findall( self.pat_title,        html))
            a.url     = self.__check_items_in_article(re.findall( self.pat_url,          html))
            a.kind    = self.__check_items_in_article(re.findall( self.pat_article_kind, html))
            a.date    = self.__check_items_in_article(re.findall( self.pat_publish_date, html))
            a.authors = self.__check_items_in_article(re.findall( self.pat_authors,      html))

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

            abstract = self.__check_items_in_article(re.findall( self.pat_abstract, page2.text))
            abstract = article_module.format_abstract(abstract)
            
            a.abstract_e = abstract
            a.abstract_j = translation.translation_en_into_ja(a.abstract_e)         