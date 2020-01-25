from journal.journal_template import JournalTemplate

import re

class JournalOfImmunology(JournalTemplate):

    search_mode = 3
    crawling_delay = 10
        
    journal_name = 'Journal_of_Immunology'
    journal_url = 'https://www.jimmunol.org'
    latest_articles_url = ''
    sql_database_path = 'database/{}.sqlite'.format(journal_name)

    pat_article      = r'<div class="highwire-article-citation highwire-citation-type-highwire-article"[\s\S]+?</li>'
    pat_title        = r'<span class="highwire-cite-title">([\s\S]+?)</span>'
    pat_url          = r'<a href="(.+?)"'
    pat_article_kind = r'<div class="highwire-(article)-citation highwire-citation-type-highwire-article'
    pat_publish_date = r'<span  class="highwire-cite-metadata-date highwire-cite-metadata">(.+?), </span>'
    pat_authors      = r'<span class="highwire-citation-author.*?" data-delta="\d+">(.+?)</span>'
    pat_abstract     = r'<meta name="citation_abstract" lang="en" content="&lt;p&gt;(.+?)&lt;/p&gt;" />'

    pat_article_part = r'<h2 class="pane-title">Latest Articles</h2>([\s\S]+?)</ul>'

    def format_date(self, date):
    
        [month, day, year] = date.split()

        day = day[:-1]
        if len(day) == 1:
            day = '0' + day
        pass

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
        #### This method may be overrided for each journals

        #delete html tag
        abstract = re.sub(r'\&lt;.+?\&gt;', "" , abstract)

        abstract = re.sub(r'\n|\r', "", abstract)

        abstract = re.sub(r'\s+', " ", abstract)
        abstract = re.sub(r'\s+\.', ".", abstract)
        abstract = re.sub(r'\s+\,', ",", abstract)

        return abstract