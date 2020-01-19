import re, time
import requests as webs
import article.article as article_module
import translation

import logging

accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
accept_enc = 'gzip, deflate, br'
accept_lang = 'ja,en-US;q=0.9,en;q=0.8,pt;q=0.7'
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
hds = {'Accept':accept,'Accept-Encoding':accept_enc,'Accept-Language':accept_lang,'User-Agent': ua}

counter_limit = 6

class JournalTemplate:
    # クラス変数としてミュータブルなリストを用いると、継承した子のクラスと共有されてしまい、正常に動作しない。
    # なのでTupleにしている。
    article_list = ()
    is_new_article = ()

    search_mode = 0
    crawling_delay = 10
    timeout = 10

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

    #used in get_article_items2
    pat_article_genre = ''

    #used in get_article_items3
    pat_article_part = ''

    def article_url (self):
        return self.journal_url + self.latest_articles_url

    def check_items_in_article(self, item_list):
        if len(item_list) == 0:
            return ""
        else:
            if type(item_list[0]) is tuple:
                for item in item_list[0]:
                    if item != '':
                        return item
            else:
                return item_list[0]
    
    def format_item_of_authors(self, item_list):
        #### This method may be overrided for each journals
        return ', '.join(item_list)

    def format_text(self, text):
        #### This method may be overrided for each journals

        #delete html tag
        text = re.sub(r'<.+?>', "" , text)

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

        #delete space at the end of sentence
        text = re.sub(r'\s+$', "", text)

        return text

    def format_abstract(self, abstract):
        #### This method may be overrided for each journals

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
        if   self.search_mode == 1:
            logging.info('start get_article_item1: %s', self.journal_name)
            self.__get_article_items1()
        elif self.search_mode == 2:
            logging.info('start get_article_item2: %s', self.journal_name)
            self.__get_article_items2()
        elif self.search_mode == 3:
            logging.info('start get_article_item3: %s', self.journal_name)
            self.__get_article_items3()
        else:
            return

    def __get_article_items1(self):
        ##### get latest articles
        logging.info('start crawling_delay')
        time.sleep(self.crawling_delay)
        logging.info('end crawling_delay')

        logging.info('start get method')
        page = webs.get(self.journal_url + self.latest_articles_url, headers=hds, timeout=self.timeout)
        logging.info('end get method')

        aritcle_htmls = re.findall(self.pat_article, page.text)
        logging.info('get %s articles', str(len(aritcle_htmls)))

        ###### get article items
        counter = 0
        article_list_buf = []

        # take articles by oldest first
        for html in reversed(aritcle_htmls):
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
            
            article_list_buf.append(a)
            logging.info('added a article')

            counter += 1

            if counter_limit != -1:
                if counter == counter_limit:
                    break
        
        self.article_list = tuple(reversed(article_list_buf))

    def __get_article_items2(self):
        ##### get article genre list
        logging.info('start crawling_delay')
        time.sleep(self.crawling_delay)
        logging.info('end crawling_delay')

        logging.info('start get method')
        page = webs.get(self.journal_url + self.latest_articles_url, headers=hds, timeout=self.timeout)
        logging.info('end get method')

        aritcle_genre_htmls = re.findall(self.pat_article_genre, page.text)
        logging.info('get %s article genres', str(len(aritcle_genre_htmls)))

        ###### get article list
        article_list_buf = []

        for genre_html in aritcle_genre_htmls:
            article_kind = self.check_items_in_article(re.findall(self.pat_article_kind, genre_html))
            article_kind = self.format_text(article_kind)

            aritcle_htmls = re.findall(self.pat_article, genre_html)
            logging.info('get %s articles in %s', str(len(aritcle_htmls)), article_kind)
            
            ##### get article items
            for html in aritcle_htmls:
                a = article_module.Aritcle()
                
                # get items in article
                a.title_e = self.check_items_in_article(re.findall( self.pat_title,        html))
                a.url     = self.check_items_in_article(re.findall( self.pat_url,          html))
                a.kind    = article_kind
                a.date    = self.check_items_in_article(re.findall( self.pat_publish_date, html))

                # format items
                a.authors = self.format_item_of_authors(re.findall( self.pat_authors,      html))
                a.title_e = self.format_text(a.title_e)
                a.date    = self.format_date(a.date)

                a.title_j = translation.translation_en_into_ja(a.title_e)
                
                article_list_buf.append(a)
                logging.info('added a article')
            
            self.article_list = tuple(reversed(article_list_buf))

    def __get_article_items3(self):
        ##### get new articles part
        logging.info('start crawling_delay')
        time.sleep(self.crawling_delay)
        logging.info('end crawling_delay')

        logging.info('start get method')
        page = webs.get(self.journal_url + self.latest_articles_url, headers=hds, timeout=self.timeout)
        logging.info('end get method')

        new_articles_html = re.findall(self.pat_article_part, page.text)[0]

        ###### get articles
        counter = 0
        article_list_buf = []
        aritcle_htmls = re.findall(self.pat_article, new_articles_html)
        logging.info('get %s articles', str(len(aritcle_htmls)))

        # take articles by oldest first
        for html in reversed(aritcle_htmls):
            a = article_module.Aritcle()
            
            # get items in article
            a.title_e = self.check_items_in_article(re.findall( self.pat_title,        html))
            a.url     = self.check_items_in_article(re.findall( self.pat_url,          html))
            a.kind    = self.check_items_in_article(re.findall( self.pat_article_kind, html))
            a.date    = self.check_items_in_article(re.findall( self.pat_publish_date, html))

            # format items
            a.authors = self.format_text(self.format_item_of_authors(re.findall( self.pat_authors, html)))
            a.title_e = self.format_text(a.title_e)
            a.kind    = self.format_text(a.kind)
            a.date    = self.format_date(a.date)

            a.title_j = translation.translation_en_into_ja(a.title_e)
            
            article_list_buf.append(a)
            logging.info('added a article')
            counter += 1

            if counter_limit != -1:
                if counter == counter_limit:
                    break
        
        self.article_list = tuple(reversed(article_list_buf))

    def get_abstract(self):
        c = 0
        ##### convert relative urls into absolute urls, and rewrite url items
        for a in self.article_list:
            a.url = self.journal_url + a.url
        
        ##### get abstracts of only new articles
        for i in range(len(self.article_list)):
            if self.is_new_article[i]:
                a = self.article_list[i]
                c += 1
                print(c)

                logging.info('start crawling_delay')
                time.sleep(self.crawling_delay)
                logging.info('end crawling_delay')

                try:
                    logging.info('start get method: %s', a.title_e)
                    page2 = webs.get(a.url, headers=hds, timeout=self.timeout)
                    logging.info('end get method')

                    a.abstract_e = self.check_items_in_article(re.findall( self.pat_abstract, page2.text))
                    a.abstract_e = self.format_abstract(a.abstract_e)
                    
                    a.abstract_j = translation.translation_en_into_ja(a.abstract_e)
                except webs.exceptions.ConnectTimeout:
                    logging.exception('ConnectTimeout')
                except webs.exceptions.ReadTimeout:
                    logging.exception('ReadTimeout')
                except webs.exceptions.RetryError:
                    logging.exception('RetryError')