import requests as webs
import time, re
import lxml.html

import arrange_html_table as ar
import translation as tr
import html_mail_send as mailing

text_writter_file_name = 'nature_latest_research.txt'
html_pickle_name = 'html_content_pickle.binf'

def check_items_in_article(item_list):

    if len(item_list) > 1:
        # for items of authors
        return ', '.join(item_list)

    elif len(item_list) == 1:
        return item_list[0]
    else:
        return ""

def format_text(text):
    #replace newline with space
    text = re.sub(r'\n', " ", text)

    #replace sequential space with single space
    text = re.sub(r'\s+', " ", text)

    #delete spaces at start of string
    text = re.sub(r'^\s+', "", text)

    #delete space before period
    text = re.sub(r'\s+\.', ".", text)

    #delete space before comma
    text = re.sub(r'\s+\,', ",", text)

    return text

def format_abstract(abstract):

    #delete reference number
    abstract = re.sub(r'<sup>[\s\S]+?</sup>',"",abstract)

    #delete html tag
    abstract = re.sub(r'<.+?>', "" ,abstract)

    abstract = re.sub(r'\s+?', " ", abstract)
    abstract = re.sub(r'\s+?\.', ".", abstract)
    abstract = re.sub(r'\s+?\,', ",", abstract)

    return abstract

def nature():
    journal_url = "https://www.nature.com"
    latest_articles_url = "/nature/research"

    ##### get latest articles
    time.sleep(1)
    page = webs.get(journal_url + latest_articles_url)

    ##### get article elements
    pat_article      = r'<article>[\s\S]+?</article>'
    pat_title        = r'<a href.+>([\s\S]+?)</a>'
    pat_url          = r'<a href="(.+?)" '
    pat_article_type = r'<span data-test="article.type">(.+?)</span>'
    pat_publish_date = r'<time datetime="(.+?)" itemprop'
    pat_author       = r'<span itemprop="name">(.+?)</span>'

    articles = re.findall(pat_article,page.text)

    titles        = []
    urls          = []
    article_types = []
    dates         = []
    authors       = []

    reg_exps = []
    article_item_list = []
    
    #次のforループを回すために取得する項目リストを1つのリストにまとめる
    reg_exps          += [pat_title, pat_url, pat_article_type, pat_publish_date, pat_author]
    article_item_list += [    titles,    urls,    article_types,            dates,    authors]

    ###### get article items

    counter = 0

    for article in articles:
        for i in range(0, len(article_item_list)):
            article_item_list[i].append(format_text(check_items_in_article(re.findall(reg_exps[i], article))))
        
        counter += 1

        if counter == 3:
            break

    ##### convert relative urls into absolute urls
    for i in range(len(urls)):
        urls[i] = journal_url + urls[i]

    ###### check whether the lengths of item_lists are equal
    check_buffer = True

    for i in range(0, len(article_item_list)-1):
        check_buffer = check_buffer and (len(article_item_list[i]) == len(article_item_list[i+1]))
    
        if check_buffer == False:
            break

    if check_buffer == False:
        #TODO エラーを返すようにしなければならない
        print("the lenghts of article_item_list are not equal")

    #TODO できればここまでを一つの関数として使いまわしたい
    ##### get abstracts of articles
    abstracts = []
    for url in urls:

        time.sleep(1)
        page2 = webs.get(url)

        pat_abstract = r'id="Abs1-content">([\s\S]+?)</p>'
        abstract = check_items_in_article(re.findall(pat_abstract,page2.text))
        abstract = format_abstract(abstract)
        abstracts.append(abstract)

    article_item_list.append(abstracts)

    return article_item_list

if __name__ == '__main__':
    #article_item_list = [titles, urls, article_types, dates, authors, abstracts]

    item_list = nature()

    title_j = tr.translation_english_list(item_list[0])
    abs_j = tr.translation_english_list(item_list[5])

    article_cards = ar.make_article_cards(item_list, title_j, abs_j)
    journal_card = ar.make_journal_card('Nature', article_cards)
    html_text = ar.wrap_html_tags(journal_card)
    
    mailing.html_mailing("article_alart",html_text)