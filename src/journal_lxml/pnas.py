from journal_lxml.journal_template import JournalTemplate
import requests as webs
import article.article as article_module
import translation
import lxml.html, time, pickle, re, logging

class Pnas(JournalTemplate):
    
    search_mode = 1
    crawling_delay = 10
    #counter_limit = 1

    journal_name = 'PNAS'
    journal_url = 'https://www.pnas.org'
    latest_articles_url = r'/content/by/section/Immunology%20and%20Inflammation'
    sql_database_path = 'database/{}.sqlite'.format(journal_name)

    def format_date(self, date):
        if 'first published' in date:
            #delete 'first published '
            date = date[16:-2]
        else:
            date = date[:-1]

        [month, day, year] = date.split()
        day = day[:-1]

        if len(day) == 1:
            day = '0' + day

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

        article_section = html.xpath("//div[@class='highwire-cite highwire-cite-highwire-article highwire-citation-pnas-list-complete clearfix']")
        article_list_buf = []
        counter = 0

        logging.info('found %s articles',str(len(article_section)))

        try:
            for a_sec in reversed(article_section):
                a = article_module.Aritcle()

                # get item sections
                title_sec  = a_sec.xpath(".//span[@class='highwire-cite-title']/text()")
                author_sec = a_sec.xpath(".//span[@class='highwire-citation-authors']/span/text()")
                url_sec    = a_sec.xpath(".//a[@class='highwire-cite-linked-title']/@href")
                date_sec   = a_sec.xpath(".//span[@class='highwire-cite-metadata-papdate highwire-cite-metadata']/text()")

                # get items
                a.title_e = title_sec[0]
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

                    #get article type
                    kind_sec = html.xpath("//span[@class='highwire-cite-metadata-article-category highwire-cite-metadata']/text()")
                    a.kind = kind_sec[0]

                    #get abstract
                    #abstract_sec = html.xpath("//div[@class='section abstract']/p")
                    abstract_content = html.xpath("//meta[@name='citation_abstract']/@content")[0]
                    a.abstract_e = self.format_abstract(abstract_content)
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