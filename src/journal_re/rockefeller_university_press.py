from journal_re.journal_template import JournalTemplate

class JournalOfExperimentalMedicine(JournalTemplate):

    search_mode = 3
    crawling_delay = 3
        
    journal_name = 'Journal_of_Experimental_Medicine'
    journal_url = 'https://rupress.org'
    latest_articles_url = '/JEM'
    sql_database_path = 'database/{}.sqlite'.format(journal_name)

    pat_article      = r'<div class="widget-dynamic-entry">[\s\S]+?<!-- /.widget-dynamic-journal-abstract -->'
    pat_title        = r'<div class="widget-dynamic-journal-title">[^>]+?([\s\S]+?)</a>'
    pat_url          = r'<a href="(.+?)">'
    pat_article_kind = r'<div class="widget-dynamic-journal-categories">([\s\S]+?)</div>'
    pat_publish_date = r'<div class="widget-dynamic-journal-article-date">([\s\S]+?)</div>'
    pat_authors      = r'<div class="widget-dynamic-journal-authors">([\s\S]+?)</div>'
    pat_abstract     = r'<section class="abstract"><p>([\s\S]+?)</p></section>'

    pat_article_part = r'Newest Articles([\s\S]+?)Browse All'

    def format_date(self, date):
        
        [month, day, year] = date.split()

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