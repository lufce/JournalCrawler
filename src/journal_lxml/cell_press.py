from journal_lxml.journal_template import JournalTemplate
import requests as webs
import article.article as article_module
import translation, entity_references
import lxml.html, time, pickle, re, logging

class Cell(JournalTemplate):
    
    counter_limit = 3

    journal_name = 'Cell'
    journal_url = 'https://www.cell.com'
    latest_articles_url = '/cell/newarticles'
    sql_database_path = 'database/{}.sqlite'.format(journal_name)

    def format_date(self, date):
        
        if 'First published' in date:
            #delete 'First published:'
            date = date[16:]

        [month, day, year] = date.split()
        day = day[:2]

        if   month == 'January':
            month = '01'
        elif month == 'February':
            month = '02'
        elif month == 'March':
            month = '03'
        elif month == 'April':
            month = '04'
        elif month == 'May':
            month = '05'
        elif month == 'June':
            month = '06'
        elif month == 'July':
            month = '07'
        elif month == 'August':
            month = '08'
        elif month == 'September':
            month = '09'
        elif month == 'October':
            month = '10'
        elif month == 'November':
            month = '11'
        elif month == 'December':
            month = '12'

        return '{}-{}-{}'.format(year, month, day)
    
    def format_abstract(self, abstract):
        abstract = re.sub(r'\n +<.+?>',"",abstract)
        abstract = re.sub(r'<.+?>', "", abstract)

        # remove space sequence
        abstract = re.sub(r'^ +| +$',"",abstract, flags=re.MULTILINE)

        
        abstract = re.sub(r'-\n|-\r',"-",abstract)

        # remove newline
        abstract = re.sub(r'\n|\r'," ",abstract)

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

        article_section = html.xpath("//div[@class='toc__item__body']")
        article_list_buf = []
        counter = 0

        logging.info('found %s articles',str(len(article_section)))

        try:
            for a_sec in reversed(article_section):
                a = article_module.Aritcle()

                # get item sections
                title_sec  = a_sec.xpath(".//h3[@class='toc__item__title']/a")
                author_sec = a_sec.xpath(".//ul[@class='toc__item__authors loa rlist--inline']/li/text()")
                kind_sec   = a_sec.xpath(".//div[@class='toc__item__type']/text()")
                date_sec   = a_sec.xpath(".//div[@class='toc__item__date']/text()")

                # get items
                buf_str = lxml.html.tostring(title_sec[0]).decode('utf-8')
                buf_str = entity_references.change_entity_references_to_utf8_in_text(buf_str)
                title_sec2 = lxml.html.fromstring(buf_str)

                a.title_e = title_sec2.text_content()
                a.url     = title_sec[0].values()[0]
                a.authors = ' '.join(author_sec)
                a.kind    = kind_sec[0]
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

        except IndexError:
            raise IndexError
    
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

                    #get abstract
                    if a.kind == 'Primer' or a.kind == 'Review':
                        abstract_sec = html.xpath("//div[@class='container']/div/div[2]/section[1]/div/div")
                    else:
                        abstract_sec = html.xpath("//h2[@data-left-hand-nav='Summary']/following-sibling::div/div")
                    
                    replace_text = entity_references.change_entity_references_to_utf8_in_text(lxml.html.tostring(abstract_sec[0]).decode('utf-8'))
                    a.abstract_e = self.format_abstract(replace_text)
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

class CancerCell(Cell):

    journal_name = 'Cancer_Cell'
    latest_articles_url = "/cancer-cell/newarticles"
    sql_database_path = 'database/{}.sqlite'.format(journal_name)

class Immunity(Cell):
    journal_name = 'Immunity'
    latest_articles_url = "/immunity/newarticles"
    sql_database_path = 'database/{}.sqlite'.format(journal_name)