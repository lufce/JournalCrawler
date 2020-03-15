from journal_lxml.journal_template import JournalTemplate
import requests as webs
import article.article as article_module
import translation
import lxml.html, time, pickle, re, logging

class Science(JournalTemplate):

    crawling_delay = 10
    #counter_limit = 1

    journal_name = 'Science'
    journal_url = 'https://science.sciencemag.org/'
    latest_articles_url = ''
    sql_database_path = 'database/{}.sqlite'.format(journal_name)

    def format_date(self, date):
        [day, month, year] = date.split()

        if   month == 'Jan':
            month = '01'
        elif month == 'Feb':
            month = '02'
        elif month == 'Mar':
            month = '03'
        elif month == 'Apr':
            month = '04'
        elif month == 'May':
            month = '05'
        elif month == 'Jun':
            month = '06'
        elif month == 'Jul':
            month = '07'
        elif month == 'Aug':
            month = '08'
        elif month == 'Sep':
            month = '09'
        elif month == 'Oct':
            month = '10'
        elif month == 'Nov':
            month = '11'
        elif month == 'Dec':
            month = '12'

        return '{}-{}-{}'.format(year, month, day)
    
    def format_abstract(self, abstract):
        abstract = re.sub(r'<.+?>',"",abstract)

        return abstract

    def get_article_items(self):
        ##### get latest articles
        logging.info('start crawling_delay')
        time.sleep(self.crawling_delay)
        logging.info('end crawling_delay')

        logging.info('start get method')
        page = webs.get(self.journal_url + self.latest_articles_url, headers=self.hds, timeout=self.timeout)
        logging.info('end get method')

        #logging page_source each time for debug
        with open('log/page_source_{}.binf'.format(self.journal_name), 'wb') as f:
             pickle.dump(page, f)

        ###### get article items 
        html = lxml.html.fromstring(page.content)

        article_section1 = html.xpath("//ul[@class='issue-toc item-list']")
        article_section2 = article_section1[0].xpath(".//article")
        article_list_buf = []
        counter = 0

        logging.info('found %s articles',str(len(article_section2)))

        for a_sec in reversed(article_section2):
            a = article_module.Aritcle()

            # get item sections
            title_sec  = a_sec.xpath("./div/h3/a/div")
            author_sec = a_sec.xpath(".//span[@class='highwire-citation-authors']/span/text()")
            #url_sec    = a_sec.xpath(".//a[@class='highwire-cite-linked-title']/@href")
            url_sec    = a_sec.xpath(".//a[@class='hiwire-cite-linked-title']/@href")
            date_sec   = a_sec.xpath(".//time/text()")

            # get items
            a.title_e = title_sec[0].text_content()
            a.url     = url_sec[0]
            a.authors = ', '.join(author_sec)
            a.date    = self.format_date(date_sec[0])

            # translation
            a.title_j = translation.translation_en_into_ja(a.title_e)

            # add article to article_list
            article_list_buf.append(a)

            # logging
            counter += 1
            logging.info('added a article:%s',str(counter))

            # limitation for getting articles
            if self.counter_limit != -1:
                if counter == self.counter_limit:
                    break
        
        self.article_list = tuple(reversed(article_list_buf))
    
    def get_abstract(self):
        ##### convert relative urls into absolute urls, and rewrite url items
        for a in self.article_list:
            a.url = self.journal_url + a.url

        for i in range(len(self.article_list)):
            if self.is_new_article[i]:
                a = self.article_list[i]

                logging.info('start crawling_delay')
                time.sleep(self.crawling_delay)
                logging.info('end crawling_delay')

                try:
                    logging.info('start get method: %s', a.title_e)
                    page = webs.get(a.url, headers=self.hds, timeout=self.timeout)
                    page.encoding = page.apparent_encoding
                    logging.info('end get method')
                    html = lxml.html.fromstring(page.content)

                    #get article type
                    kind_sec = html.xpath("//meta[@name='citation_section']/@content")
                    a.kind = kind_sec[0]

                    #get abstract
                    abstract_content = html.xpath("//meta[@name='citation_abstract']/@content")
                    a.abstract_e = self.format_abstract(abstract_content[0])
                    a.abstract_j = translation.translation_en_into_ja(a.abstract_e)
                
                except webs.exceptions.ConnectTimeout:
                    logging.exception('ConnectTimeout')
                except webs.exceptions.ReadTimeout:
                    logging.exception('ReadTimeout')
                except webs.exceptions.RetryError:
                    logging.exception('RetryError')
                except IndexError:
                    a.abstract_j = "abstractの取得に失敗しました。"

        pass

class ScienceTranslationalMedicine(Science):
    crawling_delay = 10
    #counter_limit = 1

    journal_name = 'Science_Translational_Medicine'
    journal_url = 'https://stm.sciencemag.org/'
    latest_articles_url = ''
    sql_database_path = 'database/{}.sqlite'.format(journal_name)

class ScienceImmunology(Science):
    crawling_delay = 10
    #counter_limit = 5

    journal_name = 'Science_Immunology'
    journal_url = 'https://immunology.sciencemag.org'
    latest_articles_url = ''
    sql_database_path = 'database/{}.sqlite'.format(journal_name)

class ScienceSignaling(Science):
    crawling_delay = 10
    #counter_limit = 1

    journal_name = 'Science_Translational_Medicine'
    journal_url = 'https://stke.sciencemag.org/'
    latest_articles_url = ''
    sql_database_path = 'database/{}.sqlite'.format(journal_name)