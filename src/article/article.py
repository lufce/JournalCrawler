def create_dummy_article_list(article_number):
    article_list = []

    for i in range(article_number):
        a = Aritcle()

        a.title_e = 'title {}'.format(i+1)
        a.title_j = 'タイトル {}'.format(i+1)
        a.abstract_e = 'abstract {}'.format(i+1)
        a.abstract_j = '要約 {}'.format(i+1)
        a.authors = 'author1, author2, author3'
        a.kind = 'article'
        if i < 3:
            a.date = '2019-11-30'
        else:
            a.date = '2019-12-01'
        a.url = 'https://www.nature.com/articles/s41586-019-1799-6'

        article_list.append(a)

    return article_list

class Aritcle:

    title_e    = ''
    title_j    = ''
    url        = ''
    kind       = ''
    date       = ''
    authors    = ''
    abstract_e = ''
    abstract_j = ''