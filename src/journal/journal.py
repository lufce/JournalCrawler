import re, time
import requests as webs

class Journal_Template:
    
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

    def __check_items_in_article(self, item_list):

        if len(item_list) > 1:
            # for items of authors
            return ', '.join(item_list)

        elif len(item_list) == 1:
            return item_list[0]
        else:
            return ""

    def __format_text(self, text):
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

    def __format_abstract(self, abstract):

        #delete reference number
        abstract = re.sub(r'<sup>[\s\S]+?</sup>',"",abstract)

        #delete html tag
        abstract = re.sub(r'<.+?>', "" ,abstract)

        abstract = re.sub(r'\s+?', " ", abstract)
        abstract = re.sub(r'\s+?\.', ".", abstract)
        abstract = re.sub(r'\s+?\,', ",", abstract)

        return abstract

    def get_article_items(self):
        ##### get latest articles
        #self.reg_exps += [pat_title, pat_url, pat_article_type, pat_publish_date, pat_author, pat_abstract]
        time.sleep(1)
        page = webs.get(self.journal_url + self.latest_articles_url)
        articles = re.findall(self.pat_article, page.text)

        #TODO Articleオブジェクトを作る。
        titles        = []
        urls          = []
        article_types = []
        dates         = []
        authors       = []

        article_item_list = []
        article_item_list += [    titles,    urls,    article_types,            dates,    authors]

        ###### get article items

        counter = 0

        for article in articles:
            for i in range(0, len(article_item_list)):
                article_item_list[i].append(self.__format_text(self.__check_items_in_article(re.findall(self.reg_exps[i], article))))
            
            counter += 1

            if counter == 5:
                break

        ##### convert relative urls into absolute urls
        for i in range(len(urls)):
            urls[i] = self.journal_url + urls[i]

        ###### check whether the lengths of item_lists are equal
        check_buffer = True

        for i in range(0, len(article_item_list)-1):
            check_buffer = check_buffer and (len(article_item_list[i]) == len(article_item_list[i+1]))
        
            if check_buffer == False:
                break

        if check_buffer == False:
            #TODO エラーを返すようにしなければならない
            print("the lenghts of article_item_list are not equal")
        
        ##### get abstracts of articles
        abstracts = []
        for url in urls:

            time.sleep(1)
            page2 = webs.get(url)

            abstract = self.__check_items_in_article(re.findall(self.reg_exps[5],page2.text))
            abstract = self.__format_abstract(abstract)
            abstracts.append(abstract)

        article_item_list.append(abstracts)

        return article_item_list

    def article_url (self):
        return self.journal_url + self.latest_articles_url