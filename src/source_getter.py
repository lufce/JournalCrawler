import requests as webs
import lxml.html, time, pickle, sys, re

text_writter_file_name = 'nature_latest_research.txt'
html_pickle_name = 'html_content_pickle.binf'

url = "https://www.nature.com/nature/research"

def html_text_writter(url):

    time.sleep(1.0)
    res = webs.get(url)
    res.encoding = res.apparent_encoding

    with open(text_writter_file_name,'w', encoding='utf-8') as f:
        f.write(res.text)

    print('{} end'.format(sys._getframe().f_code.co_name))

def dump_html_content_pickle(url):
    time.sleep(1.0)
    res = webs.get(url)
    res.encoding = res.apparent_encoding

    with open(html_pickle_name, 'wb') as f:
        pickle.dump(res.content,f)
    
    print('{} end'.format(sys._getframe().f_code.co_name))

def lxml_load_from_html_content_pickle(file_path):
    with open(file_path, 'rb') as f:
        res_cont = pickle.load(f)

    page = lxml.html.fromstring(res_cont)
    
    print('{} end'.format(sys._getframe().f_code.co_name))

    return page



if __name__ == '__main__':
    # html_text_writter(url)
    # dump_html_content_pickle(url)

    page = lxml_load_from_html_content_pickle(html_pickle_name)
    #titles_xpath = "//article/div/h3/a/text()"
    html_text = lxml.html.tostring(page)

    pat_article = r'<article>[\s\S]+?</article>'
    pat_title = r'<a href.+>([\s\S]+?)</a>'

    print(type(html_text))

    iter_articles = re.findall(pat_article,html_text.decode('utf-8'))

    for article in iter_articles:
        iter_titles = re.findall(pat_title, article)

        for title in iter_titles:
            print(title.encode('utf-8').decode('utf-8'))
    