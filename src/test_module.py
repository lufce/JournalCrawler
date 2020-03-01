from journal_lxml.cell_press import Cell, CancerCell, Immunity
from journal_lxml.pnas import Pnas
from journal_re.aaas import Science
from journal_re.nature_group import *
from journal_re.rockefeller_university_press import JournalOfExperimentalMedicine
from journal_re.journal_of_immunology import JournalOfImmunology

import arrange_html_table, my_sqlite, html_mail_send

##### main
journal_list = [Pnas()]
journal_card_list = []
contents_list_card = ''

for j in journal_list:

    try:

        # get article items except the abstracts
        j.store_article_list()

        # judge new item from database
        j.is_new_article = tuple([True] * len(j.article_list))

        j.get_abstract()

        article_cards = arrange_html_table.make_article_cards(j.article_list, j.is_new_article)

        journal_card = arrange_html_table.make_journal_card(j, article_cards)
        if journal_card != '':
            journal_card_list.append(journal_card)
        
        contents_list_card = arrange_html_table.make_contents_list_card(j, contents_list_card)
    
    except IndexError:
        print('IndexError Occured. Html layout may be changed in {}.'.format(j.journal_name))

journal_cards = arrange_html_table.join_cards(journal_card_list)

html = arrange_html_table.wrap_html_tags(contents_list_card + journal_cards)

html_mail_send.html_mailing('今朝の新着論文', html, 'debug')


