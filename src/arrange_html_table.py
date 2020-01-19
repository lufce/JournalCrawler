import article.article as article_module

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

def __make_article_card(article):
    article_card ='''
    <table width="{width}" border="{border}" cellpadding="{padding}" cellspacing="{spacing}">
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
                   spacing=__ARTICLE_TABLE_CELLSPC, title_bgcolor=__ARTICLE_TITLE_BGCOLOR, title_j=article.title_j, article_url=article.url, \
                   title_e=article.title_e, abs_j=article.abstract_j, abs_e=article.abstract_e, article_type=article.kind, date=article.date, authors=article.authors, \
                   article_line_font_size=__ARTICLE_LINE_FONT_SIZE, author_line_font_size=__AUTHOR_LINE_FONT_SIZE)

    return article_card

def join_cards(card_list):
    cards = '\n'.join(card_list)
    return cards

def make_article_cards(article_list, is_new_list):
    # if all article is not new, return '' ( empty string ).
    #article_item_list = [titles, urls, article_types, dates, authors, abstracts]

    article_card_list=[]

    for i in range(0, len(article_list)):
        if is_new_list[i]:
            article_card_list.append(__make_article_card(article_list[i]))
    
    article_cards = join_cards(article_card_list)

    return article_cards

def make_journal_card(journal_name,article_cards):
    if article_cards == '':
        return ''
    else:

        journal_card = '''<table width="{journal_width}" border="{journal_border}" cellpadding="{journal_padding}" cellspacing="{journal_spacing}" bgcolor="{journal_bgcolor}">
        <tr>
            <td>
                <font size="6"><b>{journal_title}</b></font><br>
                {article_cards}
            </td>
        </tr>
        </table>'''.format(journal_width=__JOURNAL_TABLE_WIDHT, journal_border=__JOURNAL_TABLE_BORDER, \
                    journal_padding=__JOURNAL_TABLE_CELLPAD, journal_spacing=__JOURNAL_TABLE_CELLSPC, \
                    journal_bgcolor=__JOURNAL_TABLE_BGCOLOR, journal_title=journal_name, article_cards=article_cards)

        return journal_card

def wrap_html_tags(journal_cards):
    if journal_cards == '':
        return ''

    else:

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
    article_list = article_module.create_dummy_article_list(3)

    is_new_list = [True,False,True]
    article_cards = make_article_cards(article_list,is_new_list)

    journal_card = make_journal_card('journal_title', article_cards)

    html = wrap_html_tags(journal_card)

    with open('journal_card_test.txt','w', encoding='UTF-8') as f:
        f.write(html)
    

if __name__=='__main__':
    test()