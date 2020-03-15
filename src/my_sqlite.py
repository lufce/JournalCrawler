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

    # if len(yyyymm_list) > 20:
    #     # large viriaty of yyyymm list indicates wrong list reference.
    #     #TODO 独自の例外処理
    #     raise Exception

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

def __search_records_by_date(cur, date):
    
    pass

# =======================for debug or test =============================
def __show_records_in_the_table(con, table_name):
    cur = con.cursor()
    for rec in cur.execute("select * from {}".format(table_name)):
        print(rec)
    cur.close()

def __show_records_in_the_sqlite_master(con):
    cur = con.cursor()
    for c in cur.execute("select * from sqlite_master"):
        print(c)
    cur.close()

def __show_records_at_the_date(con, date):
    #yyyy-mm-dd is required as data fromat.
    date_list = date.split('-')
    
    # check date format
    if len(date_list) != 3:
        print('invalid date fromat')
        return
    
    is_invalid = False
    for num in date_list:
        if num.isdecimal() == False:
            print('{} is not decimal'.format(num))
            is_invalid = True
    
    if is_invalid:
        return

    cur = con.cursor()
    tuple_date = (date,)
    yyyymm = date_list[0] + date_list[1]
    for rec in cur.execute('select * from T_{yyyymm} where date = ?'.format(yyyymm = yyyymm), tuple_date):
        print(rec)
    
    cur.close()
    
    print(date_list)

def __rename_table_name(con, old_name, new_name):
    
    __show_records_in_the_sqlite_master(con)

    cur = con.cursor()
    order = 'alter table {old} rename to {new}'.format(old = old_name, new = new_name)
    cur.execute(order)
    cur.close()

    print("")
    __show_records_in_the_sqlite_master(con)

def __temp():
    db_path = 'database/Immunity.sqlite'
    con = sql.connect(db_path)

    try:
        #__show_records_in_the_table(con, 'T_')
        #__show_records_in_the_sqlite_master(con)
        #__show_records_at_the_date(con,'2020-03-13')
        __rename_table_name(con, 'T_', 'T_202003')
    finally:
        con.close()



if __name__ == '__main__':
    #__test_write_article_info_into_database()
    __temp()