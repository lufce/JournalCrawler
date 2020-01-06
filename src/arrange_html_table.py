##### settings

__JOURNAL_TABLE_WIDHT    = '100%'
__JOURNAL_TABLE_BORDER   = '0'
__JOURNAL_TABLE_CELLPAD  = '5'
__JOURNAL_TABLE_CELLSPC  = '10'
__JOURNAL_TABLE_BGCOLOR  = '#ffffff'

__ARTICLE_TABLE_WIDTH    = '100%'
__ARTICLE_TABLE_BORDER   = '0'
__ARTICLE_TABLE_CELLPAD  = '5'
__ARTICLE_TABLE_CELLSPC  = '10'

__ARTICLE_TITLE_BGCOLOR  = '#ededed'
__ARTICLE_LINE_FONT_SIZE = '2'
__AUTHOR_LINE_FONT_SIZE  = '2'

##### /settings

def __make_article_card(title_e, title_j, abs_e, abs_j, authors, article_type, date, url):
    article_card ='''<table width="{width}" border="{border}" cellpadding="{padding}" cellspacing="{spacing}">
        <tr>
            <td bgcolor="{title_bgcolor}"><font size="{article_line_font_size}">{article_type}:{date}</font><br>
            <b><a href="{article_url}">{title_j}</b> {title_e}</a><br>
            <font size="{author_line_font_size}">{authors}</font>
            </td>
        </tr>
        <tr>
            <td>{abs_j}<br>{abs_e}</td>
        </tr>
</table>
    <br>'''.format(width=__ARTICLE_TABLE_WIDTH, border=__ARTICLE_TABLE_BORDER, padding=__ARTICLE_TABLE_CELLPAD, \
                   spacing=__ARTICLE_TABLE_CELLSPC, title_bgcolor=__ARTICLE_TITLE_BGCOLOR, title_j=title_j, article_url=url, \
                   title_e=title_e, abs_j=abs_j, abs_e=abs_e, article_type=article_type, date=date, authors=authors, \
                   article_line_font_size=__ARTICLE_LINE_FONT_SIZE, author_line_font_size=__AUTHOR_LINE_FONT_SIZE)

    return article_card

def __join_article_cards(article_card_list):
    article_cards = '\n'.join(article_card_list)
    return article_cards

def make_article_cards(article_item_list, title_j, abs_j):
    #article_item_list = [titles, urls, article_types, dates, authors, abstracts]

    title_e      = article_item_list[0]
    url          = article_item_list[1]
    article_type = article_item_list[2]
    date         = article_item_list[3]
    authors      = article_item_list[4]
    abs_e        = article_item_list[5]

    article_card_list=[]

    for i in range(0, len(title_e)):
        article_card_list.append(__make_article_card(title_e[i], title_j[i], abs_e[i], abs_j[i], authors[i], article_type[i], date[i], url[i]))
    
    article_cards = __join_article_cards(article_card_list)

    return article_cards

def make_journal_card(journal_title,article_cards):
    journal_card = '''<table width="{journal_width}" border="{journal_border}" cellpadding="{journal_padding}" cellspacing="{journal_spacing}" bgcolor="{journal_bgcolor}">
    <tr>
        <td>
            <font size="6"><b>{journal_title}</b></font><br>
            {article_cards}
        </td>
    </tr>
</table>'''.format(journal_width=__JOURNAL_TABLE_WIDHT, journal_border=__JOURNAL_TABLE_BORDER, \
                   journal_padding=__JOURNAL_TABLE_CELLPAD, journal_spacing=__JOURNAL_TABLE_CELLSPC, \
                   journal_bgcolor=__JOURNAL_TABLE_BGCOLOR, journal_title=journal_title, article_cards=article_cards)

    return journal_card

def wrap_html_tags(journal_cards):
    html_text = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
    <head></head>
    <body>
    {}
    </body>
</html>
    '''.format(journal_cards)

    return html_text

def test():
    article_card_list = []

    for i in range(1,4):
        title = 'title {}'.format(i)
        abstract = 'abstract {}'.format(i)
        author_list = 'author1, author2, author3'
        article_type = 'article'
        date = '2019-12-12'
        url = 'https://www.nature.com/articles/s41586-019-1799-6'

        article_card_list.append(__make_article_card(title, "タイトル", abstract, "要約", author_list, article_type, date, url))
    
    article_cards = __join_article_cards(article_card_list)

    journal_card = make_journal_card('journal_title', article_cards)

    with open('journal_card_test.txt','w', encoding='UTF-8') as f:
        f.write(journal_card)
    

if __name__=='__main__':
    test()