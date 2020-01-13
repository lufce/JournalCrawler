from journal.journal import Journal_Template

class Nature(Journal_Template):

    def __init__(self):
        
        journal_name = 'Nature'
        journal_url = "https://www.nature.com"
        latest_articles_url = "/nature/research"

        pat_article      = r'<article>[\s\S]+?</article>'
        pat_title        = r'<a href.+>([\s\S]+?)</a>'
        pat_url          = r'<a href="(.+?)" '
        pat_article_kind = r'<span data-test="article.type">(.+?)</span>'
        pat_publish_date = r'<time datetime="(.+?)" itemprop'
        pat_authors      = r'<span itemprop="name">(.+?)</span>'
        pat_abstract     = r'id="Abs1-content">([\s\S]+?)</p>'

        super().__init__(journal_name, journal_url, latest_articles_url, pat_article, pat_title, pat_url, pat_article_kind, pat_publish_date, pat_authors, pat_abstract)