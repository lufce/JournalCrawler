import re, time
import requests as webs
import article.article as article_module

class Journal_Template:
    articles = []

    reg_exps = []
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

    def __init__(self, journal_name, journal_url, latest_articles_url, \
                 pat_article, pat_title, pat_url, pat_article_type, \
                 pat_publish_date, pat_author, pat_abstract):
        
        self.pat_article = pat_article

        self.pat_title = pat_title
        self.pat_url = pat_url
        self.pat_article_type = pat_article_type
        self.pat_publish_date = pat_publish_date
        self.pat_author = pat_author
        self.pat_abstract = pat_abstract
        
        self.journal_name = journal_name
        self.journal_url = journal_url
        self.latest_articles_url = latest_articles_url

        self.reg_exps += [pat_title, pat_url, pat_article_type, pat_publish_date, pat_author, pat_abstract]

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

    def get_articles(self):
        ##### get latest articles
        #self.reg_exps += [pat_title, pat_url, pat_article_type, pat_publish_date, pat_author, pat_abstract]
        time.sleep(1)
        page = webs.get(self.journal_url + self.latest_articles_url)
        aritcle_htmls = re.findall(self.pat_article, page.text)

        ###### get article items
        counter = 0

        for html in aritcle_htmls:
            a = article_module.Aritcle()

            for i in range(a.item_number_except_abstract):
                item = self.__check_items_in_article(re.findall(self.reg_exps[i], html))
                a.item_list[i] = article_module.format_text(item)
            
            self.articles.append(a)
            counter += 1

            if counter == 5:
                break

        ##### convert relative urls into absolute urls, and rewrite url items
        for a in self.articles:
            a.url = self.journal_url + a.url
        
        ##### get abstracts of articles
        for a in self.articles:

            time.sleep(1)
            page2 = webs.get(a.url)

            abstract = self.__check_items_in_article(re.findall(self.reg_exps[5],page2.text))
            abstract = article_module.format_abstract(abstract)
            
            a.abstract = abstract