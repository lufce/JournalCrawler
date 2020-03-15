import re

class JournalTemplate:
    # クラス変数としてミュータブルなリストを用いると、継承した子のクラスと共有されてしまい、正常に動作しない。
    # なのでTupleにしている。
    article_list = ()
    is_new_article = ()
    occured_error = False

    #sqliteを操作するためのコネクション
    connection = None

    # set -1 for getting articles unlimitedly
    counter_limit = -1

    search_mode = 0
    crawling_delay = 10
    timeout = 10

    journal_name = ''
    journal_url = ''
    latest_articles_url = ''
    sql_database_path = ''

    # crawler_setting
    accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    accept_enc = 'gzip, deflate, br'
    accept_lang = 'ja,en-US;q=0.9,en;q=0.8,pt;q=0.7'
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    hds = {'Accept':accept,'Accept-Encoding':accept_enc,'Accept-Language':accept_lang,'User-Agent': ua}

    def article_url (self):
        return self.journal_url + self.latest_articles_url
    
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
        self.get_article_items()

    def get_article_items(self):
        # should be overrided
        pass

    def get_abstract(self):
        # should be overrided
        pass