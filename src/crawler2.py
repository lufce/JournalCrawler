from journal.nature_group.nature import Nature

import arrange_html_table
import my_sqlite
import html_mail_send

nature = Nature()
nature.store_article_list()

is_new_list = my_sqlite.write_article_info_into_database(nature.sql_database_path, nature.article_list)

article_cards = arrange_html_table.make_article_cards(nature.article_list,is_new_list)
journal_card = arrange_html_table.make_journal_card(nature.journal_name, article_cards)
html = arrange_html_table.wrap_html_tags(journal_card)

html_mail_send.html_mailing('test',html)
