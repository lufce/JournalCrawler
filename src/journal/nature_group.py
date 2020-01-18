from src.journal.journal_template import JournalTemplate

class Nature(JournalTemplate):
        
    journal_name = 'Nature'
    journal_url = "https://www.nature.com"
    latest_articles_url = "/nature/research"
    db_path = 'database/{}.sqlite'.format(journal_name)

    pat_article      = r'<article>[\s\S]+?</article>'
    pat_title        = r'<a href.+>([\s\S]+?)</a>'
    pat_url          = r'<a href="(.+?)" '
    pat_article_kind = r'<span data-test="article.type">(.+?)</span>'
    pat_publish_date = r'<time datetime="(.+?)" itemprop'
    pat_authors      = r'<span itemprop="name">(.+?)</span>'
    pat_abstract     = r'id="Abs1-content">([\s\S]+?)</p>'
