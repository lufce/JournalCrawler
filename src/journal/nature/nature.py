import JournalCrawler.src.journal.journal as journal

class nature(journal):

    def __init__(self):
        self.journal_name = 'Nature'
        self.journal_url = "https://www.nature.com"
        self.latest_articles_url = "/nature/research"

        self.pat_article      = r'<article>[\s\S]+?</article>'
        self.pat_title        = r'<a href.+>([\s\S]+?)</a>'
        self.pat_url          = r'<a href="(.+?)" '
        self.pat_article_type = r'<span data-test="article.type">(.+?)</span>'
        self.pat_publish_date = r'<time datetime="(.+?)" itemprop'
        self.pat_author       = r'<span itemprop="name">(.+?)</span>'
        self.pat_abstract     = r'id="Abs1-content">([\s\S]+?)</p>'

        self.re_exp.append()