from journal.journal import Journal_Template

class Cell(Journal_Template):

    def __init__(self):
        
        journal_name = 'Cell'
        journal_url = "https://www.cell.com"
        latest_articles_url = "/cell/newarticles"
        db_path = 'database/{}.sqlite'.format(journal_name)

        pat_article      = r'<section class="toc__section aop__toc">[\s\S]+?</section>'
        pat_title        = r'<a href="/cell/fulltext/[\s\S]+?" title="([\s\S]+?)">'
        pat_url          = r'<a href="(/cell/fulltext/[\s\S]+?)"'
        pat_article_kind = r'<div class="toc__item__type">(.+?)</div>'
        pat_publish_date = r'<div class="toc__item__date">.+?:(.+?)</div>'
        pat_authors      = r'<li class="loa__item">(.+?)[,<]'
        pat_abstract     = r'<div class="section-paragraph">[^<]*<div class="section-paragraph">([\s\S]+?)</div>'

        super().__init__(journal_name, journal_url, latest_articles_url, pat_article, pat_title, pat_url, pat_article_kind, pat_publish_date, pat_authors, pat_abstract, db_path)

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
