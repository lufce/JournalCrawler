import pickle, lxml.html
import article.article as article_module

def open_page_source_pickle(journal_name):
    with open('log/page_source_{}.binf'.format(journal_name), 'rb') as f:
            page = pickle.load(f)
    
    return page

def get_items_in_PNAS(page):
    html = lxml.html.fromstring(page.content)

    article_section = html.xpath("//div[@class='highwire-cite highwire-cite-highwire-article highwire-citation-pnas-list-complete clearfix']")

    try:
        #for a_sec in reversed(article_section):
        for a_sec in article_section:
            a = article_module.Aritcle()

            # get item sections
            title_sec  = a_sec.xpath(".//span[@class='highwire-cite-title']")

            # get items
            a.title_e = ''.join(title_sec[0].itertext())
            pass

    except IndexError:
        raise IndexError

if __name__ == '__main__':
    p = open_page_source_pickle('PNAS')
    get_items_in_PNAS(p)