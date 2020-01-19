from journal.journal_template import JournalTemplate

class Cell(JournalTemplate):
    
    search_mode = 1

    journal_name = 'Cell'
    journal_url = 'https://www.cell.com'
    latest_articles_url = '/cell/newarticles'
    sql_database_path = 'database/{}.sqlite'.format(journal_name)

    pat_article      = r'<section class="toc__section aop__toc">[\s\S]+?</section>'
    pat_title        = r'<a href="/[^/]+/fulltext/[\s\S]+?" title="([\s\S]+?)">'
    pat_url          = r'<a href="(/[^/]+/fulltext/[\s\S]+?)"'
    pat_article_kind = r'<div class="toc__item__type">(.+?)</div>'
    pat_publish_date = r'<div class="toc__item__date">.+?:(.+?)</div>'
    pat_authors      = r'<li class="loa__item">(.+?)[,<]'
    pat_abstract     = r'<div class="section-paragraph">[^<]*<div class="section-paragraph">([\s\S]+?)</div>'

    def format_date(self, date):
        
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

class CancerCell(Cell):

    journal_name = 'Cancer Cell'
    latest_articles_url = "/cancer-cell/newarticles"

class Immunity(Cell):
    journal_name = 'Immunity'
    latest_articles_url = "/immunity/newarticles"