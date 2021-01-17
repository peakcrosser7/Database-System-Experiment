import os
import pymysql


def clear_cmd():
    os.system('cls')


def is_Chinese(ch):
    if '\u4e00' <= ch <= '\u9fa5':
        return True
    else:
        return False


def len_str(string):
    count = 0
    for line in string:
        if is_Chinese(line):
            count = count + 2
        else:
            count = count + 1
    return count


def printing(string, size=0, e='\n'):
    l = size - len_str(string)
    if l > 0:
        string += ' ' * l
    print(string, end=e)


def print_list(str_list, format_list):
    for s, l in zip(str_list, format_list):
        s = str(s)
        printing(s, l, '')
    print('')


def print_sql(str_dict, format_list):
    for s, l in zip(str_dict.values(), format_list):
        s = str(s)
        printing(s, l, '')
    print('')


def inputing(msg, is_int=False):
    ret = input(msg)
    if not ret:
        return None
    if is_int:
        try:
            return int(ret)
        except Exception as e:
            print(e)
            return None
    return ret


class MyDB:
    def __init__(self, cfg):
        self.config = cfg
        self.db = pymysql.connect(**self.config)
        self.cursor = self.db.cursor()

    def insert_sql(self, table_name, value_list):
        s = '%s,' * len(value_list)
        sql = 'insert into ' + table_name + \
              ' values(' + s.rstrip(',') + ')'
        # print(sql)
        try:
            self.cursor.execute(sql, value_list)
            self.db.commit()
            return 1
        except Exception as e:
            print(e)
            self.db.rollback()
            return 0

    def select_sql(self, table_name, col_str, where_str=''):
        if not where_str:
            sql = 'select ' + col_str + ' from ' + table_name
        else:
            sql = 'select ' + col_str + ' from ' + table_name + \
                  ' where ' + where_str
        # print(sql)
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            flag = 1
            return flag, data
        except Exception as e:
            print(e)
            return 0, None

    def update_sql(self, table_name, col_list, value_list, where_str):
        s = ''
        for i in col_list:
            s += i + '=%s,'
        sql = 'update ' + table_name + ' set ' + s.rstrip(',') + \
              ' where ' + where_str
        # print(sql)
        try:
            self.cursor.execute(sql, value_list)
            self.db.commit()
            return 1
        except Exception as e:
            print(e)
            self.db.rollback()
            return 0

    def delete_sql(self, table_name, where_str):
        sql = 'delete from ' + table_name + ' where ' + where_str
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return 1
        except Exception as e:
            print(e)
            self.db.rollback()
            return 0
