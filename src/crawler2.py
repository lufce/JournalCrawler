from journal.cell_press import Cell, Immunity

import arrange_html_table
import my_sqlite
import html_mail_send

journal_list = [Cell(),Immunity()]

journal_card_list = []

for journal in journal_list:
    journal.store_article_list()

    is_new_list = my_sqlite.write_article_info_into_database(journal.sql_database_path, journal.article_list)

    article_cards = arrange_html_table.make_article_cards(journal.article_list,is_new_list)
    journal_card_list.append(arrange_html_table.make_journal_card(journal.journal_name, article_cards))

journal_cards = arrange_html_table.join_cards(journal_card_list)

html = arrange_html_table.wrap_html_tags(journal_cards)

html_mail_send.html_mailing('test',html)
