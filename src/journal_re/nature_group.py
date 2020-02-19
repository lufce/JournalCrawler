from journal_re.journal_template import JournalTemplate
import re

class Nature(JournalTemplate):

    search_mode = 1
    crawling_delay = 3
        
    journal_name = 'Nature'
    journal_url = 'https://www.nature.com'
    latest_articles_url = '/nature/research'
    sql_database_path = 'database/{}.sqlite'.format(journal_name)

    pat_article      = r'<article>[\s\S]+?</article>'
    pat_title        = r'<a href.+>([\s\S]+?)</a>'
    pat_url          = r'<a href="(.+?)" '
    pat_article_kind = r'<span data-test="article.type">(.+?)</span>'
    pat_publish_date = r'<time datetime="(.+?)" itemprop'
    pat_authors      = r'<span itemprop="name">(.+?)</span>'
    pat_abstract     = r'id="Abs1-content">([\s\S]+?)</p>'


    def format_abstract(self, abstract):
        #### This method may be overrided for each journals

        #delete reference number
        abstract = re.sub(r'<sup>[\d,–]+?</sup>',"",abstract)   #- is not minus or hyphen. maybe dash.
        abstract = re.sub(r'<sup><a data-track="click" data-track-action="reference anchor"[\s\S]+?</sup>',"",abstract)

        #delete html tag
        abstract = re.sub(r'<.+?>', "" , abstract)

        abstract = re.sub(r'\n|\r', "", abstract)

        abstract = re.sub(r'\s+', " ", abstract)
        abstract = re.sub(r'\s+\.', ".", abstract)
        abstract = re.sub(r'\s+\,', ",", abstract)

        abstract = re.sub(r',\.', ".", abstract)

        return abstract

class NatureImmunology(Nature):
        
    journal_name = 'Nature_Immunology'
    
    latest_articles_url = '/ni/research'
    sql_database_path = 'database/{}.sqlite'.format(journal_name)

class NatureMedicine(Nature):
        
    journal_name = 'Nature_Medicine'
    
    latest_articles_url = '/nm/research'
    sql_database_path = 'database/{}.sqlite'.format(journal_name)

class NatureCancer(Nature):
        
    journal_name = 'Nature_Cancer'
    
    latest_articles_url = '/natcancer/research'
    sql_database_path = 'database/{}.sqlite'.format(journal_name)

class NatureMethods(Nature):
        
    journal_name = 'Nature_Methods'
    
    latest_articles_url = '/nmeth/research'
    sql_database_path = 'database/{}.sqlite'.format(journal_name)

class NatureReviewsImmunology(Nature):
        
    journal_name = 'Nature_Reviews_Immunology'
    
    latest_articles_url = '/nri/reviews'
    sql_database_path = 'database/{}.sqlite'.format(journal_name)

class ScientificReports(Nature):
        
    journal_name = 'Scientific_Reports'

    pat_title        = r'<img[^>]+?>([\s\S]+?)</a>'
    
    latest_articles_url = '/subjects/immunology/srep'
    sql_database_path = 'database/{}.sqlite'.format(journal_name)

class NatureCommunications(Nature):
        
    journal_name = 'Nature_Communications'

    pat_title        = r'<img[^>]+?>([\s\S]+?)</a>'
    
    latest_articles_url = '/subjects/immunology/ncomms'
    sql_database_path = 'database/{}.sqlite'.format(journal_name)