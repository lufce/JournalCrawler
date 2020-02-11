from journal.cell_press import Cell, CancerCell, Immunity
from journal.aaas import Science
from journal.nature_group import *
from journal.rockefeller_university_press import JournalOfExperimentalMedicine
from journal.journal_of_immunology import JournalOfImmunology

import arrange_html_table, my_sqlite, html_mail_send
import logging, time

##### logging setting

now = time.strftime('%Y%m%d-%H%M')

date_format = '%H:%M:%S'
log_format = '%(asctime)s| %(message)s'
logging.basicConfig(filename='log/{}.log'.format(now),level=logging.INFO, format=log_format, datefmt=date_format)

##### main

logging.info('Crawling Starts.')

journal_list = [Nature(), NatureImmunology(), NatureMedicine(), NatureMethods(), NatureReviewsImmunology(), \
                Cell(), CancerCell(), Immunity(), \
                JournalOfExperimentalMedicine(), \
                JournalOfImmunology(), \
                Science(), ScientificReports()]
journal_card_list = []
contents_list_card = ''

for j in journal_list:

    logging.info('--------------------%s starts--------------------', j.journal_name)

    # get article items except the abstracts
    logging.info('Store article')
    j.store_article_list()

    # judge new item from database
    logging.info('Save article info into %s', j.sql_database_path)
    is_new_list = my_sqlite.write_article_info_into_database(j.sql_database_path, j.article_list)
    j.is_new_article = tuple(is_new_list)

    logging.info('Getting abstracts')
    j.get_abstract()

    logging.info('Making article cards')
    article_cards = arrange_html_table.make_article_cards(j.article_list, j.is_new_article)

    logging.info('Making journal card')
    journal_card = arrange_html_table.make_journal_card(j, article_cards)
    if journal_card != '':
        journal_card_list.append(journal_card)
    
    contents_list_card = arrange_html_table.make_contents_list_card(j, contents_list_card)

logging.info('Making journal cards')
journal_cards = arrange_html_table.join_cards(journal_card_list)

logging.info('Making html mail body')
html = arrange_html_table.wrap_html_tags(journal_cards)

logging.info('Sending mails')
html_mail_send.html_mailing('今朝の新着論文',html)

logging.info('End')