import sqlite3 as sql
import article.article as article_module

def __get_yyyymm_from_date(date):
    #date format is yyyy-mm-dd
    return(date[:4]+date[5:7])

def __get_yyyymm_list(date_list):
    yyyymm_list = []
    
    for date in date_list:
        yyyymm = __get_yyyymm_from_date(date)

        if len(yyyymm_list) == 0:
            yyyymm_list.append(yyyymm)
        else:
            isNew = True

            for ym in yyyymm_list:
                if yyyymm == ym:
                    isNew = False
                    break
            
            if isNew:
                yyyymm_list.append(yyyymm)
    
    return yyyymm_list

def __previous_yyyymm(date):
    yy = int( date[:4])
    mm = int( date[5:7])

    if mm - 1 == 0:
        yy = yy - 1
        mm = 12
    else:
        mm -= 1

    yy = str(yy)
    mm = str(mm)

    if len(mm) == 1:
        mm = '0' + mm

def write_article_info_into_database(db_path, article_list):
    # database schema is (title UNIQUE, urls UNIQUE, article_type TEXT, date TEXT, authors TEXT)
    # dupulication is detected by database integrity error due to UNIQUE item.    

    # yyyymm like 201903 is used as a table name.
    date_list = [a.date for a in article_list]
    yyyymm_list = __get_yyyymm_list(date_list)

    if len(yyyymm_list) > 10:
        # large viriaty of yyyymm list indicates wrong list reference.
        #TODO 独自の例外処理
        raise Exception

    connection = sql.connect(db_path)
    c = connection.cursor()

    for yyyymm in yyyymm_list:
        c.execute('CREATE TABLE IF NOT EXISTS T_{} (title UNIQUE, url UNIQUE, article_type TEXT, date TEXT, authors TEXT)'.format(yyyymm))

    # boolean list for choice articles to be mailed.
    is_new_contents = []

    for i in range(len(article_list)):
        
        # get table_name for entry of the article
        yyyymm = __get_yyyymm_from_date(article_list[i].date)

        try:
            c.execute('INSERT INTO T_{} (title, url, article_type, date, authors) VALUES (?,?,?,?,?)'.format(yyyymm), \
                ( article_list[i].title_e, article_list[i].url, article_list[i].kind, article_list[i].date, article_list[i].authors ))

            # No exception meands that this article is new one.
            is_new_contents.append(True)

        except sql.IntegrityError as err:
            if 'UNIQUE' in err.args[0]:

                # if IntegrityError occurs, this article has already been registered.
                is_new_contents.append(False)

            else:
                raise Exception

    connection.commit()
    connection.close()

    return is_new_contents

def __test_write_article_info_into_database():
    # article_item_list contains [titles, urls, article_types, dates, authors]
    db_path = 'database/sqlite_test.sqlite'

    article_list = article_module.create_dummy_article_list(5)

    write_article_info_into_database(db_path, article_list)

if __name__ == '__main__':
    __test_write_article_info_into_database()
