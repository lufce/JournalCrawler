# from journal_re.journal_template import JournalTemplate

# class Science(JournalTemplate):

#     search_mode = 2

#     journal_name = 'Science'
#     journal_url = 'https://science.sciencemag.org/'
#     latest_articles_url = ''
#     sql_database_path = 'database/{}.sqlite'.format(journal_name)

#     pat_article      = r'<article class="highwire-cite highwire-cite-highwire-article.+>[\s\S]+?</article>'
#     pat_title        = r'<div class="highwire.+?title">([\s\S]+?)</div>'
#     pat_url          = r'<a href="(/content/.+?)"'
#     pat_article_kind = r'<h2 id[^>]+?>([\s\S]+?)</h2>'
#     pat_publish_date = r'<time>(.+?)</time>'
#     pat_authors      = r'<span class="highwire-citation-author[^>]*?>([^<]+)</span>'
#     pat_abstract     = r'<div class="section abstract" id="abstract-[\d]"><h2>Abstract</h2><p id="p-[\d]+?">([\s\S]+?)</p></div>|<div class="section summary" id="abstract-[\d]"><h2>Summary</h2><p id="p-[\d]+?">([\s\S]+?)</p></div>'

#     pat_article_genre= r'<li class="issue-toc-section issue-toc-section-(?!contents)[^>]+?>[\s\S]+?</article></div></div></li></ul></li>'

#     def format_date(self, date):
    
#         [day, month, year] = date.split()

#         if   month == 'Jan':
#             month = '01'
#         elif month == 'Feb':
#             month = '02'
#         elif month == 'Mar':
#             month = '03'
#         elif month == 'Apr':
#             month = '04'
#         elif month == 'May':
#             month = '05'
#         elif month == 'Jun':
#             month = '06'
#         elif month == 'Jul':
#             month = '07'
#         elif month == 'Aug':
#             month = '08'
#         elif month == 'Sep':
#             month = '09'
#         elif month == 'Oct':
#             month = '10'
#         elif month == 'Nov':
#             month = '11'
#         elif month == 'Dec':
#             month = '12'

#         return '{}-{}-{}'.format(year, month, day)