import re, time
import requests as webs
import article.article as article_module
import translation

accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
accept_enc = 'gzip, deflate, br'
accept_lang = 'ja,en-US;q=0.9,en;q=0.8,pt;q=0.7'
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
hds = {'Accept':accept,'Accept-Encoding':accept_enc,'Accept-Language':accept_lang,'User-Agent': ua}

class JournalTemplate:
    article_list = ()

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

    #used in store_article_items2
    pat_article_genre = ''

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
            self.__get_article_items1()
        elif self.search_mode == 2:
            self.__get_article_items2()
        else:
            return
        
        #self.__get_abstract()

    def __get_article_items1(self):
        ##### get latest articles
        #with webs.Session() as ses:
            #ses.headers.update(hds)
            
        time.sleep(self.crawling_delay)
        #page = ses.get(self.journal_url + self.latest_articles_url, timeout=3)
        page = webs.get(self.journal_url + self.latest_articles_url, headers=hds, timeout=self.timeout)
        aritcle_htmls = re.findall(self.pat_article, page.text)

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
            counter += 1

            if counter == 2:
                break
        
        self.article_list = tuple(article_list_buf)
        self.__get_abstract()

    def __get_article_items2(self):
        ##### get latest articles
        with webs.Session() as ses:
            ses.headers.update(hds)

            time.sleep(self.crawling_delay)
            page = ses.get(self.journal_url + self.latest_articles_url, timeout=self.timeout)
            aritcle_genre_htmls = re.findall(self.pat_article_genre, page.text)

            ###### get article items
            #counter = 0
            article_list_buf = []

            for genre_html in aritcle_genre_htmls:
                article_kind = self.check_items_in_article(re.findall(self.pat_article_kind, genre_html))
                article_kind = self.format_text(article_kind)

                aritcle_htmls = re.findall(self.pat_article, genre_html)
                
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
                    #counter += 1

                    #if counter == 5:
                        #break
            
            self.article_list = tuple(article_list_buf)
            self.__get_abstract()
        
    def __get_abstract(self):
        c = 0
        ##### convert relative urls into absolute urls, and rewrite url items
        for a in self.article_list:
            a.url = self.journal_url + a.url
        
        ##### get abstracts of articles
        for a in self.article_list:
            c += 1
            print(c)

            time.sleep(self.crawling_delay)

            try:
                #page2 = session.get(a.url, timeout=3)
                page2 = webs.get(a.url, headers=hds, timeout=self.timeout)

                a.abstract_e = self.check_items_in_article(re.findall( self.pat_abstract, page2.text))
                a.abstract_e = self.format_abstract(a.abstract_e)
                
                a.abstract_j = translation.translation_en_into_ja(a.abstract_e)
            except webs.exceptions.ConnectionError:
                print('error is occered.')